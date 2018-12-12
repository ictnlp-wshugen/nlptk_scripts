# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:09
import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', type=bool, default=False, help='output command str')
    return parser


def get_convert_parser():
    parser = get_parser()
    add_convert_args_(parser)
    return parser


def get_bpe_parser():
    parser = get_convert_parser()
    add_bpe_args_(parser)
    return parser


def add_bpe_args_(parser):
    parser.add_argument('--operations', '-n', type=int, default=32000, help='num of operations')
    parser.add_argument('--keep-codes', '-k', type=bool, default=False, help='whether to keep codes file or not')


def add_convert_args_(parser):
    parser.add_argument('--file-path', '-f', required=True, help='file path to be a2b')
    parser.add_argument('--output-path', '-o', help='file path to save')
    parser.add_argument('--encoding', '-e', default='utf8', choices=['utf8', 'gbk'], help='file encoding')
    parser.add_argument('--lang', '-l', default='zh', choices=['zh', 'en'], help='file encoding')


def parse_convert_arguments():
    parser = get_convert_parser()
    return parser.parse_known_args()[0]


def parse_bpe_arguments():
    parser = get_bpe_parser()
    return parser.parse_known_args()[0]
