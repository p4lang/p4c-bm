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

from collections import defaultdict, OrderedDict
import p4_hlir.hlir.p4 as p4
from util.topo_sorting import Graph
import re
from copy import copy
import logging
import sys


_STATIC_VARS = []


logging.basicConfig()
logger = logging.getLogger(__name__)


def LOG_CRITICAL(msg, *args, **kwargs):  # pragma: no cover
    logger.critical(msg, *args, **kwargs)
    logging.shutdown()
    sys.exit(1)


def LOG_WARNING(msg, *args, **kwargs):  # pragma: no cover
    logger.warning(msg, *args, **kwargs)


def LOG_INFO(msg, *args, **kwargs):  # pragma: no cover
    logger.info(msg, *args, **kwargs)


def static_var(varname, value):
    def decorate(func):
        _STATIC_VARS.append((func, varname, value))
        setattr(func, varname, copy(value))
        return func
    return decorate


def reset_static_vars():
    for(func, varname, value) in _STATIC_VARS:
        setattr(func, varname, copy(value))


def header_length_exp_format(p4_expression, fields):

    def find_idx(name):
        for idx, field in enumerate(fields):
            if name == field:
                return idx
        return -1

    if type(p4_expression) is p4.p4_expression:
        new_expr = p4.p4_expression(op=p4_expression.op)
        new_expr.left = header_length_exp_format(p4_expression.left, fields)
        new_expr.right = header_length_exp_format(p4_expression.right, fields)
        return new_expr
    elif type(p4_expression) is str:  # refers to field in same header
        idx = find_idx(p4_expression)
        assert(idx >= 0)
        # trick so that dump_expression uses local for this
        return p4.p4_signature_ref(idx)
    else:
        return p4_expression


def dump_header_types(json_dict, hlir):
    header_types = []
    id_ = 0
    for name, p4_header in hlir.p4_headers.items():
        header_type_dict = OrderedDict()
        header_type_dict["name"] = name
        header_type_dict["id"] = id_
        id_ += 1

        fixed_width = 0
        for field, bit_width in p4_header.layout.items():
            if bit_width != p4.P4_AUTO_WIDTH:
                fixed_width += bit_width

        fields = []
        for field, bit_width in p4_header.layout.items():
            if bit_width == p4.P4_AUTO_WIDTH:
                bit_width = "*"
            fields.append([field, bit_width])
        header_type_dict["fields"] = fields

        length_exp = None
        max_length = None
        if p4_header.flex_width:
            length_exp = header_length_exp_format(p4_header.length,
                                                  zip(*fields)[0])
            # bm expects a length in bits
            length_exp = p4.p4_expression(length_exp, "*", 8)
            length_exp = p4.p4_expression(length_exp, "-", fixed_width)
            length_exp = dump_expression(length_exp)
            max_length = p4_header.max_length
        header_type_dict["length_exp"] = length_exp
        header_type_dict["max_length"] = max_length

        header_types.append(header_type_dict)

    json_dict["header_types"] = header_types


def dump_headers(json_dict, hlir):
    headers = []
    id_ = 0
    for name, p4_header_instance in hlir.p4_header_instances.items():
        if p4_header_instance.virtual:
            continue
        header_instance_dict = OrderedDict()
        header_instance_dict["name"] = name
        header_instance_dict["id"] = id_
        id_ += 1
        header_instance_dict["header_type"] =\
            p4_header_instance.header_type.name
        header_instance_dict["metadata"] = p4_header_instance.metadata
        headers.append(header_instance_dict)

    json_dict["headers"] = headers


