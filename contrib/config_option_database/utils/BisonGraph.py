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
from utils.YaccParser import parse_yacc

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
def _rules2graph(rules):
    graph = networkx.MultiDiGraph()
    for rule_id, rule in enumerate(rules):
        graph.add_edge(rule.expandable_symbol, str(rule_id))
        for index, symbol in enumerate(rule.expansion):
            graph.add_edge(str(rule_id), symbol, index=index)
    return graph


def _yacc2graph(yacc):
    return _rules2graph(parse_yacc(yacc))


def is_rule(node):
    try:
        int(node)
    except ValueError:
        return False
    return True


class BisonGraph:
    def __init__(self, yaccfile):
        with open(yaccfile, "r") as f:
            yacc = f.read()
            self.graph = _yacc2graph(yacc)

    def get_nodes(self):
        return list(self.graph.nodes)

    def _children_of_rule_sorted(self, node):
        children = []
        for child, arcs in self.graph[node].items():
            for _, arc in arcs.items():
                children.append((arc["index"], child))
        return [x[1] for x in sorted(children)]

    def get_children(self, node):
        if is_rule(node):
            return self._children_of_rule_sorted(node)
        else:
            return sorted(self.graph.successors(node))

    def get_parents(self, node):
        return sorted(self.graph.predecessors(node))

    def is_terminal(self, node):
        return len(list(self.graph.successors(node))) == 0

    def add_arc(self, from_node, to_node):
        if is_rule(from_node) and not is_rule(to_node):
            index = len(self.get_children(from_node))
            self.graph.add_edge(from_node, to_node, index=index)
        elif not is_rule(from_node) and is_rule(to_node):
            self.graph.add_edge(from_node, to_node)
        else:
            raise Exception(
                "Arc must be added from non-rule to rule or rule to non-rule: "
                + from_node
                + "->"
                + to_node
            )

    def make_terminal(self, node):
        children = self.get_children(node)
        for child in children:
            self.graph.remove_edge(node, child)

    def remove(self, node):
        self.graph.remove_node(node)

    def _gather_tokens_from_rules(self, node, paths, stack):
        paths = paths.copy()
        for child in self.get_children(node):
            if self.is_terminal(child):
                if child == "$end":
                    break
                for i in range(len(paths)):
                    paths[i] += (child,)
            else:
                paths = self.get_paths(child, paths, stack)
        return paths

    def _gather_tokens_from_nonterminals(self, node, paths, stack):
        new_paths = []
        for child in self.get_children(node):
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

        if is_rule(node):
            paths = self._gather_tokens_from_rules(node, paths, stack)
        else:
            paths = self._gather_tokens_from_nonterminals(node, paths, stack)

        stack.remove(node)
        return paths
