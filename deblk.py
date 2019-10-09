#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:58
import subprocess

from options import parse_convert_arguments


def main(args):
    if args.output_path is None:
        setattr(args, 'output_path', '{}.deblank'.format(args.file_path))
    kwargs = {
        'input': args.file_path,
        'output': args.output_path
    }
    cmd_str = "sed -r 's/ //g' {input} > {output}".format(**kwargs)
    if args.verbose:
        print(cmd_str)
    subprocess.call(cmd_str, shell=True)


def cli_main():
    _args = parse_convert_arguments()
    main(_args)


if __name__ == '__main__':
    cli_main()