def dump_header_stacks(json_dict, hlir):
    header_stacks = []

    class HST:
        def __init__(self, name, size, header_type):
            self.name = name
            self.size = size
            self.header_type = header_type
            self.ids = []

        def add_header_id(self, header_id):
            self.ids.append(header_id)

    my_stacks = {}
    header_id = 0
    for name, p4_header_instance in hlir.p4_header_instances.items():
        if p4_header_instance.virtual:
            continue
        header_id += 1
        if p4_header_instance.max_index is None:
            continue
        base_name = p4_header_instance.base_name
        if base_name not in my_stacks:
            my_stacks[base_name] = HST(base_name,
                                       p4_header_instance.max_index + 1,
                                       p4_header_instance.header_type.name)
        my_stacks[base_name].add_header_id(header_id - 1)

    id_ = 0
    for base_name, hst in my_stacks.items():
        header_stack_dict = OrderedDict()
        header_stack_dict["name"] = base_name
        header_stack_dict["id"] = id_
        id_ += 1
        header_stack_dict["size"] = hst.size
        header_stack_dict["header_type"] = hst.header_type
        header_stack_dict["header_ids"] = hst.ids
        header_stacks.append(header_stack_dict)

    json_dict["header_stacks"] = header_stacks


def format_field_ref(p4_field):
    header = p4_field.instance
    if not header.virtual:
        return [header.name, p4_field.name]
    else:
        return [header.base_name, p4_field.name]


def build_match_value(widths, value):
    res = ""
    for width in reversed(widths):
        mask = (1 << width) - 1
        val = value & mask
        num_bytes = (width + 7) / 8
        res = "{0:0{1}x}".format(val, 2 * num_bytes) + res
        value = value >> width
    return "0x" + res


def dump_parsers(json_dict, hlir):
    parsers = []
    parser_id = 0

    # only one parser in P4 right now, choose name "parser" for it
    parser_dict = OrderedDict()
    parser_dict["name"] = "parser"
    parser_dict["id"] = parser_id
    parser_id += 1
    # the init parse state is always "start"
    parser_dict["init_state"] = "start"
    parse_states = []

    parse_state_id = 0
    for name, p4_parse_state in hlir.p4_parse_states.items():
        parse_state_dict = OrderedDict()
        parse_state_dict["name"] = name
        parse_state_dict["id"] = parse_state_id
        parse_state_id += 1

        parser_ops = []
        for parser_op in p4_parse_state.call_sequence:
            parser_op_dict = OrderedDict()
            op_type = parser_op[0]
            parameters = []
            if op_type == p4.parse_call.extract:
                parser_op_dict["op"] = "extract"
                header = parser_op[1]
                param_dict = OrderedDict()
                if header.virtual:
                    param_dict["type"] = "stack"
                    param_dict["value"] = header.base_name
                else:
                    param_dict["type"] = "regular"
                    param_dict["value"] = header.name
                parameters.append(param_dict)
            elif op_type == p4.parse_call.set:
                parser_op_dict["op"] = "set"
                dest_field, src = parser_op[1], parser_op[2]
                assert(type(dest_field) is p4.p4_field and
                       "parser assignment target should be a field")
                dest_dict = OrderedDict()
                src_dict = OrderedDict()
                dest_dict["type"] = "field"
                dest_dict["value"] = format_field_ref(dest_field)
                parameters.append(dest_dict)
                if type(src) is int or type(src) is long:
                    src_dict["type"] = "hexstr"
                    src_dict["value"] = hex(src)
                elif type(src) is p4.p4_field:
                    src_dict["type"] = "field"
                    src_dict["value"] = format_field_ref(src)
                elif type(src) is tuple:
                    src_dict["type"] = "lookahead"
                    src_dict["value"] = list(src)
                elif type(src) is p4.p4_expression:
                    src_dict["type"] = "expression"
                    src_dict["value"] = dump_expression(src)
                else:  # pragma: no cover
                    LOG_CRITICAL("invalid src type for set_metadata: %s",
                                 type(src))
                parameters.append(src_dict)
            else:  # pragma: no cover
                LOG_CRITICAL("invalid parser operation: %s", op_type)

            parser_op_dict["parameters"] = parameters
            parser_ops.append(parser_op_dict)

        parse_state_dict["parser_ops"] = parser_ops

        transition_key = []
        field_widths = []
        for switch_ref in p4_parse_state.branch_on:
            switch_ref_dict = OrderedDict()
            if type(switch_ref) is p4.p4_field:
                field_widths.append(switch_ref.width)
                header = switch_ref.instance
                if header.virtual:
                    switch_ref_dict["type"] = "stack_field"
                else:
                    switch_ref_dict["type"] = "field"
                switch_ref_dict["value"] = format_field_ref(switch_ref)
            elif type(switch_ref) is tuple:
                field_widths.append(switch_ref[1])
                switch_ref_dict["type"] = "lookahead"
                switch_ref_dict["value"] = list(switch_ref)
            else:  # pragma: no cover
                LOG_CRITICAL("not supported")
            transition_key.append(switch_ref_dict)
        parse_state_dict["transition_key"] = transition_key

        transitions = []
        for branch_case, next_state in p4_parse_state.branch_to.items():
            transition_dict = OrderedDict()
            value, mask = None, None
            if branch_case == p4.P4_DEFAULT:
                value = "default"
            elif type(branch_case) is int:
                value = build_match_value(field_widths, branch_case)
            elif type(branch_case) is tuple:
                value, mask = (build_match_value(field_widths, branch_case[0]),
                               build_match_value(field_widths, branch_case[1]))
            else:  # pragma: no cover
                LOG_CRITICAL("value sets not supported in parser")

            transition_dict["value"] = value
            transition_dict["mask"] = mask

            if isinstance(next_state, p4.p4_parse_state):
                transition_dict["next_state"] = next_state.name
            else:
                # we do not support control flows here anymore
                transition_dict["next_state"] = None

            transitions.append(transition_dict)

        parse_state_dict["transitions"] = transitions

        parse_states.append(parse_state_dict)

    parser_dict["parse_states"] = parse_states

    parsers.append(parser_dict)

    json_dict["parsers"] = parsers


