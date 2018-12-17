# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:09
import argparse


def parse_arguments(parser):
    return parser.parse_known_args()[0]


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true', default=False, help='output command str')
    return parser


def add_convert_args_(parser):
    parser.add_argument('--file-path', '-f', required=True, help='file path to be a2b')
    parser.add_argument('--output-path', '-o', help='file path to save')
    parser.add_argument('--encoding', '-e', default='utf8', choices=['utf8', 'gbk'], help='file encoding')
    parser.add_argument('--lang', '-l', default='zh', choices=['zh', 'en'], help='file encoding')


def get_convert_parser():
    parser = get_parser()
    add_convert_args_(parser)
    return parser


def parse_convert_arguments():
    return parse_arguments(get_convert_parser())


def get_shuffle_parser():
    parser = get_convert_parser()
    parser.add_argument('--seed', '-s', type=int, default=195610, help='the PRNG seed for reproducibility')
    return parser


def parse_shuffle_arguments():
    return parse_arguments(get_shuffle_parser())


def add_bpe_args_(parser):
    parser.add_argument('--operations', '-n', type=int, default=32000, help='num of operations')
    parser.add_argument('--keep-codes', '-k', action='store_true', default=False,
                        help='whether to keep codes file or not')
    parser.add_argument('--scripts-path', '-p', default=None, help='subword-nmt path')


def get_bpe_parser():
    parser = get_convert_parser()
    add_bpe_args_(parser)
    return parser


def parse_bpe_arguments():
    return parse_arguments(get_bpe_parser())
