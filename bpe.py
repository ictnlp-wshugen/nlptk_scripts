#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:08
import os
import subprocess

from options import get_convert_parser
from options import parse_arguments


def add_bpe_args_(parser):
    parser.add_argument('-c', '--codes-path',
                        help='codes file path')
    parser.add_argument('-n', '--operations', type=int, default=32000,
                        help='num of operations')
    parser.add_argument('-k', '--keep-codes', action='store_true', default=False,
                        help='whether to keep codes file or not')
    parser.add_argument('-p', '--scripts-path', default=None,
                        help='subword-nmt path')


def get_bpe_parser():
    parser = get_convert_parser()
    add_bpe_args_(parser)
    return parser


def parse_bpe_arguments():
    return parse_arguments(get_bpe_parser())


def main(args):
    if args.output_path is None:
        setattr(args, 'output_path', '{}.bpe.{}'.format(args.file_path, args.operations))
    if args.codes_path is None:
        setattr(args, 'codes_path', '{}.bpe.codes'.format(args.file_path))
    else:
        setattr(args, 'keep_codes', True)

    if args.scripts_path is None:
        script_path = os.path.dirname(os.path.abspath(__file__))
        setattr(args, 'scripts_path', '{}/vendor/subword-nmt'.format(script_path))
    assert os.path.isdir(args.scripts_path), 'file path {} does not exist'.format(args.scripts_path)
    if os.path.isdir('{}/subword_nmt'.format(args.scripts_path)):
        setattr(args, 'scripts_path', '{}/subword_nmt'.format(args.scripts_path))

    kwargs = {
        'learn': '{}/learn_bpe.py'.format(args.scripts_path),
        'option': '-s',
        'operations': args.operations,
        'input': args.file_path,
        'output': args.codes_path
    }
    learn_bpe_cmd_str = '{learn} {option} {operations} < {input} > {output}'.format(**kwargs)
    if args.verbose:
        print(learn_bpe_cmd_str)
    subprocess.check_call(learn_bpe_cmd_str, shell=True)

    kwargs.update({
        'apply': '{}/apply_bpe.py'.format(args.scripts_path),
        'option': '-c',
        'codes': args.codes_path,
        'output': args.output_path
    })
    apply_bpe_cmd_str = '{apply} {option} {codes} < {input} > {output}'.format(**kwargs)
    if args.verbose:
        print(apply_bpe_cmd_str)
    subprocess.check_call(apply_bpe_cmd_str, shell=True)

    if not args.keep_codes:
        os.remove(args.codes_path)


if __name__ == '__main__':
    arguments = parse_bpe_arguments()
    main(arguments)