def process_forced_header_ordering(hlir, ordering):
    p4_ordering = []
    for hdr_name in ordering:
        if hdr_name in hlir.p4_header_instances:
            p4_ordering.append(hlir.p4_header_instances[hdr_name])
        elif hdr_name + "[0]" in hlir.p4_header_instances:
            hdr_0 = hlir.p4_header_instances[hdr_name + "[0]"]
            for index in xrange(hdr_0.max_index + 1):
                indexed_name = hdr_name + "[" + str(index) + "]"
                p4_ordering.append(hlir.p4_header_instances[indexed_name])
        else:
            return None
    return p4_ordering


def produce_parser_topo_sorting(hlir):
    header_graph = Graph()

    def walk_rec(hlir, parse_state, prev_hdr_node, tag_stacks_index, visited):
        assert(isinstance(parse_state, p4.p4_parse_state))
        for call in parse_state.call_sequence:
            call_type = call[0]
            if call_type == p4.parse_call.extract:
                hdr = call[1]

                if hdr.virtual:
                    base_name = hdr.base_name
                    current_index = tag_stacks_index[base_name]
                    if current_index > hdr.max_index:
                        return
                    tag_stacks_index[base_name] += 1
                    name = base_name + "[%d]" % current_index
                    hdr = hlir.p4_header_instances[name]
                # takes care of loops in parser (e.g. for TLV parsing)
                elif parse_state in visited:
                    return

                if hdr not in header_graph:
                    header_graph.add_node(hdr)
                hdr_node = header_graph.get_node(hdr)

                if prev_hdr_node:
                    prev_hdr_node.add_edge_to(hdr_node)
                else:
                    header_graph.root = hdr
                prev_hdr_node = hdr_node

        for branch_case, next_state in parse_state.branch_to.items():
            if not next_state:
                continue
            if not isinstance(next_state, p4.p4_parse_state):
                continue
            walk_rec(hlir, next_state, prev_hdr_node,
                     tag_stacks_index.copy(), visited | {parse_state})

    start_state = hlir.p4_parse_states["start"]
    for pragma in start_state._pragmas:
        try:
            words = pragma.split()
            if words[0] != "header_ordering":
                continue
        except:  # pragma: no cover
            continue
        sorting = process_forced_header_ordering(hlir, words[1:])
        if sorting is None:  # pragma: no cover
            LOG_CRITICAL("invalid 'header_ordering' pragma")
        return sorting

    walk_rec(hlir, start_state, None, defaultdict(int), set())

    header_topo_sorting = header_graph.produce_topo_sorting()
    if header_topo_sorting is None:  # pragma: no cover
        LOG_CRITICAL("could not produce topo sorting because of cycles")

    return header_topo_sorting


