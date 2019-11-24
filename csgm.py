#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019/11/25 00:37
import re

from easy_tornado.utils import file_exists
from easy_tornado.utils import load_file_contents
from easy_tornado.utils import write_iterable_contents

from options import get_parser, parse_arguments


def get_csgm_parser():
    parser = get_parser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--to-sgm', action='store_true',
        help='palin2sgm, input plain text, output sgm format file'
    )
    group.add_argument(
        '--from-sgm', action='store_true',
        help='sgm2plain, input sgm format file, output plain text'
    )
    parser.add_argument(
        '--file-path', '-fp', metavar='FP', required=True,
        help='file path to be converted'
    )
    parser.add_argument(
        '--save-path', '-o', metavar='FP', default=None,
        help='file path to save at'
    )

    return parser


def parse_stat_arguments():
    parser = get_csgm_parser()
    return parse_arguments(parser)


def sgm2plain(sgm_path, plain_path=None, nop_if_exists=True):
    """
    Convert .sgm file to a plain text file, contents are sentence in the seg tag

    :param sgm_path: sgm file path
    :type sgm_path: str

    :param plain_path: target plain text file, if None, auto set to be the same as
    sgm_path but with '.sgm' replaced with '.plain' (optional)
    :type plain_path: str or None

    :param nop_if_exists: if the target plain file already exists, it does no
    operation, else the function overwrites it
    :type nop_if_exists: bool
    """
    sgm_suffix = '.sgm'
    if not sgm_path.endswith(sgm_suffix):
        raise ValueError('smg_path must be ended with {}'.format(sgm_suffix))

    if not file_exists(sgm_path):
        raise ValueError('sgm_path {} not exists'.format(sgm_path))

    if plain_path is None:
        pos = sgm_path.rfind(sgm_suffix)
        plain_path = sgm_path[:pos] + '.plain'

    if file_exists(plain_path) and nop_if_exists:
        return

    lines = [x.strip(' \r\n') for x in load_file_contents(sgm_path)]
    sentences = [
        re.sub(r'</?.*?>', '', x)
        for x in filter(lambda x: x.startswith('<seg'), lines)
    ]
    write_iterable_contents(plain_path, sentences)


def main(args):
    if args.from_sgm:
        sgm2plain(args.file_path, plain_path=args.save_path)
    elif args.to_sgm:
        raise NotImplementedError
    else:
        raise NotImplemented


def cli_main():
    main(parse_stat_arguments())


if __name__ == '__main__':
    cli_main()
