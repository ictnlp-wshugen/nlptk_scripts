#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-01-02 14:39
from options import get_parser
from options import parse_arguments
from utils.file_ops import load_file_contents


def get_stat_parser():
    parser = get_parser()
    parser.add_argument('-fps', '--file-paths', nargs='+',
                        help='file paths to be counted')
    return parser


def parse_stat_arguments():
    return parse_arguments(get_stat_parser())


def count_file_tokens(file_path):
    contents = load_file_contents(file_path)
    count = 0
    for line in contents:
        tokens = line.strip().split()
        count += len(tokens)
    return count


def main(args):
    count = 0
    for file_path in args.file_paths:
        _count = count_file_tokens(file_path)
        if args.verbose:
            print('{} tokens in {}'.format(_count, file_path))
        count += _count
    print('{} tokens total'.format(count))


if __name__ == '__main__':
    main(parse_stat_arguments())
