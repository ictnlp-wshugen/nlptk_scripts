#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-17 15:33
import io

import numpy

from options import get_convert_parser
from options import parse_arguments


def get_shuffle_parser():
    parser = get_convert_parser()
    parser.add_argument('-s', '--seed', type=int, default=195610,
                        help='the PRNG seed for reproducibility')
    return parser


def parse_shuffle_arguments():
    return parse_arguments(get_shuffle_parser())


def main(args):
    if args.output_path is None:
        setattr(args, 'output_path', '{}.shuffle'.format(args.file_path))
    with io.open(args.file_path, mode='r', encoding=args.encoding) as rfp, \
            io.open(args.output_path, mode='w', encoding=args.encoding) as wfp:
        contents = rfp.readlines()
        num_of_lines = len(contents)
        numpy.random.seed(args.seed)
        shuffled = numpy.random.permutation(num_of_lines)
        for index in shuffled:
            wfp.write(contents[index])


if __name__ == '__main__':
    arguments = parse_shuffle_arguments()
    main(arguments)
