#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:08
import os
import subprocess

from options import parse_convert_arguments


def main(args):
    if args.output_path is None:
        setattr(args, 'output_path', '{}.tok'.format(args.file_path))
    script_path = os.path.dirname(os.path.abspath(__file__))
    kwargs = {
        'class_path': '{}/vendor/stanford-postagger-3.9.1.jar'.format(script_path),
        'main_class': 'edu.stanford.nlp.process.PTBTokenizer',
        'input': args.file_path,
        'output': args.output_path,
        'options': ' '.join([
            '-preserveLines',
            '-lowerCase'
        ])
    }
    cmd_str = 'java -cp {class_path} {main_class} {options} < {input} > {output}'.format(**kwargs)
    if args.verbose:
        print(cmd_str)
    subprocess.call(cmd_str, shell=True)


def cli_main():
    arguments = parse_convert_arguments()
    main(arguments)


if __name__ == '__main__':
    cli_main()
