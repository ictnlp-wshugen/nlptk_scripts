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
    name='hcnmt',
    version='2.8',
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
            'hcnmt-caller = hcnmt.bin.caller:cli_main',
            'hcnmt-quantize = hcnmt.bin.quantize:cli_main',
            'hcnmt-train = hcnmt.bin.train:cli_main',
            'hcnmt-test = hcnmt.bin.test:cli_main',
            'hcnmt-release = hcnmt.bin.release:cli_main',
            'hcnmt-bleu = hcnmt.bin.bleu:cli_main',
            'hcnmt-stop = hcnmt.bin.stop:cli_main',
        ],
    },
)
