#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:08
import os
import subprocess

from options import parse_bpe_arguments


def main(args):
    if args.output_path is None:
        setattr(args, 'output_path', '{}.bpe.{}'.format(args.file_path, args.operations))
    setattr(args, 'codes_path', '{}.bpe.codes'.format(args.file_path))
    if args.scripts_path is None:
        script_path = os.path.dirname(os.path.abspath(__file__))
        setattr(args, 'scripts_path', '{}/subword_nmt'.format(script_path))
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
