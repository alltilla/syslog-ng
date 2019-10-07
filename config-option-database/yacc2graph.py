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

class Rule():
    def __init__(self, number, parent, symbols):
        self.number = number
        self.parent = parent
        self.symbols = symbols

def _run_in_shell(command):
    proc = Popen(command)
    proc.wait()
    return proc.returncode == 0

def _write_to_file(string):
  file = NamedTemporaryFile(mode='w+')
  file.write(string)
  file.flush()
  file.seek(0)
  return file

def _yacc2xml(yacc):
    with _write_to_file(yacc) as file:
        output = '/tmp/yacc2xml.xml'
        try:
            if not _run_in_shell(['bison', '--xml='+output, file.name]):
                raise Exception('Failed to convert to xml:\n{}\n'.format(yacc))
        except FileNotFoundError:
            raise Exception('bison executable not found')
        #_run_in_shell(['cat', '/tmp/yacc2xml.xml'])
        return output

def _xml2rules(filename):
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
        rules.append(Rule(number, parent, symbols))
    return rules

def yacc2rules(yacc):
    xml = _yacc2xml(yacc)
    rules = _xml2rules(xml)
    remove(xml)
    return rules

def show_graph(graph):
    import matplotlib.pyplot as plt
    pos=networkx.planar_layout (graph)
    networkx.draw(graph, pos, with_labels=True, node_size=500)
    networkx.draw_networkx_edge_labels(graph, pos)
    plt.show()

def rules2graph(rules):
    graph = networkx.DiGraph()
    for rule in rules:
        rule_node = str(rule.number)
        graph.add_edge(rule.parent, rule_node)
        for index, symbol in enumerate(rule.symbols):
            graph.add_edge(rule_node, symbol, index=index)

    #show_graph(graph)
    return graph

def yacc2graph(yacc):
    return rules2graph(yacc2rules(yacc))

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

def get_options2(graph, node_key='$accept', stack=None, lines=None):
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
                if child != '$end':
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

class Option():
    def __init__(self, line):
        self.driver = None
        self.driver_type = None
        self.keyword = []
        self.type = []
        self.parents = []
        self.tokens = line.split(' ')
        print('---')
        print('tokens', line)
        self.parse(self.tokens)

        print('hi', self.driver_type, self.driver, self.keyword, self.type, self.parents)

    def parse(self, tokens):
        if not tokens:
            return
        if not self.driver_type or not self.driver:
            if 'LL_CONTEXT_' not in tokens[0]:
                raise Exception('Not a driver option')
            if tokens[2] != "'('":
                raise Exception("Missing driver '('")
            if tokens[-1] != "')'":
                raise Exception("Missing driver ')'")
            self.driver_type = tokens[0]
            self.driver = tokens[1]
            self.parse(tokens[3:-1])
            return
        if not "'('" in tokens and not "')'" in tokens:
            self.keyword = tokens
            return
        else:
            if tokens[-1] != "')'":
                raise Exception("Missing option ')'")
            lb = tokens.index("'('")
            keyword = tokens[:lb]
            types = tokens[lb+1:-1]
            if "'('" in types:
                self.parents.append(keyword)
                self.parse(types)
                return
            self.keyword = keyword
            self.type = types
            return


def get_options(graph):
    lines = get_options2(graph)
    options = []
    for line in lines:
        option = Option(line)
        options.append(option)
        #print(option.tokens)
    return options
