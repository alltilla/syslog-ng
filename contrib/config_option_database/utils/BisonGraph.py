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
from utils.YaccParser import parse_yacc, Rule

# _rules2graph:
# The structure of the graph is the following:
#  * The graph is directed
#  * A node can either be a symbol (terminal/nonterminal) or a rule number
#  * The edges connect the parent nodes to its children nodes
#  * Rule numbers always have symbols as children
#  * Symbols always have rule numbers as children
#  * Edges can be indexed
#  * When we are traversing through the graph, if a node's edges
#    are indexed, the edges must be traversed in ascending order,
#    if they are not indexed, the order does not matter
#  * Rule numbers' edges to their children are indexed
#  * Symbols' edges to their children are not indexed
#
# In simple words, take the following yacc syntax:
# %token test1
# %token test1next
# %token test2
# %token test2next
# %%
# start
#     : test                      # rule number 0
#     ;
# test
#     : test1 test1next test1next # rule number 1
#     | test2 test2next test      # rule number 2
#     ;
#
# * 'start' and 'test' are nonterminal symbols
# * test1, test1next, test2, test2next are terminal symbols
# * Every line, starting with a ':' or a '|' are rules, and they are numbered
#
# * The child of 'start' is 'rule number 0', and it is not indexed
# * The child of 'rule number 0' is 'test', and it is indexed
# * The children of 'test' are 'rule number 0' and 'rule number 1', and they are not indexed
# * The children of 'rule number 1' are 'test1', 'test1next' and 'test1next' and they are indexed
# * The children of 'rule number 2' are 'test2', 'test2next' and 'test', and they are indexed
#
# (See the unit tests for more examples)


def is_rule_node(node):
    return isinstance(node, int)


class BisonGraph:
    def __init__(self, yaccfile):
        self.__next_rule_id = 0
        self.graph = networkx.MultiDiGraph()
        with open(yaccfile, "r") as f:
            yacc = f.read()
            for rule in parse_yacc(yacc):
                self.add_rule(rule)

    # Rule manipulation

    def get_all_rules(self):
        rules = []
        for rule_node in filter(is_rule_node, list(self.graph.nodes)):
            rules.append(self.__create_rule_from_rule_node(rule_node))
        return rules

    def get_rules_containing(self, symbol):
        assert not is_rule_node(symbol)

        rules = []
        rule_nodes_related_to_symbol = set(self.graph.predecessors(symbol)) | set(
            self.graph.successors(symbol)
        )
        for rule_node in rule_nodes_related_to_symbol:
            rules.append(self.__create_rule_from_rule_node(rule_node))
        return rules

    def add_rule(self, rule):
        rule_id = self.__get_next_rule_id()
        self.graph.add_edge(rule.expandable_symbol, rule_id)
        for index, symbol in enumerate(rule.expansion):
            self.graph.add_edge(rule_id, symbol, index=index)

    def remove_rule(self, rule):
        possible_rule_nodes = list(self.graph.successors(rule.expandable_symbol))
        for rule_node in possible_rule_nodes:
            if self.__get_expansion_from_rule_node(rule_node) == rule.expansion:
                self.graph.remove_node(rule_node)

    # Symbol manipulation

    def get_all_symbols(self):
        return list(filter(lambda x: not is_rule_node(x), self.graph.nodes))

    def make_terminal(self, symbol):
        assert not is_rule_node(symbol)

        for rule_node in list(self.graph.successors(symbol)):
            self.graph.remove_node(rule_node)

    def remove_symbol(self, symbol):
        assert not is_rule_node(symbol)

        self.make_terminal(symbol)
        self.graph.remove_node(symbol)

    # Private functions

    def __get_next_rule_id(self):
        next_rule_id = self.__next_rule_id
        self.__next_rule_id += 1
        return next_rule_id

    def __create_rule_from_rule_node(self, rule_node):
        assert is_rule_node(rule_node)

        expandable_symbols = list(self.graph.predecessors(rule_node))
        assert len(expandable_symbols) == 1
        return Rule(
            expandable_symbols[0], self.__get_expansion_from_rule_node(rule_node)
        )

    def __get_expansion_from_rule_node(self, rule_node):
        assert is_rule_node(rule_node)

        indexed_expansion_symbols = []
        for expansion_symbol, arcs in self.graph[rule_node].items():
            for _, arc in arcs.items():
                indexed_expansion_symbols.append((arc["index"], expansion_symbol))
        expansion = [x[1] for x in sorted(indexed_expansion_symbols)]
        return expansion



    # TODO refactor these, and add optimization of unreachable things, etc...

    def __is_terminal(self, node):
        return len(list(self.graph.successors(node))) == 0

    def __gather_tokens_from_rules(self, node, paths, stack):
        paths = paths.copy()
        for child in self.__get_expansion_from_rule_node(node):
            if self.__is_terminal(child):
                if child == "$end":
                    break
                for i in range(len(paths)):
                    paths[i] += (child,)
            else:
                paths = self.get_paths(child, paths, stack)
        return paths

    def __gather_tokens_from_nonterminals(self, node, paths, stack):
        new_paths = []
        for child in sorted(self.graph.successors(node)):
            new_path = self.get_paths(child, paths, stack)
            new_paths.extend(new_path)
        return new_paths

    def get_paths(self, node="$accept", paths=None, stack=None):
        if stack is None:
            stack = set()
        if paths is None:
            paths = [()]

        if node in stack:
            return paths
        stack.add(node)

        if is_rule_node(node):
            paths = self.__gather_tokens_from_rules(node, paths, stack)
        else:
            paths = self.__gather_tokens_from_nonterminals(node, paths, stack)

        stack.remove(node)
        return paths
