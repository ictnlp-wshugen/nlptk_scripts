#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-01-02 14:39
from os.path import basename

from easy_tornado import it_print
from easy_tornado.utils import load_file_contents
from easy_tornado.utils import write_iterable_contents

from options import get_parser
from options import parse_arguments


def get_stat_parser():
    parser = get_parser()
    parser.add_argument(
        '--output-duplicated', '-o', action='store_true',
        help='output middle result, i.e. .dup file'
    )
    parser.add_argument(
        '--file-paths', '-fps', metavar='FPS', nargs='+', required=True,
        help='file paths to be counted'
    )

    return parser


def parse_stat_arguments():
    return parse_arguments(get_stat_parser())


def count_file_tokens(file_path):
    contents = load_file_contents(file_path, strip=True)
    count, vocab = 0, set()
    total, seqs = len(contents), set()
    seen, repeated = dict(), list()
    for lineno, line in enumerate(contents, start=1):
        if line == '':
            continue

        if line in seen:
            repeated.append((lineno, seen[line], line))
        else:
            seen[line] = lineno
        seqs.add(line)
        tokens = line.split()
        count += len(tokens)
        for token in tokens:
            vocab.add(token)
    return (count, vocab), (total, seqs), repeated


def main(args):
    token_report = '{} tokens with diversity {}'
    sequence_report = '{} sequences with unique {}'
    count, vocab = 0, set()
    total, seqs = 0, set()

    def dup2line(x):
        return '{} {} {}'.format(*x)

    for file_path in args.file_paths:
        _vocab_stat, _seq_stat, duplicated = count_file_tokens(file_path)
        (_count, _vocab) = _vocab_stat
        (_total, _seqs) = _seq_stat
        count += _count
        vocab |= _vocab
        total += _total
        seqs |= _seqs

        filename = basename(file_path)
        if args.verbose:
            it_print('{} statistics: '.format(filename), indent=2)
            it_print(token_report.format(_count, len(_vocab)), indent=4)
            it_print(sequence_report.format(_total, len(_seqs)), indent=4)

        if args.output_duplicated:
            dup_path = '{}.dup'.format(filename)
            write_iterable_contents(dup_path, duplicated, obj2line_func=dup2line)

    it_print('corpora statistics: ')
    it_print(token_report.format(count, len(vocab)), indent=2)
    it_print(sequence_report.format(total, len(seqs)), indent=2)


def cli_main():
    main(parse_stat_arguments())


if __name__ == '__main__':
    cli_main()
