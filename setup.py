#!/usr/bin/env python
# -*- coding: utf-8 -*-

import p4c_bm

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'p4-hlir',
    'Tenjin'
]

setup(
    name='p4c_bm',
    version=p4c_bm.__version__,
    description="Generates the JSON configuration for the behavioral-model, as well as the PD C/C++ files if needed",
    long_description=readme + '\n\n' + history,
    author="Antonin Bas",
    author_email='antonin@barefootnetworks.com',
    url='https://github.com/antoninbas/p4c_bm',
    packages=[
        'p4c_bm', 'p4c_bm.util',
    ],
    package_dir={'p4c_bm':
                 'p4c_bm'},
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
