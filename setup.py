#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2019-06-12 15:43
import ssl

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name='nlptk',
    version='0.2',
    description='Natural Language Processing Toolkit',
    author='Wang Shugen',
    author_email='wangshugen@ict.ac.cn',
    url='https://github.com/ictnlp-wshugen',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7+',
        'Topic :: Scientific/Engineering :: Natural Language Processing',
    ],
    long_description=readme,
    packages=find_packages(include=['nlptk']),
    entry_points={
        'console_scripts': [
            'nlptk-a2b = nlptk.bin.a2b:cli_main',
            'nlptk-bleu = nlptk.bin.bleu:cli_main',
            'nlptk-bpe = nlptk.bin.bpe:cli_main',
            'nlptk-deblk = nlptk.bin.deblk:cli_main',
            'nlptk-debpe = nlptk.bin.debpe:cli_main',
            'nlptk-detok = nlptk.bin.detok:cli_main',
            'nlptk-fdup = nlptk.bin.fdup:cli_main',
            'nlptk-filter = nlptk.bin.filter:cli_main',
            'nlptk-flen = nlptk.bin.flen:cli_main',
            'nlptk-mapping = nlptk.bin.mapping:cli_main',
            'nlptk-shuffle = nlptk.bin.shuffle:cli_main',
            'nlptk-stat = nlptk.bin.stat:cli_main',
            'nlptk-tok = nlptk.bin.tok:cli_main',
        ],
    },
)
