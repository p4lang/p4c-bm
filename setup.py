#!/usr/bin/env python

# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Antonin Bas (antonin@barefootnetworks.com)
#
#

# -*- coding: utf-8 -*-

import p4c_bm
import os
import sys

SETUP_PY_PATH = os.path.dirname(__file__)
SRC_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), "p4c_bm"))

from setuptools import setup
from setuptools.command.install import install

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

# pre-install hook
class CustomInstall(install):
    def run(self):
        in_path = os.path.join(SETUP_PY_PATH, 'p4c-bmv2.in')
        out_path = os.path.join(SETUP_PY_PATH, 'p4c-bmv2')
        with open(in_path, "r") as fin:
            with open(out_path, "w") as fout:
                for line in fin:
                    # we use the platform-dependent install path computed by
                    # setuptools
                    fout.write(line.replace('@pythondir@', self.install_lib))
        install.run(self)

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
    # entry_points={
    #     'console_scripts': [
    #         'p4c-bmv2=p4c_bm.__main__:main',
    #     ],
    # },
    scripts=['p4c-bmv2'],
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
    test_suite='tests',
    cmdclass={'install': CustomInstall},
)
