# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-12 20:09
import argparse
import os


def get_project_root():
    return os.path.dirname(__file__)


def parse_arguments(parser):
    return parser.parse_known_args()[0]


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose', '-v', action='store_true', default=False,
        help='output command str'
    )
    return parser


def add_output_args_(parser):
    parser.add_argument(
        '--output-path', '-o', default=None,
        help='file path to save'
    )


def add_convert_args_(parser):
    parser.add_argument(
        '--file-path', '-f', required=True,
        help='file path to be convert'
    )
    parser.add_argument(
        '--encoding', '-e', default='utf8', choices=['utf8', 'gbk'],
        help='file encoding'
    )
    parser.add_argument(
        '--lang', '-l', default='zh', choices=['zh', 'en'],
        help='file encoding'
    )
    add_output_args_(parser)


def add_bilingual_args_(parser):
    parser.add_argument(
        '--source', '-s', required=True,
        help='source path'
    )
    parser.add_argument(
        '--target', '-t', required=True,
        help='target path'
    )


def get_convert_parser():
    parser = get_parser()
    add_convert_args_(parser)
    return parser


def parse_convert_arguments():
    parser = get_convert_parser()
    return parse_arguments(parser)
