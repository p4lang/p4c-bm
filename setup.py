#!/usr/bin/env python
# -*- coding: utf-8 -*-

import p4c_bm
import os
import sys

SETUP_PY_PATH = os.path.dirname(__file__)
SRC_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), "p4c_bm"))

from setuptools import setup

with open(os.path.join(SETUP_PY_PATH, 'README.rst')) as readme_file:
    readme = readme_file.read()

with open(os.path.join(SETUP_PY_PATH, 'HISTORY.rst')) as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open(os.path.join(SRC_PATH, "_version_str.py"), 'w') as version_f:
    version_f.write("# This file is auto-generated\n")
    version_f.write("version_str = '{}'\n".format(p4c_bm.__version__))

requirements = [
    # TODO: put package requirements here
    'p4-hlir',
    'Tenjin'
]

setup(
    name='p4c_bm',
    version=p4c_bm.__version__,
    description="Generates the JSON configuration for the behavioral-model",
    long_description=readme + '\n\n' + history,
    author="Antonin Bas",
    author_email='antonin@barefootnetworks.com',
    url='https://github.com/antoninbas/p4c_bm',
    packages=[
        'p4c_bm', 'p4c_bm.util',
    ],
    package_dir={'p4c_bm': SRC_PATH},
    include_package_data=True,
    install_requires=requirements,
    entry_points = {
        'console_scripts': [
            'p4c-bmv2=p4c_bm.__main__:main',
        ],
    },
    license="Apache",
    zip_safe=False,
    keywords='p4c_bm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests'
)
