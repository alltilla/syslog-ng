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

import pytest
from tempfile import NamedTemporaryFile

from utils.BisonGraph import BisonGraph, Rule

test_string = r"""
%token test1
%token test1next
%token test2
%token test2next
%token KW_TEST
%token number
%token string
%%
start
    : test
    ;
test
    : test1 test1next test1next
    | test2 test2next test
    | KW_TEST '(' test_opts ')'
      {
        int dummy_variable;
        some_c_code(dummy_variable);
      }
    |
    ;
test_opts
    : number
    | string
    ;
%%
"""


@pytest.fixture
def graph():
    with NamedTemporaryFile(mode="w") as f:
        f.write(test_string)
        f.flush()
        f.seek(0)
        graph = BisonGraph(f.name)
    return graph


def test_get_all_symbols(graph):
    expected = [
        "$accept",
        "start",
        "test",
        "test_opts",
        "$end",
        "test1",
        "test1next",
        "test2",
        "test2next",
        "KW_TEST",
        "'('",
        "')'",
        "number",
        "string",
    ]
    assert sorted(graph.get_all_symbols()) == sorted(expected)


def test_get_all_rules(graph):
    expected = [
        Rule("$accept", ["start", "$end"]),
        Rule("start", ["test"]),
        Rule("test", ["test1", "test1next", "test1next"]),
        Rule("test", ["test2", "test2next", "test"]),
        Rule("test", ["KW_TEST", "'('", "test_opts", "')'"]),
        Rule("test", []),
        Rule("test_opts", ["number"]),
        Rule("test_opts", ["string"]),
    ]
    assert sorted(graph.get_all_rules()) == sorted(expected)


def test_get_rules_containing(graph):
    expected = [
        Rule("start", ["test"]),
        Rule("test", ["test1", "test1next", "test1next"]),
        Rule("test", ["test2", "test2next", "test"]),
        Rule("test", ["KW_TEST", "'('", "test_opts", "')'"]),
        Rule("test", []),
    ]
    assert sorted(graph.get_rules_containing("test")) == sorted(expected)


def test_add_rule(graph):
    Rule("test", ["foo"])
    graph.add_rule(Rule("test", ["foo"]))

    assert Rule("test", ["foo"]) in graph.get_all_rules()

def test_remove_rule(graph):
    expected = [
        Rule("$accept", ["start", "$end"]),
        Rule("start", ["test"]),
        Rule("test", ["test1", "test1next", "test1next"]),
        Rule("test", ["test2", "test2next", "test"]),
        Rule("test", []),
        Rule("test_opts", ["number"]),
        Rule("test_opts", ["string"]),
    ]

    graph.remove_rule(Rule("test", ["KW_TEST", "'('", "test_opts", "')'"]))

    assert sorted(graph.get_all_rules()) == sorted(expected)


def test_remove_symbol(graph):
    expected_symbols = [
        "$accept",
        "start",
        "test",
        "$end",
        "test1",
        "test1next",
        "test2",
        "test2next",
        "KW_TEST",
        "'('",
        "')'",
        "number",
        "string",
    ]
    expected_rules = [
        Rule("$accept", ["start", "$end"]),
        Rule("start", ["test"]),
        Rule("test", ["test1", "test1next", "test1next"]),
        Rule("test", ["test2", "test2next", "test"]),
        Rule("test", ["KW_TEST", "'('", "')'"]),
        Rule("test", []),
    ]

    graph.remove_symbol("test_opts")

    assert sorted(graph.get_all_symbols()) == sorted(expected_symbols)
    assert sorted(graph.get_all_rules()) == sorted(expected_rules)


def test_make_terminal(graph):
    expected_symbols = [
        "$accept",
        "start",
        "test",
        "test_opts",
        "$end",
        "test1",
        "test1next",
        "test2",
        "test2next",
        "KW_TEST",
        "'('",
        "')'",
        "number",
        "string",
    ]
    expected_rules = [
        Rule("$accept", ["start", "$end"]),
        Rule("start", ["test"]),
        Rule("test_opts", ["number"]),
        Rule("test_opts", ["string"]),
    ]

    graph.make_terminal("test")

    assert sorted(graph.get_all_symbols()) == sorted(expected_symbols)
    assert sorted(graph.get_all_rules()) == sorted(expected_rules)

# def test_is_rule_node_not_in_graph(graph):
#     with pytest.raises(Exception) as e:
#         graph.is_rule('invalid_node')
#     assert 'Node not in graph:' in str(e.value)





# def test_remove(graph):
#     assert 'KW_TEST' in graph.get_nodes() and '2' in graph.get_nodes()
#     graph.remove('KW_TEST')
#     graph.remove('2')
#     assert 'KW_TEST' not in graph.get_nodes() and '2' not in graph.get_nodes()


# def test_get_paths(graph):
#     expected = [
#         ('test1', 'test1next', 'test1next'),
#         ('test2', 'test2next'),
#         ('KW_TEST', "'('", 'number', "')'"),
#         ('KW_TEST', "'('", 'string', "')'"),
#         ()
#     ]
#     assert graph.get_paths() == expected


# @pytest.mark.parametrize(
#     'from_node,to_node',
#     [
#         ('3', 'test1'),
#         ('test2', '4')
#     ]
# )
# def test_add_arc(graph, from_node, to_node):
#     graph.add_arc(from_node, to_node)
#     assert to_node in graph.get_children(from_node)


# @pytest.mark.parametrize(
#     'from_node,to_node',
#     [
#         ('3', '4'),
#         ('test1', 'test2')
#     ]
# )
# def test_invalid_add_arc(graph, from_node, to_node):
#     with pytest.raises(Exception) as e:
#         graph.add_arc('3', '4')
#     assert 'Arc must be added from non-rule to rule or rule to non-rule:' in str(e.value)
