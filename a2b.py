#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 19:54
import os
import subprocess

from options import parse_convert_arguments


def main(args):
    if args.output_path is None:
        setattr(args, 'output_path', '{}.a2b'.format(args.file_path))
    script_path = os.path.dirname(os.path.abspath(__file__))
    kwargs = {
        'command': '{}/bin/tra2b'.format(script_path),
        'input': args.file_path,
        'output': args.output_path,
        'options': ' '.join([
            '-{}'.format(args.encoding),
            '-{}'.format('pre' if args.lang == 'zh' else 'all')
        ])
    }
    cmd_str = '{command} {options} {input} {output}'.format(**kwargs)
    if args.verbose:
        print(cmd_str)
    subprocess.check_call(cmd_str, shell=True)


def cli_main():
    _args = parse_convert_arguments()
    main(_args)


if __name__ == '__main__':
    cli_main()
