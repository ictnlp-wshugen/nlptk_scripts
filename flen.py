#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/11/27 22:23
from __future__ import division

import io

from easy_tornado.utils.logging import it_print

from options import get_parser
from options import parse_arguments


def main(args):
    it_print(vars(args), json_fmt=True, indent=2)

    with io.open(args.file_path, mode='r', encoding='utf-8') as rfp:
        lines = [x.strip() for x in rfp.readlines()]
        total_count = len(lines)

    filtered_count, total_length, filtered_items = 0, 0, []
    for i, line in enumerate(lines):
        length = len(line.split() if args.split else line)
        total_length += length

        criteria = length > args.max_length
        if criteria:
            filtered_count += 1
            filtered_items.append((i, length, line))
    params = {
        'total_lines': total_count,
        'filtered_count': filtered_count,
        'satisfied_count': total_count - filtered_count,
        'max_length': args.max_length,
        'average_length': total_length / total_count
    }
    it_print('{total_lines} lines total, {filtered_count} lines longer than '
             '{max_length} symbols, {satisfied_count} lines in range, average '
             'line length {average_length:.2f}'.format(**params))

    if filtered_count == 0 or not args.verbose:
        return

    it_print('lines are listed below: ')
    for index, length, line in filtered_items:
        it_print('{lineno}/{length}: {line}'.format(**{
            'lineno': index + 1,
            'length': length,
            'line': line
        }))


if __name__ == '__main__':
    parser = get_parser()
    parser.add_argument('--file-path', '-f', help='file path', required=True)
    parser.add_argument('--split', '-s', action='store_true', default=False)
    parser.add_argument('--max-length', '-l', type=int, default=100,
                        help='max length of sentence')
    main(parse_arguments(parser))