def dump_deparsers(json_dict, hlir):
    deparsers = []
    deparser_id = 0

    # for now, only one deparser, called "deparser" and inferred from the one
    # parser
    deparser_dict = OrderedDict()
    deparser_dict["name"] = "deparser"
    deparser_dict["id"] = deparser_id
    deparser_id += 1

    header_topo_sorting = produce_parser_topo_sorting(hlir)
    deparser_order = [hdr.name for hdr in header_topo_sorting]
    deparser_dict["order"] = deparser_order

    deparsers.append(deparser_dict)

    json_dict["deparsers"] = deparsers


def dump_expression(p4_expression):
    if p4_expression is None:
        return None
    expression_dict = OrderedDict()
    if type(p4_expression) is int:
        expression_dict["type"] = "hexstr"
        expression_dict["value"] = hex(p4_expression)
    elif type(p4_expression) is bool:
        expression_dict["type"] = "bool"
        expression_dict["value"] = p4_expression
    elif type(p4_expression) is p4.p4_header_instance:
        expression_dict["type"] = "header"
        expression_dict["value"] = p4_expression.name
    elif type(p4_expression) is p4.p4_field:
        expression_dict["type"] = "field"
        expression_dict["value"] = format_field_ref(p4_expression)
    elif type(p4_expression) is p4.p4_signature_ref:
        expression_dict["type"] = "local"
        expression_dict["value"] = p4_expression.idx
    else:
        expression_dict["type"] = "expression"
        expression_dict["value"] = OrderedDict()
        expression_dict["value"]["op"] = p4_expression.op
        expression_dict["value"]["left"] =\
            dump_expression(p4_expression.left)
        expression_dict["value"]["right"] =\
            dump_expression(p4_expression.right)

        # expression_dict["op"] = p4_expression.op
        # expression_dict["left"] = dump_expression(p4_expression.left)
        # expression_dict["right"] = dump_expression(p4_expression.right)
    return expression_dict


def get_nodes(pipe_ptr, node_set):
    if pipe_ptr is None:
        return
    if pipe_ptr in node_set:
        return
    node_set.add(pipe_ptr)
    for next_node in pipe_ptr.next_.values():
        get_nodes(next_node, node_set)


match_types_map = {
    p4.p4_match_type.P4_MATCH_EXACT: "exact",
    p4.p4_match_type.P4_MATCH_LPM: "lpm",
    p4.p4_match_type.P4_MATCH_TERNARY: "ternary",
    p4.p4_match_type.P4_MATCH_VALID: "valid"
}


def get_table_match_type(p4_table):
    match_types = []
    for _, m_type, _ in p4_table.match_fields:
        match_types.append(match_types_map[m_type])

    if len(match_types) == 0:
        match_type = "exact"
    elif "ternary" in match_types:
        match_type = "ternary"
    elif match_types.count("lpm") >= 2:  # pragma: no cover
        LOG_CRITICAL("cannot have 2 different lpm matches in a single table")
    elif "lpm" in match_types:
        match_type = "lpm"
    else:
        # that includes the case when we only have one valid match and
        # nothing else
        match_type = "exact"

    return match_type


def get_table_type(p4_table):
    act_prof = p4_table.action_profile
    if act_prof is None:
        table_type = "simple"
    elif act_prof.selector is None:
        table_type = "indirect"
    else:
        table_type = "indirect_ws"
    return table_type


