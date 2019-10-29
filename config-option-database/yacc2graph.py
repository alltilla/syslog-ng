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
from subprocess import Popen, DEVNULL
from os import remove
import xml.etree.ElementTree as xml_parser

import networkx

class Rule():
    def __init__(self, number, parent, symbols):
        self.number = number
        self.parent = parent
        self.symbols = symbols

def _yacc2xml(yacc):
    with _write_to_file(yacc) as file:
        output = '/tmp/yacc2xml.xml'
        try:
            if not _run_in_shell(['bison', '--xml='+output, '--output=/dev/null', file.name]):
                raise Exception('Failed to convert to xml:\n{}\n'.format(yacc))
        except FileNotFoundError:
            raise Exception('bison executable not found')
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
        if symbols:
            rules.append(Rule(number, parent, symbols))
    return rules

def _yacc2rules(yacc):
    xml = _yacc2xml(yacc)
    rules = _xml2rules(xml)
    remove(xml)
    return rules

def _rules2graph(rules):
    graph = networkx.DiGraph()
    for rule in rules:
        rule_node = str(rule.number)
        graph.add_edge(rule.parent, rule_node)
        for index, symbol in enumerate(rule.symbols):
            graph.add_edge(rule_node, symbol, index=index)
    return graph

def yacc2graph(yacc):
    return _rules2graph(_yacc2rules(yacc))

def _run_in_shell(command):
    proc = Popen(command, stderr=DEVNULL, stdout=DEVNULL)
    proc.wait()
    return proc.returncode == 0

def _write_to_file(string):
    file = NamedTemporaryFile(mode='w+')
    file.write(string)
    file.flush()
    file.seek(0)
    return file
