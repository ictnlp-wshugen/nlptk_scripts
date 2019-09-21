#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-04-11 16:46
from collections import OrderedDict

from easy_tornado.compat import python2
from easy_tornado.utils.file_operation import file_exists
from easy_tornado.utils.file_operation import load_file_contents
from easy_tornado.utils.file_operation import write_file_contents
from easy_tornado.utils.logging import it_print
from easy_tornado.utils.str_extension import to_json

from options import get_parser
from options import parse_arguments

message = '{} duplicated samples: {}'


def get_dup_parser():
    parser = get_parser()
    parser.add_argument(
        '--source', '-s', required=True,
        help='source path to be analyzed (or source dup path)'
    )
    parser.add_argument(
        '--target', '-t', required=True,
        help='target path to be analyzed (or source dup path)'
    )
    parser.add_argument(
        '--corpus', '-c', action='store_true', default=False,
        help='whether the source and target is corpus path'
    )
    parser.add_argument(
        '--output', '-o', default='linenos.json',
        help='duplicated linenos output path'
    )
    parser.add_argument(
        '--remove', '-r', action='store_true', default=False,
        help='duplicated linenos output path'
    )

    return parser


def parse_dup_arguments():
    return parse_arguments(get_dup_parser())


def parse_duplicated(dup_path, prefix=''):
    duplicated = OrderedDict()
    dup_lines = load_file_contents(dup_path)
    for line in dup_lines:
        if python2:
            lineno, dno, subject = line.split(' ', 2)
        else:
            lineno, dno, subject = line.split(maxsplit=2)
        lineno = int(lineno)
        if dno in duplicated:
            duplicated[dno]['linenos'].append(lineno)
        else:
            duplicated[dno] = {
                'subject': subject,
                'linenos': [lineno],
            }

    it_print(message.format(prefix, len(duplicated)))
    return duplicated


def analyze(co_duplicated, src_duplicated, tgt_duplicated):
    co_linenos = set()
    for key in src_duplicated.keys():
        # the same line is marked as duplicated in target
        if key not in tgt_duplicated:
            continue

        source, target = src_duplicated[key], tgt_duplicated[key]
        src, src_linenos = source['subject'], source['linenos']
        tgt, tgt_linenos = target['subject'], target['linenos']
        for lineno in sorted(src_linenos):
            if lineno not in tgt_linenos:
                continue

            co_linenos.add(lineno)
            if key in co_duplicated:
                co_duplicated[key]['linenos'].append(lineno)
            else:
                co_duplicated[key] = {
                    'source': src,
                    'target': tgt,
                    'linenos': [lineno]
                }
            tgt_linenos.remove(lineno)
    co_duplicated['linenos'] = co_linenos
    it_print(message.format('common', len(co_linenos)))


def execute(source, target, co_duplicated, ext='.dedup', verbose=False):
    duplicated = co_duplicated.pop('linenos')
    src_contents = load_file_contents(source, strip=False)
    tgt_contents = load_file_contents(target, strip=False)
    total = len(src_contents)
    assert total == len(tgt_contents)

    src_lines, tgt_lines = [], []
    iterator = zip(src_contents, tgt_contents)
    for lineno, (src, tgt) in enumerate(iterator, start=1):
        if verbose and lineno % 10000 == 0:
            it_print('processed {}'.format(lineno))
        if lineno in duplicated:
            duplicated.remove(lineno)
            continue
        # write to file
        src_lines.append(src)
        tgt_lines.append(tgt)

    count = len(src_lines)
    assert count == len(tgt_lines)

    it_print('total {} lines, after filter, {} left'.format(total, count))
    write_file_contents(source + ext, ''.join(src_lines))
    write_file_contents(target + ext, ''.join(tgt_lines))


def main(args):
    ext = '.dup'
    if args.corpus:
        source, target = args.source, args.target
        src_dup_path, tgt_dup_path = source + ext, target + ext
    else:
        src_dup_path, tgt_dup_path = args.source, args.target
        assert src_dup_path.endswith(ext) and tgt_dup_path.endswith(ext)
        source = src_dup_path.replace(ext, '')
        target = tgt_dup_path.replace(ext, '')
    if not all([file_exists(x) for x in [src_dup_path, tgt_dup_path]]):
        raise ValueError('.dup files not exists, try to use tok_stat.py with '
                         '-o option to generate')

    co_duplicated = OrderedDict()
    src_duplicated = parse_duplicated(src_dup_path, 'source')
    tgt_duplicated = parse_duplicated(tgt_dup_path, 'target')
    analyze(co_duplicated, src_duplicated, tgt_duplicated)

    if args.remove:
        execute(source, target, co_duplicated, verbose=args.verbose)

    contents = to_json(co_duplicated, indent=2)
    write_file_contents(args.output, contents)


def cli_main():
    main(parse_dup_arguments())


if __name__ == '__main__':
    cli_main()