@static_var("pipeline_id", 0)
@static_var("table_id", 0)
@static_var("condition_id", 0)
def dump_one_pipeline(name, pipe_ptr, hlir):
    def get_table_name(p4_table):
        if not p4_table:
            return None
        return p4_table.name

    def table_has_counters(p4_table):
        for name, counter in hlir.p4_counters.items():
            if counter.binding == (p4.P4_DIRECT, p4_table):
                return True
        return False

    pipeline_dict = OrderedDict()
    pipeline_dict["name"] = name
    pipeline_dict["id"] = dump_one_pipeline.pipeline_id
    dump_one_pipeline.pipeline_id += 1
    pipeline_dict["init_table"] = get_table_name(pipe_ptr)

    node_set = set()
    get_nodes(pipe_ptr, node_set)

    tables = []
    for name, table in hlir.p4_tables.items():
        if table not in node_set:
            continue

        table_dict = OrderedDict()
        table_dict["name"] = name
        table_dict["id"] = dump_one_pipeline.table_id
        dump_one_pipeline.table_id += 1

        match_type = get_table_match_type(table)
        table_dict["match_type"] = match_type

        table_dict["type"] = get_table_type(table)
        if table_dict["type"] == "indirect" or\
           table_dict["type"] == "indirect_ws":
            # name needed for PD generation
            table_dict["act_prof_name"] = table.action_profile.name
        if table_dict["type"] == "indirect_ws":
            p4_selector = table.action_profile.selector
            selector = OrderedDict()
            selector["algo"] = p4_selector.selection_key.algorithm
            elements = []
            assert(len(p4_selector.selection_key.input) == 1)
            for field in p4_selector.selection_key.input[0].fields:
                element_dict = OrderedDict()
                if type(field) is not p4.p4_field:  # pragma: no cover
                    LOG_CRITICAL("only fields supported in field lists")
                element_dict["type"] = "field"
                element_dict["value"] = format_field_ref(field)
                elements.append(element_dict)
            selector["input"] = elements
            table_dict["selector"] = selector

        table_dict["max_size"] = table.max_size if table.max_size else 16384

        table_dict["with_counters"] = table_has_counters(table)

        table_dict["support_timeout"] = table.support_timeout

        key = []
        for field_ref, m_type, mask in table.match_fields:
            key_field = OrderedDict()
            if mask:  # pragma: no cover
                LOG_CRITICAL("mask not supported for match fields")
            match_type = match_types_map[m_type]
            key_field["match_type"] = match_type
            if(match_type == "valid"):
                assert(type(field_ref) is p4.p4_header_instance)
                key_field["target"] = field_ref.name
            else:
                key_field["target"] = format_field_ref(field_ref)
            key.append(key_field)
        table_dict["key"] = key

        table_dict["actions"] = [a.name for a in table.actions]

        next_tables = OrderedDict()
        if "hit" in table.next_:
            next_tables["__HIT__"] = get_table_name(table.next_["hit"])
            next_tables["__MISS__"] = get_table_name(table.next_["miss"])
        else:
            for a, nt in table.next_.items():
                next_tables[a.name] = get_table_name(nt)
        table_dict["next_tables"] = next_tables

        table_dict["default_action"] = None

        tables.append(table_dict)

    pipeline_dict["tables"] = tables

    conditionals = []
    for name, cnode in hlir.p4_conditional_nodes.items():
        if cnode not in node_set:
            continue

        conditional_dict = OrderedDict()
        conditional_dict["name"] = name
        conditional_dict["id"] = dump_one_pipeline.condition_id
        dump_one_pipeline.condition_id += 1
        conditional_dict["expression"] = dump_expression(cnode.condition)

        conditional_dict["true_next"] = get_table_name(cnode.next_[True])
        conditional_dict["false_next"] = get_table_name(cnode.next_[False])

        conditionals.append(conditional_dict)

    pipeline_dict["conditionals"] = conditionals

    return pipeline_dict


def dump_pipelines(json_dict, hlir):
    pipelines = []

    # 2 pipelines: ingress and egress
    assert(len(hlir.p4_ingress_ptr) == 1 and "only one ingress ptr supported")
    ingress_ptr = hlir.p4_ingress_ptr.keys()[0]
    pipelines.append(dump_one_pipeline("ingress", ingress_ptr, hlir))

    egress_ptr = hlir.p4_egress_ptr
    pipelines.append(dump_one_pipeline("egress", egress_ptr, hlir))

    json_dict["pipelines"] = pipelines


def index_OrderedDict(self, kf):
    idx = 0
    for k, v in self.items():
        if(k == kf):
            return idx
        idx += 1


