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
from os import remove, path, listdir
from glob import glob
from importlib import import_module
from inspect import getargspec

from ConfigGraph import ConfigGraph

import networkx

import xml.etree.ElementTree as xml_parser


class Yacc2Graph():
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
                rules.append(Yacc2Graph.Rule(number, parent, symbols))
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
        proc = Popen(command, stderr=DEVNULL, stdout=DEVNULL)
        proc.wait()
        return proc.returncode == 0

    def _write_to_file(self, string):
        file = NamedTemporaryFile(mode='w+')
        file.write(string)
        file.flush()
        file.seek(0)
        return file

class PluginExecutor():
    def __init__(self, debug=False):
        self.debug = debug
        with open('/home/alltilla/Work/repos/OSE/build/modules/afsocket/afsocket-grammar.y', 'r') as myfile:
            yacc = myfile.read()
            graph = Yacc2Graph().yacc2graph(yacc)
            self.graph = ConfigGraph(graph)
            self.plugins = {}
            self.load_plugins()

    def log(self, message):
        if self.debug:
            print(message)

    def load_plugins(self):
        plugin_dir = path.join(path.dirname(__file__), 'plugins')
        for full_filename in glob(path.join(plugin_dir, '*.py')):
            plugin_name = path.basename(full_filename)[:-3]
            plugin_module = import_module('plugins.'+plugin_name, package='plugin')
            func_args = getargspec(plugin_module.plugin).args
            assert func_args == ['graph', 'args'], 'Invalid arguments for plugin function'
            self.load_plugin(plugin_name, plugin_module.plugin)

    def load_plugin(self, plugin_name, plugin):
        assert plugin_name not in self.plugins, 'Plugin already exists: ' + plugin_name
        self.plugins[plugin_name] = plugin
        self.log('Loaded plugin: ' + plugin_name)

    def run_plugin(self, plugin_name, attrs):
        self.plugins[plugin_name](self.graph, attrs)
