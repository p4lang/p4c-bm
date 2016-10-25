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

"""
test_p4c_bm
----------------------------------

Tests for `p4c_bm` module.
"""

import pytest
import os
import sys
import tempfile
import json
from pkg_resources import resource_string

from p4_hlir.main import HLIR

from p4c_bm import gen_json
from p4c_bm import gen_pd
from p4c_bm import __main__
from p4c_bm.util.topo_sorting import Graph
from p4c_bm.util.tenjin_wrapper import MacroPreprocessor

try:
    from p4_hlir_v1_1.main import HLIR as HLIRv1_1
    p4_v1_1_support = True
except ImportError:
    p4_v1_1_support = False


def list_p4_programs(with_negative=False):
    p4_programs_dir = "tests/p4_programs"
    files = os.listdir(p4_programs_dir)
    if with_negative:
        return [os.path.join(p4_programs_dir, f)
                for f in files if os.path.splitext(f)[1] == '.p4']
    else:
        return [os.path.join(p4_programs_dir, f)
                for f in files
                if os.path.splitext(f)[1] == '.p4' and "negative" not in f]


@pytest.mark.parametrize("input_p4", list_p4_programs(with_negative=True))
def test_gen_json(input_p4):
    assert os.path.exists(input_p4)
    h = HLIR(input_p4)
    more_primitives = json.loads(
        resource_string(__name__,
                        os.path.join('..', 'p4c_bm', 'primitives.json'))
    )
    h.add_primitives(more_primitives)
    assert h.build()
    if "negative" in input_p4:  # negative test => compiler must exit
        with pytest.raises(SystemExit):
            gen_json.json_dict_create(h)
    else:
        # using keep_pragmas == True to maximize coverage
        json_dict = gen_json.json_dict_create(h, keep_pragmas=True)
        assert json_dict


def list_files(dirname, ext):
    files = os.listdir(dirname)
    return [os.path.join(dirname, f)
            for f in files if os.path.splitext(f)[1] == ext]


@pytest.mark.parametrize(
    "input_aliases",
    list_files(os.path.join("tests", "testdata", "field_aliases"), ".txt"))
def test_gen_json_field_aliases(input_aliases):
    assert os.path.exists(input_aliases)

    input_p4 = os.path.join("tests", "p4_programs", "triv_eth.p4")
    assert os.path.exists(input_p4)
    h = HLIR(input_p4)
    assert h.build()

    if "error" in input_aliases:
        # make sure that the program exits
        with pytest.raises(SystemExit):
            gen_json.json_dict_create(h, input_aliases)
    else:
        assert "sample" in input_aliases
        json_dict = gen_json.json_dict_create(h, input_aliases)
        assert json_dict
        assert "field_aliases" in json_dict


@pytest.mark.skipif(not p4_v1_1_support, reason="No P4 v1.1 support")
@pytest.mark.parametrize(
    "input_p4",
    list_files(os.path.join("tests", "p4_programs", "v1_1"), ".p4"))
def test_v1_1_gen_json(input_p4):
    assert os.path.exists(input_p4)
    h = HLIRv1_1(input_p4)
    more_primitives = json.loads(
        resource_string(__name__,
                        os.path.join('..', 'p4c_bm', 'primitives_v1_1.json'))
    )
    h.add_primitives(more_primitives)
    assert h.build()
    json_dict = gen_json.json_dict_create(h, p4_v1_1=True)
    assert json_dict


@pytest.mark.parametrize("input_p4", list_p4_programs())
def test_gen_pd(input_p4, tmpdir):
    assert os.path.exists(input_p4)
    p = str(tmpdir)
    h = HLIR(input_p4)
    more_primitives = json.loads(
        resource_string(__name__,
                        os.path.join('..', 'p4c_bm', 'primitives.json'))
    )
    h.add_primitives(more_primitives)
    assert h.build()
    json_dict = gen_json.json_dict_create(h)
    assert json_dict
    gen_pd.generate_pd_source(json_dict, p, "pref")
    # now we check for all generated files
    inc_path = tmpdir.join("pd")
    src_path = tmpdir.join("src")
    assert inc_path.ensure_dir()
    assert src_path.ensure_dir()
    expected_inc_path = "p4c_bm/templates/pd/"
    expected_inc = [f for f in os.listdir(expected_inc_path)]
    expected_src_path = "p4c_bm/templates/src/"
    expected_src = [f for f in os.listdir(expected_src_path)]
    assert set(expected_inc) == set([f.basename for f in inc_path.listdir()])
    assert set(expected_src) == set([f.basename for f in src_path.listdir()])


def test_gen_of_pd(tmpdir):
    input_p4 = os.path.join("tests", "p4_programs", "l2_openflow.p4")
    assert os.path.exists(input_p4)
    p = str(tmpdir)
    h = HLIR(input_p4)
    more_primitives = json.loads(
        resource_string(__name__,
                        os.path.join('..', 'p4c_bm', 'primitives.json'))
    )
    h.add_primitives(more_primitives)
    assert h.build()
    json_dict = gen_json.json_dict_create(h)
    assert json_dict

    # hack the args
    from argparse import Namespace
    args = Namespace(plugin_list=["of"],
                     openflow_mapping_dir=os.path.join("tests", "of_mapping"),
                     openflow_mapping_mod="l2_openflow")

    gen_pd.generate_pd_source(json_dict, p, "pref", args)
    # now we check for all generated files
    of_path = tmpdir.join("plugin", "of")
    inc_path = of_path.join("inc")
    src_path = of_path.join("src")
    assert inc_path.ensure_dir()
    assert src_path.ensure_dir()
    expected_inc_path = "p4c_bm/plugin/of/inc"
    expected_inc = [f for f in os.listdir(expected_inc_path)]
    expected_src_path = "p4c_bm/plugin/of/src/"
    expected_src = [f for f in os.listdir(expected_src_path)]
    assert set(expected_inc) == set([f.basename for f in inc_path.listdir()])
    assert set(expected_src) == set([f.basename for f in src_path.listdir()])