OrderedDict.index = index_OrderedDict


# TODO: unify with method below
@static_var("ids", {})
def field_list_to_learn_id(p4_field_list):
    ids = field_list_to_learn_id.ids
    if p4_field_list in ids:
        return ids[p4_field_list]
    idx = len(ids) + 1
    ids[p4_field_list] = idx
    return idx


@static_var("ids", {})
def field_list_to_id(p4_field_list):
    ids = field_list_to_id.ids
    if p4_field_list in ids:
        return ids[p4_field_list]
    idx = len(ids) + 1
    ids[p4_field_list] = idx
    return idx


def dump_actions(json_dict, hlir):
    actions = []
    action_id = 0

    table_actions_set = set()
    for _, table in hlir.p4_tables.items():
        for action in table.actions:
            table_actions_set.add(action)

    for action in table_actions_set:
        action_dict = OrderedDict()
        action_dict["name"] = action.name
        action_dict["id"] = action_id
        action_id += 1

        runtime_data = []
        param_with_bit_widths = OrderedDict()
        for param, width in zip(action.signature, action.signature_widths):
            if not width:  # pragma: no cover
                LOG_CRITICAL("unused parameter in action def")
            param_with_bit_widths[param] = width

            param_dict = OrderedDict()
            param_dict["name"] = param
            param_dict["bitwidth"] = width
            runtime_data.append(param_dict)
        action_dict["runtime_data"] = runtime_data

        primitives = []
        for call in action.flat_call_sequence:
            primitive_dict = OrderedDict()

            primitive_name = call[0].name
            primitive_dict["op"] = primitive_name

            primitive_args = []
            for arg in call[1]:
                arg_dict = OrderedDict()
                if type(arg) is int or type(arg) is long:
                    arg_dict["type"] = "hexstr"
                    arg_dict["value"] = hex(arg)
                elif type(arg) is p4.p4_field:
                    arg_dict["type"] = "field"
                    arg_dict["value"] = format_field_ref(arg)
                elif type(arg) is p4.p4_header_instance:
                    arg_dict["type"] = "header"
                    arg_dict["value"] = arg.name
                elif type(arg) is p4.p4_signature_ref:
                    arg_dict["type"] = "runtime_data"
                    arg_dict["value"] = arg.idx
                elif type(arg) is p4.p4_field_list:
                    # hack for generate_digest calls
                    if primitive_name == "generate_digest":
                        id_ = field_list_to_learn_id(arg)
                    elif "clone" in primitive_name:
                        id_ = field_list_to_id(arg)
                    arg_dict["type"] = "hexstr"
                    arg_dict["value"] = hex(id_)
                elif type(arg) is p4.p4_field_list_calculation:
                    arg_dict["type"] = "calculation"
                    arg_dict["value"] = arg.name
                elif type(arg) is p4.p4_meter:
                    arg_dict["type"] = "meter_array"
                    arg_dict["value"] = arg.name
                elif type(arg) is p4.p4_counter:
                    arg_dict["type"] = "counter_array"
                    arg_dict["value"] = arg.name
                elif type(arg) is p4.p4_register:
                    arg_dict["type"] = "register_array"
                    arg_dict["value"] = arg.name
                elif type(arg) is p4.p4_expression:
                    arg_dict["type"] = "expression"
                    arg_dict["value"] = dump_expression(arg)
                else:  # pragma: no cover
                    LOG_CRITICAL("action arg type is not supported: ",
                                 type(arg))

                if primitive_name in {"push", "pop"} and\
                   arg_dict["type"] == "header":
                    arg_dict["type"] = "header_stack"
                    arg_dict["value"] = re.sub(r'\[.*\]', '', arg_dict["value"])

                primitive_args.append(arg_dict)
            primitive_dict["parameters"] = primitive_args

            primitives.append(primitive_dict)

        action_dict["primitives"] = primitives

        actions.append(action_dict)

    json_dict["actions"] = actions


