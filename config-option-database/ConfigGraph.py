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

class ConfigGraph():
    def __init__(self, graph):
        self.graph = graph

    def _get_node(self, node_name):
        return self.graph[node_name]

    def get_start(self):
        return '$accept'

    def get_end(self):
        return '$end'

    def get_nodes(self):
        return self.graph.nodes

    def get_children(self, node_name):
        node = self._get_node(node_name)
        children = [(k, v) for k, v in node.items()]
        if children:
            if 'index' in children[0][1].keys():
                children.sort(key=lambda x : x[1]['index'])
            else:
                children.sort(key=lambda x : x[0])
        return list(map(lambda x : x[0], children))

    def is_terminal(self, node_name):
        return len(self._get_node(node_name)) == 0

    def is_junction(self, node_name):
        self._get_node(node_name) # Exception if not in graph
        try:
            int(node_name)
        except:
            return False
        return True

    def make_terminal(self, node_name):
        children = self.get_children(node_name)
        for child in children:
            self.graph.remove_edge(node_name, child)

    def show_graph(self, graph):
        import matplotlib.pyplot as plt
        pos=networkx.random_layout(self.graph)
        networkx.draw(graph, pos, with_labels=True, node_size=500)
        networkx.draw_networkx_edge_labels(graph, pos)
        plt.show()