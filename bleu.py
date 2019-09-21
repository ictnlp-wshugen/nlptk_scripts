#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-18 14:42
import os
import subprocess

from options import get_parser
from options import parse_arguments


def add_bleu_args_(parser):
    parser.add_argument(
        '--lowercase', '-lc', action='store_true', default=False,
        help='whether to use case insensitive bleu metric'
    )
    parser.add_argument(
        '--references', '-r', nargs='+', metavar='REF',
        help='references to calculate bleu'
    )
    parser.add_argument(
        '--candidate', '-c', required=True,
        help='candidate system translation to calculate bleu'
    )
    parser.add_argument(
        '--moses_scripts_path', '-msp',
        help='moses scripts path'
    )


def get_bleu_parser():
    parser = get_parser()
    add_bleu_args_(parser)
    return parser


def parse_bleu_arguments():
    return parse_arguments(get_bleu_parser())


def main(args):
    if args.moses_scripts_path is None:
        moses_decoder_home = os.environ.get('MOSES_DECODER_HOME', None)
        if moses_decoder_home is not None:
            setattr(args, 'moses_scripts_path', '{}/scripts'.format(moses_decoder_home))
    if not os.path.exists(args.moses_scripts_path):
        raise ValueError('moses_scripts_path not set')
    scripts_path = args.moses_scripts_path
    kwargs = {
        'multi_bleu_script': '{}/generic/multi-bleu.perl'.format(scripts_path),
        'references': ' '.join(args.references),
        'candidate': args.candidate,
        'options': ' '.join([
            '-lc' if args.lowercase else '',
        ])
    }
    cmd_str = '{multi_bleu_script} {options} {references} < {candidate}'.format(**kwargs)
    if args.verbose:
        print(cmd_str)
    subprocess.call(cmd_str, shell=True, stderr=open('/dev/null', mode='w'))


if __name__ == '__main__':
    arguments = parse_bleu_arguments()
    main(arguments)
