#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 19:54
import subprocess

from arguments import parse_convert_arguments


def main(args):
    if args.output_path is None:
        setattr(args, 'output_path', '{}.tok'.format(getattr(args, 'file_path')))
    option = 'pre' if args.lang == 'zh' else 'all'
    cmd_str = './tra2b -{} {} {} {}'.format(args.encoding, option, args.file_path, args.output_path)
    if args.verbose:
        print(cmd_str)
    subprocess.check_call(cmd_str, shell=True)


if __name__ == '__main__':
    arguments = parse_convert_arguments()
    main(arguments)
