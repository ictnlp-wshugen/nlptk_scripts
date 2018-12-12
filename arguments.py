# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:09
import argparse


def parse_convert_arguments():
    parser = argparse.ArgumentParser('Tokenize')
    parser.add_argument('--file-path', '-f', required=True, help='file path to be a2b')
    parser.add_argument('--output-path', '-o', help='file path to save')
    parser.add_argument('--encoding', '-e', default='utf8', choices=['utf8', 'gbk'], help='file encoding')
    parser.add_argument('--lang', '-l', default='zh', choices=['zh', 'en'], help='file encoding')
    _args, _ = parser.parse_known_args()
    return _args
