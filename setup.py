#!/usr/bin/env python
from setuptools import setup

setup  (
    name        = 'simple_cpu',
    version     = '1.0.0',
    description = 'A simple CPU and assembler.',
    author = 'Travis Cunningham',
    author_email = 'travcunn@umail.iu.edu',
    url = 'https://github.com/travcunn/simple_cpu',
    license = 'MIT',
    packages  =  ['simple_cpu'],
    package_dir = {'simple_cpu' : 'simple_cpu'},
    entry_points = {
        'console_scripts': [
            'cpu = simple_cpu.__main__:cpu',
            'assembler = simple_cpu.__main__:assembler',
        ],
    },
    install_requires=[
        'pytest',
        'pytest-cov',
        'mock',
        'tox',
    ],
)
