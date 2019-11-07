#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019/9/27 00:43
from easy_tornado import it_print
from easy_tornado.utils import file_exists
from easy_tornado.utils import file_lines
from easy_tornado.utils import open_files

from options import get_parser
from options import parse_arguments


def get_filter_parser():
    parser = get_parser()
    parser.add_argument(
        '--source-paths', '-sps', nargs='+', required=True,
        help='source file paths'
    )
    parser.add_argument(
        '--target-paths', '-tps', nargs='+', required=True,
        help='target file paths'
    )
    parser.add_argument(
        '--source-constraint', '-sc', metavar='EXPR', required=True,
        help='source constraint, tuple like (1,50)'
    )
    parser.add_argument(
        '--target-constraint', '-tc', metavar='EXPR', default=None,
        help='target constraint, tuple line source constraint or ratio '
             'like (0.5,1.5) which means the target length is between half '
             'and double size as source length'
    )
    parser.add_argument(
        '--source-logic-and', action='store_true', default=False,
        help='if set, then the criteria is satisfied if and only if all '
             'source path meet the requirement, else anyone of them'
    )
    parser.add_argument(
        '--target-logic-and', action='store_true', default=False,
        help='if set, then the criteria is satisfied if and only if all '
             'target path meet the requirement, else anyone of them'
    )
    return parser


def check_file_paths(file_paths):
    line_cnt = file_lines(file_paths[0])
    for file_path in file_paths:
        if not file_exists(file_path):
            it_print('file path [{}] does not exists.'.format(file_path))
            exit(0)
        cnt = file_lines(file_path)
        if line_cnt != cnt:
            it_print('file lines mismatch: {} => {}.'.format(line_cnt, cnt))
            exit(0)
    return line_cnt


def build_suffix(path, constraint):
    suffix = '-'.join([str(x) for x in constraint])
    return '{}.{}'.format(path, suffix)


def refine_constraint(constraint, ref_constraint=None):
    if constraint is None:
        assert ref_constraint is not None
        return ref_constraint

    if isinstance(constraint, str):
        constraint = eval(constraint)

    if any([isinstance(x, float) for x in constraint]):
        assert ref_constraint is not None
        start, end = constraint
        if isinstance(start, float):
            start *= ref_constraint[0]
        if isinstance(end, float):
            end *= ref_constraint[1]
        constraint = (int(start), int(end))

    return constraint


def check_constraint(lines, constraint, logic):
    lengths = [len(x.split()) for x in lines]
    if logic and not all([
        constraint[0] <= x <= constraint[1] for x in lengths
    ]):
        return False
    elif any([
        not constraint[0] <= x <= constraint[1] for x in lengths
    ]):
        return False
    return True


def main(args):
    src_paths, tgt_paths = args.source_paths, args.target_paths
    src_logic, tgt_logic = args.source_logic_and, args.target_logic_and
    src_constraint = refine_constraint(args.source_constraint)
    tgt_constraint = refine_constraint(args.target_constraint, src_constraint)

    # check paths
    src_cnt = check_file_paths(src_paths)
    tgt_cnt = check_file_paths(tgt_paths)
    if src_cnt != tgt_cnt:
        it_print('file lines mismatch: {} => {}.'.format(src_cnt, tgt_cnt))
        exit(0)

    t_src_paths = [build_suffix(x, src_constraint) for x in src_paths]
    t_tgt_paths = [build_suffix(x, tgt_constraint) for x in tgt_paths]
    with open_files(*src_paths, mode='r') as src_rfps, \
            open_files(*tgt_paths, mode='r') as tgt_rfps, \
            open_files(*t_src_paths, mode='w') as src_wfps, \
            open_files(*t_tgt_paths, mode='w') as tgt_wfps:
        line_cnt, kept_cnt = 0, 0
        while line_cnt < src_cnt:
            line_cnt += 1
            src_lines = [rfp.readline() for rfp in src_rfps]
            tgt_lines = [rfp.readline() for rfp in tgt_rfps]
            if not check_constraint(src_lines, src_constraint, src_logic):
                continue
            if not check_constraint(tgt_lines, tgt_constraint, tgt_logic):
                continue

            [wfp.write(line) for wfp, line in zip(src_wfps, src_lines)]
            [wfp.write(line) for wfp, line in zip(tgt_wfps, tgt_lines)]
            kept_cnt += 1

    it_print('kept lines: {}/{}'.format(kept_cnt, line_cnt))
    it_print('filter job done.')


def cli_main():
    _parser = get_filter_parser()
    _args = parse_arguments(_parser)
    main(_args)


if __name__ == '__main__':
    cli_main()