def call_main(options):
    argv_save = list(sys.argv)
    sys.argv = ["p4c-bmv2"] + options
    sys.argc = len(sys.argv)
    try:
        __main__.main()
    except SystemExit as e:
        sys.argv = argv_save
        sys.argc = len(argv_save)
        return e.code
    return 0


def test_main(tmpdir):
    input_p4 = os.path.join("tests", "p4_programs", "triv_eth.p4")
    input_p4_v1_1 = os.path.join("tests", "p4_programs", "v1_1", "misc.p4")

    assert call_main(["-h"]) == 0
    assert call_main(["--help"]) == 0

    assert call_main(["-v"]) == 0
    assert call_main(["--version"]) == 0

    assert call_main([]) != 0

    assert call_main([input_p4]) == 0

    tmp_json = tempfile.mkstemp(suffix=".json")
    assert call_main([input_p4, "--json", tmp_json[1]]) == 0

    # v1.1
    assert call_main([input_p4_v1_1, "--json", tmp_json[1], "--p4-v1.1"]) == 0

    # not a file, but a directory
    assert call_main([input_p4, "--json", str(tmpdir)]) != 0

    # not a valid path
    assert call_main([input_p4, "--json", "plop/blah"]) != 0

    # not a directory
    assert call_main([input_p4, "--pd", tmp_json[1]]) != 0

    assert call_main([input_p4, "--pd", str(tmpdir)]) == 0

    assert call_main([input_p4, "--json", tmp_json[1],
                      "--pd", str(tmpdir)]) == 0

    # invalid input
    assert call_main([tmp_json[1]]) != 0

    # PD from JSON
    assert call_main([tmp_json[1], "--pd", str(tmpdir), "--pd-from-json"]) == 0

    # PD from JSON with invalid input
    assert call_main(["plop.json", "--pd", str(tmpdir), "--pd-from-json"]) != 0

    # preprocessor flag
    assert call_main([input_p4, "-DANTONIN_ON"]) == 0
    assert call_main([input_p4, "-I/home/"]) == 0

    # field aliases
    input_field_aliases = os.path.join("tests", "testdata",
                                       "field_aliases", "sample_1.txt")
    assert call_main([input_p4, "--field-aliases", input_field_aliases]) == 0

    # invalid option
    assert call_main([input_p4, "--nonsense"]) != 0

    # extra primitives file
    primitive_dir = os.path.join("tests", "testdata", "extra_primitives")
    primitive = os.path.join(primitive_dir, "unknown_primitive.json")
    primitive_1 = os.path.join(primitive_dir, "unknown_primitive_1.json")

    assert call_main([input_p4, "--primitives", "plop.json"]) != 0

    assert call_main([input_p4, "--primitives", primitive]) == 0

    assert call_main([input_p4, "--primitives", primitive,
                      "--primitives", primitive_1]) == 0

    os.remove(tmp_json[1])


def test_extra_primitives():
    primitive_dir = os.path.join("tests", "testdata", "extra_primitives")
    primitive_json = os.path.join(primitive_dir, "unknown_primitive.json")
    assert os.path.exists(primitive_json)

    input_p4 = os.path.join(primitive_dir, "unknown_primitive.p4")
    assert os.path.exists(input_p4)

    assert call_main([input_p4]) != 0

    assert call_main([input_p4, "--primitives", primitive_json]) == 0


def test_topo_sorting_good():
    g = Graph()
    nodes = []
    for i in xrange(5):
        g.add_node(i)
        nodes.append(g.get_node(i))
    edges = [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)]
    for n1, n2 in edges:
        nodes[n1].add_edge_to(nodes[n2])
    topo_sorting = g.produce_topo_sorting()
    valid = [[0, 1, 2, 3, 4],
             [0, 1, 3, 2, 4]]
    assert topo_sorting in valid


def test_topo_sorting_bad():
    g = Graph()
    nodes = []
    for i in xrange(3):
        g.add_node(i)
        nodes.append(g.get_node(i))
    edges = [(0, 1), (1, 2), (2, 1)]
    for n1, n2 in edges:
        nodes[n1].add_edge_to(nodes[n2])
    topo_sorting = g.produce_topo_sorting()
    assert topo_sorting is None


def test_tenjin_macro_preprocessor():
    mp = MacroPreprocessor()
    input_ = """
//:: #define METER_STUFF
//:: for i in xrange(10):
//::   if True:
print "YES!"
//::   #endif
//:: #endfor
//:: #enddefine
//::   #expand METER_STUFF 2
"""
    expected_output = """
//::   for i in xrange(10):
//::     if True:
  print "YES!"
//::     #endif
//::   #endfor
"""
    output = mp.__call__(input_)
    assert expected_output.strip() == output.strip()