def dump_calculations(json_dict, hlir):
    calculations = []
    id_ = 0
    for name, p4_calculation in hlir.p4_field_list_calculations.items():
        calc_dict = OrderedDict()
        calc_dict["name"] = name
        calc_dict["id"] = id_
        id_ += 1
        inputs = p4_calculation.input
        assert(len(inputs) == 1)
        input_ = inputs[0]
        my_input = []
        last_header = None
        for field in input_.fields:
            if type(field) is p4.p4_field:
                field_dict = OrderedDict()
                field_dict["type"] = "field"
                field_dict["value"] = format_field_ref(field)
                last_header = field.instance
                my_input.append(field_dict)
            elif type(field) is p4.p4_sized_integer:
                field_dict = OrderedDict()
                if field.width % 8 != 0:  # pragma: no cover
                    LOG_CRITICAL(
                        "p4 sized integers' width needs to be a multiple of 8"
                    )
                # recycling function I wrote for parser
                # TODO: find a better name for it
                s = build_match_value([field.width / 8], field)
                field_dict["type"] = "hexstr"
                field_dict["value"] = s
                field_dict["bitwidth"] = field.width
                my_input.append(field_dict)
            elif field is p4.P4_PAYLOAD:
                # this case is treated in a somewhat special way. We look at the
                # header topo sorting and add them to the calculation
                # input. This is not exactly what is described in P4. This is
                # obviously not optimal but payload needs to change in P4 anyway
                # (it is incorrect).
                topo_sorting = produce_parser_topo_sorting(hlir)
                for i, h in enumerate(topo_sorting):
                    if h == last_header:
                        break
                for h in topo_sorting[(i + 1):]:
                    field_dict = OrderedDict()
                    field_dict["type"] = "header"
                    field_dict["value"] = h.name
                    my_input.append(field_dict)
                field_dict = OrderedDict()
                field_dict["type"] = "payload"
                my_input.append(field_dict)
            else:  # pragma: no cover
                LOG_CRITICAL("field lists can only include fields")
        calc_dict["input"] = my_input
        calc_dict["algo"] = p4_calculation.algorithm
        # calc_dict["output_width"] = calculation.output_width

        calculations.append(calc_dict)

    json_dict["calculations"] = calculations


def dump_checksums(json_dict, hlir):
    checksums = []
    id_ = 0
    for name, p4_header_instance in hlir.p4_header_instances.items():
        for field_instance in p4_header_instance.fields:
            field_ref = format_field_ref(field_instance)
            field_name = '.'.join(field_ref)
            for calculation in field_instance.calculation:
                checksum_dict = OrderedDict()
                type_, calc, if_cond = calculation
                assert(calc.output_width == field_instance.width)
                checksum_dict["name"] = field_name
                checksum_dict["id"] = id_
                id_ += 1
                checksum_dict["target"] = field_ref
                checksum_dict["type"] = "generic"
                checksum_dict["calculation"] = calc.name
                checksums.append(checksum_dict)
                break

    json_dict["checksums"] = checksums


# TODO: deprecate this function and merge with the one below
def dump_learn_lists(json_dict, hlir):
    learn_lists = []

    learn_list_ids = field_list_to_learn_id.ids
    for p4_field_list, id_ in learn_list_ids.items():
        learn_list_dict = OrderedDict()
        learn_list_dict["id"] = id_
        learn_list_dict["name"] = p4_field_list.name

        elements = []
        for field in p4_field_list.fields:
            element_dict = OrderedDict()
            if type(field) is not p4.p4_field:  # pragma: no cover
                LOG_CRITICAL("only fields supported in field lists for now")
            element_dict["type"] = "field"
            element_dict["value"] = format_field_ref(field)

            elements.append(element_dict)

        learn_list_dict["elements"] = elements

        learn_lists.append(learn_list_dict)

    learn_lists.sort(key=lambda field_list: field_list["id"])

    json_dict["learn_lists"] = learn_lists


