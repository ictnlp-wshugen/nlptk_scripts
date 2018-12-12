#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 19:54
import argparse
import subprocess


def parse_arguments():
    parser = argparse.ArgumentParser('A2B')
    parser.add_argument('--file-path', '-f', required=True, help='file path to be a2b')
    parser.add_argument('--output-path', '-o', help='file path to save')
    parser.add_argument('--encoding', '-e', default='utf8', choices=['utf8', 'gbk'], help='file encoding')
    parser.add_argument('--lang', '-l', default='zh', choices=['zh', 'en'], help='file encoding')
    _args, _ = parser.parse_known_args()
    return _args


def main(args):
    if not hasattr(args, 'output_path'):
        setattr(args, 'output_path', '{}.tok'.format(getattr(args, 'file_path')))
    option = 'pre' if args.lang == 'zh' else 'all'
    cmd_fmt = './tra2b -{} {} {} {}'.format(args.encoding, option, args.file_path, args.output_path)
    subprocess.check_call(cmd_fmt)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
