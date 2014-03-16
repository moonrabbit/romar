#!/usr/bin/env python

import os
import sys

from setuptools import setup

readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')

setup(
    name='romar',
    version='0.0.1',
    url='https://github.com/moonrabbit/tojson',
    license='MIT',
    author='hpi',
    author_email='master@hpi.cc',
    description='Rows Marshaller',
    long_description=open(readme_path).read(),
    packages=[
        'romar'
    ],
    zip_safe=False,
    install_requires=[],
    tests_require=[
        'pytest',
    ],
    platforms='any',
)