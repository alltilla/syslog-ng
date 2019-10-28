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
from yacc2graph import yacc2graph

from pathlib import Path

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

    def show_graph(self):
        import matplotlib.pyplot as plt
        pos=networkx.random_layout(self.graph)
        networkx.draw(self.graph, pos, with_labels=True, node_size=500)
        networkx.draw_networkx_edge_labels(self.graph, pos)
        plt.show()

class SyntaxGraph():
    def __init__(self, paths):
        self.graph = self.build_syntax_graph(paths)

    def build_syntax_graph(self, paths):
        graph = {None:{}}
        for path in paths:
            insert_to = graph[None]
            for token in path:
                if token[0] == "'" and token[-1] == "'":
                    token = token[1:-1]
                if not token in insert_to.keys():
                    insert_to[token] = {}
                insert_to = insert_to[token]
        # from json import dumps
        # print(dumps(graph, indent=2))
        return graph

    def print_path(self, children=None, string=''):
        if children == None:
            children = self.graph[None]
        keys = children.keys()
        if len(keys) == 0:
            print(string)
        elif len(keys) == 1:
            child = list(keys)[0]
            string2 = string + ' ' + child
            self.print_path(children[child], string2)
        else:
            print(string)
            sorted_keys = list(children.keys())
            sorted_keys.sort()
            for child in sorted_keys:
                string2 = len(string)*' ' + ' ' + child
                self.print_path(children[child], string2)

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

class OptionParser():
    def __init__(self, tokens):
        self.tokens = list(tokens)

    class Option():
        def __init__(self, drivers, keyword, types, parents):
            self.drivers = drivers
            self.keyword = keyword
            self.types = types
            self.parents = parents

        def __eq__(self, other):
            return self.drivers == other.drivers and self.keyword == other.keyword and self.types == other.types and self.parents == other.parents

        def __str__(self):
            return str(self.drivers) + ', ' + str(self.keyword) + ', ' + ' '.join(self.types) + ', ' + ' '.join(self.parents)

        def __hash__(self):
            return hash(str(self))

    def _find_leaves(self):
        leaves = set()
        lb = None

        for index, token in enumerate(self.tokens):
            if token == "'('":
                lb = index
            elif token == "')'" and lb != None:
                assert self.tokens[lb-1][0:3] == 'KW_', self.tokens
                leaves.add((lb-1, index))
                lb = None

        skip = 0
        lb = None
        for index in range(len(self.tokens)-1, 0, -1):
            token = self.tokens[index]
            if token == "'('":
                if skip:
                    skip -= 1
                    continue
                if lb and lb - index > 2:
                    leaves.add((index+1, lb-1-1))
                lb = index
            elif token == "')'" and lb:
                skip += 1

        return leaves

    def _parse_drivers(self):
        #assert self.tokens[1].startswith('KW_')
        assert self.tokens[2] == "'('"
        return [(self.tokens[0], self.tokens[1])]

    def _parse_keyword_and_types(self, leaf_interval):
        leaf = self.tokens[leaf_interval[0]:leaf_interval[1]+1]
        if "'('" in leaf and "')'" in leaf:
            assert leaf[0].startswith('KW_') and leaf[1] == "'('" and leaf[-1] == "')'", leaf
            keyword = leaf[0]
            types = leaf[2:-1]
        else:
            keyword = None
            types = leaf
        return keyword, types

    def _parse_parents(self, leaf_interval):
        skip = 0
        parents = []
        next_is_kw = False
        reverse_sublist = self.tokens[:leaf_interval[0]]
        reverse_sublist.reverse()
        for token in reverse_sublist:
            if token == "'('":
                if skip:
                    skip -= 1
                else:
                    next_is_kw = True
            elif next_is_kw:
                parents.append(token)
                next_is_kw = False
            elif token == "')'":
                skip += 1
        parents.reverse()
        return parents[1:]

    def get_options(self):
        options = []
        for leaf_interval in self._find_leaves():
            drivers = self._parse_drivers()
            keyword, types = self._parse_keyword_and_types(leaf_interval)
            parents = self._parse_parents(leaf_interval)
            options.append(OptionParser.Option(drivers, keyword, types, parents))
        return options

    def _merge(self, options, option_list):
        append = True
        for option in options:
            for other in option_list:
                if option.keyword == other.keyword and option.types == other.types and option.parents == other.parents:
                    if option.drivers[0] not in other.drivers:
                        other.drivers.append(option.drivers[0])
                    append = False
                    break
            if append:
                option_list.append(option)

    def parse_and_merge(self, option_list):
        options = self.get_options()
        self._merge(options, option_list)
