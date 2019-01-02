# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-01-02 14:55
import io


def load_file_contents(file_path, pieces=True):
    with io.open(file_path, mode='r', encoding='utf-8') as rfp:
        contents = rfp.readlines()
        if not pieces:
            contents = ''.join([x.strip() for x in contents])
        return contents
