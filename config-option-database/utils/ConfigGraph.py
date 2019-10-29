#############################################################################
# Copyright (c) 2019 Balabit
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# As an additional exemption you are allowed to compile & link against the
# OpenSSL libraries as published by the OpenSSL project. See the file
# COPYING for details.
#
#############################################################################

import networkx
from tempfile import NamedTemporaryFile
from pathlib import Path

from yacc2graph import yacc2graph
from utils.MergeYm import merge_grammars

class BisonGraph():
    def __init__(self, yaccfile):
        with open(yaccfile, 'r') as f:
            yacc = f.read()
            self.graph = yacc2graph(yacc)

    def get_start(self):
        return '$accept'

    def get_end(self):
        return '$end'

    def get_nodes(self):
        return iter(list(self.graph.nodes))

    def get_children(self, node_name):
        children_as_list = self.graph.successors(node_name)
        if children_as_list and self.is_junction(node_name):
            children = [(k, v) for k, v in self.graph[node_name].items()]
            children.sort(key=lambda x: x[1]['index'])
            return list(map(lambda x: x[0], children))
        else:
            return list(children_as_list)

    def is_terminal(self, node_name):
        return len(self.get_children(node_name)) == 0

    def is_junction(self, node_name):
        self.graph[node_name] # Exception if not in graph
        try:
            int(node_name)
        except:
            return False
        return True

    def make_terminal(self, node_name):
        children = self.get_children(node_name)
        for child in children:
            self.graph.remove_edge(node_name, child)
    
    def remove(self, node_name):
        self.graph.remove_node(node_name)

    def get_paths(self, node=None, paths=None, stack=None):
        if node == None:
            node = self.get_start()
        if stack == None:
            stack = []
        if paths == None:
            paths = [()]

        if node in stack:
            return paths
        stack.append(node)

        if self.is_junction(node):
            for child in self.get_children(node):
                if self.is_terminal(child):
                    if child == self.get_end():
                        break
                    paths = paths[:]
                    for i in range(len(paths)):
                        paths[i] += (child,)
                else:
                    paths = self.get_paths(child, paths, stack)
        else:
            new_paths = []
            for child in self.get_children(node):
                new_path = self.get_paths(child, paths, stack)
                new_paths.extend(new_path)
            paths = new_paths

        stack.pop()
        return paths

def cut_at_types(graph):
    types = [
        'attribute_option',
        'date_parser_flags',
        'date_parser_stamp',
        'dnsmode',
        'facility_string',
        'filter_content',
        'filter_expr',
        'filter_fac_list',
        'filter_level_list',
        'kafka_property',
        'http_auth_header_plugin',
        'inherit_mode',
        'level_string',
        'log_flags_items',
        'matcher_flags',
        'nonnegative_integer',
        'nonnegative_integer64',
        'parser_csv_delimiters',
        'parser_csv_dialect',
        'parser_csv_flags',
        'path_check',
        'path_no_check',
        'path_secret',
        'positive_integer',
        'stateful_parser_inject_mode',
        'string',
        'string_list',
        'string_or_number',
        'synthetic_message',
        'template_content',
        'template_content_inner',
        'vp_scope_list',
        'yesno',
    ]

    for opt_type in types:
        if not opt_type in graph.get_nodes():
            continue
        graph.make_terminal(opt_type)

def remove_code_blocks(graph):
    list(map(lambda x: graph.remove(x), filter(lambda x: x.startswith('$@'), graph.get_nodes())))

def get_options_from_path(path):
    return OptionParser(path).get_options()

def get_driver_options():
    with NamedTemporaryFile(mode='w+') as yaccfile:
        merge_grammars(yaccfile.name)
        graph = BisonGraph(yaccfile.name)
    cut_at_types(graph)
    remove_code_blocks(graph)
    paths = filter(lambda path: path[0] in ['LL_CONTEXT_SOURCE', 'LL_CONTEXT_DESTINATION'], graph.get_paths())
    options = set()
    for path in paths:
        for option in get_options_from_path(path):
            options.add(option)
    return options

class OptionParser():
    def __init__(self, tokens):
        self.tokens = list(tokens)

    def _find_options_with_keyword(self):
        options = set()
        option_start = None
        for index, token in enumerate(self.tokens):
            if token == "'('" and index != 2:
                assert self.tokens[index - 1].startswith('KW_'), self.tokens
                option_start = index - 1
            elif token == "')'" and option_start != None:
                options.add((option_start, index))
                option_start = None
        return options

    def _find_options_wo_keyword(self):
        options = set()
        left_brace = None
        for index, token in enumerate(self.tokens):
            if token == "'('":
                if left_brace == None:
                    left_brace = index
                    continue
                option_start = left_brace + 1
                option_end = index - 2
                if option_start <= option_end:
                    options.add((option_start, option_end))
                left_brace = index
            elif token == "')'":
                left_brace = None
        return options

    def _find_options(self):
        return self._find_options_wo_keyword() | self._find_options_with_keyword()

    def _parse_keyword_and_arguments(self, option):
        tokens = tuple(self.tokens[option[0]:option[1] + 1])
        if "'('" in tokens and "')'" in tokens:
            assert tokens[0].startswith('KW_') and tokens[1] == "'('" and tokens[-1] == "')'", tokens
            keyword = tokens[0]
            arguments = tokens[2:-1]
        else:
            keyword = ''
            arguments = tokens
        return keyword, arguments

    def _parse_parents(self, option):
        parents = []
        skip = 0
        for index, token in reversed(list(enumerate(self.tokens[:option[0]]))):
            if token == "'('":
                if skip:
                    skip -= 1
                else:
                    parents.append(self.tokens[index - 1])
            elif token == "')'":
                skip += 1
        return tuple(reversed(parents[:-1]))

    def get_options(self):
        assert self.tokens[1].startswith('KW_')
        assert self.tokens[2] == "'('"
        context, driver = self.tokens[0], self.tokens[1]
        options = []
        for option in self._find_options():
            keyword, arguments = self._parse_keyword_and_arguments(option)
            parents = self._parse_parents(option)
            options.append((context, driver, keyword, arguments, parents))
        return options
