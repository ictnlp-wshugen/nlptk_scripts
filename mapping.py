#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-04-04 22:38
from collections import OrderedDict

from easy_tornado.utils.file_operation import file_exists
from easy_tornado.utils.file_operation import load_file_contents
from easy_tornado.utils.file_operation import write_file_contents
from easy_tornado.utils.logging import it_print
from easy_tornado.utils.str_extension import to_json
from tqdm import tqdm

from options import add_bilingual_args_
from options import add_output_args_
from options import get_parser
from options import parse_arguments


def get_mapping_parser():
    parser = get_parser()
    add_bilingual_args_(parser)
    add_output_args_(parser)
    return parser


def parse_bpe_arguments():
    return parse_arguments(get_mapping_parser())


def main(args):
    source, target, output = args.source, args.target, args.output_path
    assert all([file_exists(x) for x in [source, target]])

    src_contents = load_file_contents(source)
    tgt_contents = load_file_contents(target)
    src_cnt, tgt_cnt = len(src_contents), len(tgt_contents)
    assert src_cnt <= tgt_cnt
    it_print('source {} lines, target {} lines'.format(src_cnt, tgt_cnt))

    if output is None:
        output = 'mapping.json'

    src_mapping = OrderedDict({
        k + 1: src_contents[k] for k in range(src_cnt)
    })
    tgt_mapping = {
        k + 1: tgt_contents[k] for k in range(tgt_cnt)
    }

    mapping = OrderedDict()
    with tqdm(total=src_cnt, disable=not args.verbose) as pb:
        src_keys = list(sorted(src_mapping.keys()))
        for key in src_keys:
            sub, value = None, src_mapping[key]
            for sub in tgt_mapping:
                if value == tgt_mapping[sub]:
                    mapping[key] = sub
                    break
            if sub is not None:
                it_print('{} -> {}'.format(key, sub))
                src_mapping.pop(key)
                tgt_mapping.pop(sub)
            pb.update(1)

    write_file_contents(output, to_json(mapping, indent=2))
    write_file_contents('source.left.json', to_json(src_mapping, indent=2))
    write_file_contents('target.left.json', to_json(tgt_mapping, indent=2))


def cli_main():
    _args = parse_bpe_arguments()
    main(_args)


if __name__ == '__main__':
    cli_main()
