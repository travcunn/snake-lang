#!/usr/bin/env python
from setuptools import setup

setup  (
    name        = 'The Snake Programming Language\'s Simple Virtual Program Assembler',
    version     = '1.0.2',
    description = 'A simple virtual machine and program assembler',
    author = 'Travis Cunningham',
    author_email = 'yoyo.monem22@gmail.com',
    url = 'https://github.com/yoyomonem/snake-lang',
    license = 'MIT',
    packages  =  ['snake'],
    package_dir = {'snake': 'snake'},
    entry_points = {
        'console_scripts': [
            'snakevm = snake.cli:vm',
            'assembler = snake.cli:assembler',
            'compiler = snake.cli:compiler',
        ],
    },
    install_requires=[
        'pytest',
        'pytest-cov',
        'mock',
        'tox',
    ],
)
