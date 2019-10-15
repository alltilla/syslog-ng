#!/usr/bin/env python3
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

from tempfile import NamedTemporaryFile
from subprocess import Popen
from os import remove

import xml.etree.ElementTree as xml_parser
import networkx

def show_graph(graph):
    import matplotlib.pyplot as plt
    pos=networkx.planar_layout (graph)
    networkx.draw(graph, pos, with_labels=True, node_size=500)
    networkx.draw_networkx_edge_labels(graph, pos)
    plt.show()


class ConfigGraph():
    def __init__(self, yacc):
        self.graph = self.yacc2graph(yacc)

    class Rule():
        def __init__(self, number, parent, symbols):
            self.number = number
            self.parent = parent
            self.symbols = symbols

    def _yacc2xml(self, yacc):
        with self._write_to_file(yacc) as file:
            output = '/tmp/yacc2xml.xml'
            try:
                if not self._run_in_shell(['bison', '--xml='+output, file.name]):
                    raise Exception('Failed to convert to xml:\n{}\n'.format(yacc))
            except FileNotFoundError:
                raise Exception('bison executable not found')
            return output

    def _xml2rules(self, filename):
        rules = []
        root = xml_parser.parse(filename).getroot()
        for rule in root.iter('rule'):
            number = int(rule.get('number'))
            parent = rule.find('lhs').text
            symbols = []
            for symbol in rule.find('rhs'):
                if symbol.tag == 'empty':
                    break
                symbols.append(symbol.text)
            if symbols:
                rules.append(ConfigGraph.Rule(number, parent, symbols))
        return rules

    def yacc2rules(self, yacc):
        xml = self._yacc2xml(yacc)
        rules = self._xml2rules(xml)
        remove(xml)
        return rules

    def rules2graph(self, rules):
        graph = networkx.DiGraph()
        for rule in rules:
            rule_node = str(rule.number)
            graph.add_edge(rule.parent, rule_node)
            for index, symbol in enumerate(rule.symbols):
                graph.add_edge(rule_node, symbol, index=index)
        return graph

    def yacc2graph(self, yacc):
        return self.rules2graph(self.yacc2rules(yacc))

    def _run_in_shell(self, command):
        proc = Popen(command)
        proc.wait()
        return proc.returncode == 0

    def _write_to_file(self, string):
        file = NamedTemporaryFile(mode='w+')
        file.write(string)
        file.flush()
        file.seek(0)
        return file

def get_children(node):
    children = [(k, v) for k, v in node.items()]
    if children:
        if 'index' in children[0][1].keys():
            children.sort(key=lambda x : x[1]['index'])
        else:
            children.sort(key=lambda x : x[0])
    return list(map(lambda x : x[0], children))

def is_terminal(node):
    return not get_children(node)

def is_rule(node_key):
    try:
        int(node_key)
    except:
        return False
    return True

def lines_append(lines, terminal):
    buf = lines[:]
    for i in range(len(lines)):
        if buf[i] != '':
            buf[i] += ' '
        buf[i] += terminal
    return buf

def get_options2(graph, node_key, stack=None, lines=None):
    if not stack:
        stack = []
    if not lines:
        lines = ['']
    
    if node_key in stack:
        return lines
    
    stack.append(node_key)
    node = graph[node_key]

    if is_rule(node_key):
        for child in get_children(node):
            if is_terminal(graph[child]):
                if child != '$end' and '$@' != child[:2]:
                    lines = lines_append(lines, child)
            else:
                lines = get_options2(graph, child, stack, lines)
    else:
        new_lines = []
        for child in get_children(node):
            new_line = get_options2(graph, child, stack, lines)
            new_lines.extend(new_line)
        lines = new_lines

    stack.pop()
    return lines

class OptionParser():
    def __init__(self, line, options):
        self.tokens = line.split(' ')
        self.options = options

    class Option():
        def __init__(self, drivers, keyword, types, parents):
            self.drivers = drivers
            self.keyword = keyword
            self.types = types
            self.parents = parents

        def __eq__(self, other):
            return self.drivers == other.drivers and self.keyword == other.keyword and self.types == other.types and self.parents == other.parents

    def _find_leaves(self):
        leaves = set()
        lb = None

        for index, token in enumerate(self.tokens):
            if token == "'('":
                lb = index
            elif token == "')'" and lb != None:
                assert self.tokens[lb-1][0:3] == 'KW_', "No KW_ before '('"
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

    def _get_options(self, leaves):
        assert self.tokens[0][:11] == 'LL_CONTEXT_'
        assert self.tokens[1][:3] == 'KW_'
        assert self.tokens[2] == "'('"
        options = []
        drivers = [(self.tokens[0], self.tokens[1])]
        for leave_interval in leaves:
            leave = self.tokens[leave_interval[0]:leave_interval[1]+1]
            if "'('" in leave and "')'" in leave:
                assert leave.index("'('") == 1
                assert leave.index("')'") == len(leave)-1
                assert leave[0][:3] == 'KW_'
                keyword = leave[0]
                types = leave[leave.index("'('")+1:leave.index("')'")]
            else:
                keyword = None
                types = leave

            skip = 0
            parents = []
            next_is_kw = False
            reverse_sublist = self.tokens[:leave_interval[0]]
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
            parents = parents[1:]
            option = OptionParser.Option(drivers, keyword, types, parents)
            append = True
            for other in self.options:
                if option.keyword == other.keyword and option.types == other.types and option.parents == other.parents:
                    if option.drivers[0] not in other.drivers:
                        other.drivers.append(option.drivers[0])
                    append = False
                    break
            if append:
                options.append(option)
        return options

    def parse(self):
        leaves = self._find_leaves()
        options = self._get_options(leaves)
        return options

def get_options(graph):
    types = [
        'date_parser_flags',
        'date_parser_stamp',
        'dnsmode',
        'facility_string',
        'filter_content',
        'filter_expr',
        'filter_fac_list',
        'filter_level_list',
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
        if not opt_type in graph:
            continue
        children = get_children(graph[opt_type])
        for child in children:
            graph.remove_edge(opt_type, child)

    lines = get_options2(graph, '$accept')
    options = []
    for line in lines:
        option_parser = OptionParser(line, options)
        options.extend(option_parser.parse())
    #for option in options:
    #    print(option.drivers, option.keyword, option.types, option.parents)
    return options
