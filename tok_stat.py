#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-01-02 14:39
from easy_tornado.utils.file_operation import load_file_contents

from options import get_parser
from options import parse_arguments


def get_stat_parser():
    parser = get_parser()
    parser.add_argument('-fps', '--file-paths', nargs='+', required=True,
                        help='file paths to be counted')
    return parser


def parse_stat_arguments():
    return parse_arguments(get_stat_parser())


def count_file_tokens(file_path):
    contents = load_file_contents(file_path, strip=False)

    vocab = set()
    count = 0
    for line in contents:
        tokens = line.strip().split()
        count += len(tokens)
        for token in tokens:
            if token not in vocab:
                vocab.add(token)
    return count, vocab


def main(args):
    vocab = set()
    count = 0
    for file_path in args.file_paths:
        _count, _vocab = count_file_tokens(file_path)
        vocab |= _vocab
        if args.verbose:
            print('{} tokens with diversity {} in {}'
                  .format(_count, len(_vocab), file_path))
        count += _count
    print('{} tokens with diversity {} total'.format(count, len(vocab)))


if __name__ == '__main__':
    main(parse_stat_arguments())
