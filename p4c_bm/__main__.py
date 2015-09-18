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

import argparse
import os
import sys
from p4_hlir.main import HLIR
import gen_json
import gen_pd
import json
from pkg_resources import resource_string


def get_parser():
    parser = argparse.ArgumentParser(description='p4c-bm arguments')
    parser.add_argument('source', metavar='source', type=str,
                        help='A source file to include in the P4 program.')
    parser.add_argument('--json', dest='json', type=str,
                        help='Dump the JSON representation to this file.',
                        required=False)
    parser.add_argument('--pd', dest='pd', type=str,
                        help='Generate PD C/C++ code for this P4 program'
                        ' in this directory. Directory must exist.',
                        required=False)
    parser.add_argument('--pd-from-json', action='store_true',
                        help='Generate PD from a JSON file, not a P4 file',
                        default=False)
    parser.add_argument('--p4-prefix', type=str,
                        help='P4 name use for API function prefix',
                        default="prog", required=False)
    return parser


def _validate_path(path):
    path = os.path.abspath(path)
    if not os.path.isdir(os.path.dirname(path)):
        print path, "is not a valid path because",\
            os.path.dirname(path), "is not a valid directory"
        sys.exit(1)
    if os.path.exists(path) and not os.path.isfile(path):
        print path, "exists and is not a file"
        sys.exit(1)
    return path


def _validate_dir(path):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        print path, "is not a valid directory"
        sys.exit(1)
    return path


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.json:
        path_json = _validate_path(args.json)

    from_json = False
    if args.pd:
        path_pd = _validate_dir(args.pd)
        if args.pd_from_json:
            if not os.path.exists(args.source):
                print "Invalid JSON source"
                sys.exit(1)
            from_json = True

    if from_json:
        with open(args.source, 'r') as f:
            json_dict = json.load(f)
    else:
        h = HLIR(args.source)
        h.add_preprocessor_args("-D__TARGET_BMV2__")
        # in addition to standard P4 primitives
        more_primitives = json.loads(
            resource_string(__name__, 'primitives.json')
        )
        h.add_primitives(more_primitives)
        if not h.build():
            print "Error while building HLIR"
            sys.exit(1)

        json_dict = gen_json.json_dict_create(h)

        if args.json:
            print "Generating json output to", path_json
            with open(path_json, 'w') as fp:
                json.dump(json_dict, fp, indent=4, separators=(',', ': '))

    if args.pd:
        print "Generating PD source files in", path_pd
        gen_pd.generate_pd_source(json_dict, path_pd, args.p4_prefix)


if __name__ == "__main__":  # pragma: no cover
    main()
