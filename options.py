# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:09
import argparse


def parse_arguments(parser):
    return parser.parse_known_args()[0]


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='output command str')
    return parser


def add_convert_args_(parser):
    parser.add_argument('-f', '--file-path', required=True, help='file path to be a2b')
    parser.add_argument('-o', '--output-path', help='file path to save')
    parser.add_argument('-e', '--encoding', default='utf8', choices=['utf8', 'gbk'], help='file encoding')
    parser.add_argument('-l', '--lang', default='zh', choices=['zh', 'en'], help='file encoding')


def get_convert_parser():
    parser = get_parser()
    add_convert_args_(parser)
    return parser


def parse_convert_arguments():
    return parse_arguments(get_convert_parser())