def dump_field_lists(json_dict, hlir):
    field_lists = []

    list_ids = field_list_to_id.ids
    for p4_field_list, id_ in list_ids.items():
        field_list_dict = OrderedDict()
        field_list_dict["id"] = id_
        field_list_dict["name"] = p4_field_list.name

        elements = []
        for field in p4_field_list.fields:
            element_dict = OrderedDict()
            if type(field) is not p4.p4_field:  # pragma: no cover
                LOG_CRITICAL("only fields supported in field lists for now")
            element_dict["type"] = "field"
            element_dict["value"] = format_field_ref(field)

            elements.append(element_dict)

        field_list_dict["elements"] = elements

        field_lists.append(field_list_dict)

    field_lists.sort(key=lambda field_list: field_list["id"])

    json_dict["field_lists"] = field_lists


def dump_meters(json_dict, hlir):
    meters = []
    id_ = 0
    for name, p4_meter in hlir.p4_meters.items():
        meter_dict = OrderedDict()
        meter_dict["name"] = name
        meter_dict["id"] = id_
        id_ += 1
        if p4_meter.binding and (p4_meter.binding[0] == p4.P4_DIRECT):
            LOG_CRITICAL("direct meters not supported yet")  # pragma: no cover
        meter_dict["rate_count"] = 2  # 2 rate, 3 colors
        if p4_meter.type == p4.P4_COUNTER_BYTES:
            type_ = "bytes"
        elif p4_meter.type == p4.P4_COUNTER_PACKETS:
            type_ = "packets"
        else:  # pragma: no cover
            LOG_CRITICAL("invalid meter type")
        meter_dict["type"] = type_
        meter_dict["size"] = p4_meter.instance_count

        meters.append(meter_dict)

    json_dict["meter_arrays"] = meters


def dump_counters(json_dict, hlir):
    counters = []
    id_ = 0
    for name, p4_counter in hlir.p4_counters.items():
        counter_dict = OrderedDict()
        counter_dict["name"] = name
        counter_dict["id"] = id_
        id_ += 1
        if p4_counter.binding and (p4_counter.binding[0] == p4.P4_DIRECT):
            counter_dict["is_direct"] = True
            counter_dict["binding"] = p4_counter.binding[1].name
        else:
            counter_dict["is_direct"] = False
            counter_dict["size"] = p4_counter.instance_count

        counters.append(counter_dict)

    json_dict["counter_arrays"] = counters


def dump_registers(json_dict, hlir):
    registers = []
    id_ = 0
    for name, p4_register in hlir.p4_registers.items():
        register_dict = OrderedDict()
        register_dict["name"] = name
        register_dict["id"] = id_
        id_ += 1
        if p4_register.layout is not None:  # pragma: no cover
            LOG_CRITICAL("registers with layout not supported")
        register_dict["bitwidth"] = p4_register.width
        register_dict["size"] = p4_register.instance_count

        registers.append(register_dict)

    json_dict["register_arrays"] = registers


# TODO: what would be a better solution than this
def dump_force_arith(json_dict, hlir):
    force_arith = []

    headers = ["standard_metadata", "intrinsic_metadata"]

    for header_name in headers:
        if header_name not in hlir.p4_header_instances:
            continue
        p4_header_instance = hlir.p4_header_instances[header_name]
        p4_header_type = p4_header_instance.header_type
        for field, _ in p4_header_type.layout.items():
            force_arith.append([header_name, field])

    json_dict["force_arith"] = force_arith


def json_dict_create(hlir):
    # mostly needed for unit tests, I could write a more elegant solution...
    reset_static_vars()
    json_dict = OrderedDict()
    dump_header_types(json_dict, hlir)
    dump_headers(json_dict, hlir)
    dump_header_stacks(json_dict, hlir)
    dump_parsers(json_dict, hlir)
    dump_deparsers(json_dict, hlir)
    dump_meters(json_dict, hlir)
    dump_actions(json_dict, hlir)
    dump_pipelines(json_dict, hlir)
    dump_calculations(json_dict, hlir)
    dump_checksums(json_dict, hlir)
    dump_learn_lists(json_dict, hlir)
    dump_field_lists(json_dict, hlir)
    dump_counters(json_dict, hlir)
    dump_registers(json_dict, hlir)

    dump_force_arith(json_dict, hlir)

    return json_dict
