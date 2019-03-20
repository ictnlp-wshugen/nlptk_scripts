#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/11/27 22:23
import io

from options import get_parser
from options import parse_arguments


def main(args):
    with io.open(args.file_path, mode='r', encoding='utf-8') as rfp:
        lines = [x.strip() for x in rfp.readlines()]
        num_of_lines = len(lines)

    count, filtered = 0, []
    for i in range(num_of_lines):
        line = lines[i]
        criteria = len(line.split() if args.split else line) > args.max_length
        if criteria:
            count += 1
            filtered.append((i, line))
    params = {
        'num_of_lines': num_of_lines,
        'count': count,
        'max_length': args.max_length,
        'left': num_of_lines - count
    }
    print('{num_of_lines} lines total, {count} lines longer than {max_length} '
          'symbols, {left} lines in range'.format(**params))
    if count == 0 or not args.verbose:
        return

    print('lines are listed below: ')
    for item in filtered:
        print('{} -> {}'.format(item[0] + 1, item[1]))


if __name__ == '__main__':
    parser = get_parser()
    parser.add_argument('--file-path', '-f', help='file path', required=True)
    parser.add_argument('--split', '-s', action='store_true', default=False)
    parser.add_argument('--max-length', '-l', type=int, default=100, help='max length of sentence')
    main(parse_arguments(parser))
