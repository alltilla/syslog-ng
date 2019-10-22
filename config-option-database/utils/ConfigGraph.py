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

class ConfigGraph():
    def __init__(self, yaccfile):
        with open(yaccfile, 'r') as f:
            yacc = f.read()
            self.graph = yacc2graph(yacc)

    def get_start(self):
        return '$accept'

    def get_end(self):
        return '$end'

    def get_nodes(self):
        return self.graph.nodes

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