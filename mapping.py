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
    assert len(src_contents) == len(tgt_contents)

    if output is None:
        output = 'mapping.json'

    length = len(src_contents)
    src_mapping = OrderedDict({
        k: src_contents[k] for k in range(length)
    })
    tgt_mapping = {
        k: tgt_contents[k] for k in range(length)
    }

    mapping = OrderedDict()
    for key in src_mapping.keys():
        it_print('handling {} ...'.format(key))
        value = src_contents[key]
        sub = None
        for sub in tgt_mapping.keys():
            if value == tgt_mapping[sub]:
                mapping[key] = sub
                break
        if sub is not None:
            tgt_mapping.pop(sub)

    write_file_contents(output, to_json(mapping, indent=2))


def cli_main():
    _args = parse_bpe_arguments()
    main(_args)


if __name__ == '__main__':
    cli_main()
