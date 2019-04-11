#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-01-02 14:39
from os.path import basename

from easy_tornado.utils.file_operation import load_file_contents
from easy_tornado.utils.logging import it_print

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
    contents = load_file_contents(file_path, strip=True)
    count, vocab = 0, set()
    total, seqs = len(contents), set()
    for line in contents:
        seqs.add(line)
        tokens = line.split()
        count += len(tokens)
        for token in tokens:
            vocab.add(token)
    return (count, vocab), (total, seqs)


def main(args):
    token_report = '{} tokens with diversity {}'
    sequence_report = '{} sequences with unique {}'
    count, vocab = 0, set()
    total, seqs = 0, set()
    for file_path in args.file_paths:
        (_count, _vocab), (_total, _seqs) = count_file_tokens(file_path)
        count += _count
        vocab |= _vocab
        total += _total
        seqs |= _seqs
        if args.verbose:
            it_print('{} statistics: '.format(basename(file_path)), indent=2)
            it_print(token_report.format(_count, len(_vocab)), indent=4)
            it_print(sequence_report.format(_total, len(_seqs)), indent=4)

    it_print('corpora statistics: ')
    it_print(token_report.format(count, len(vocab)), indent=2)
    it_print(sequence_report.format(total, len(seqs)), indent=2)


if __name__ == '__main__':
    main(parse_stat_arguments())
