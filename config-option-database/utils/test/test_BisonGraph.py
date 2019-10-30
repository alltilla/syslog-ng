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

from utils.BisonGraph import BisonGraph

@pytest.fixture
def graph():
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
    : test1 test1next
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
    with NamedTemporaryFile(mode='w') as f:
        f.write(test_string)
        f.flush()
        f.seek(0)
        graph = BisonGraph(f.name)
    return graph

def test_node_children_junction_terminal(graph):
    expected = [
        {
            'node': '$accept',
            'children': ['0'],
            'is_junction': False,
            'is_terminal': False
        },
        {
            'node': '0',
            'children': ['start', '$end'],
            'is_junction': True,
            'is_terminal': False
        },
        {
            'node': 'start',
            'children': ['1'],
            'is_junction': False,
            'is_terminal': False
        },
        {
            'node': '1',
            'children': ['test'],
            'is_junction': True,
            'is_terminal': False
        },
        {
            'node': 'test',
            'children': ['2', '3', '4', '5'],
            'is_junction': False,
            'is_terminal': False
        },
        {
            'node': '2',
            'children': ['test1', 'test1next'],
            'is_junction': True,
            'is_terminal': False
        },
        {
            'node': '3',
            'children': ['test2', 'test2next', 'test'],
            'is_junction': True,
            'is_terminal': False
        },
        {
            'node': '4',
            'children': ['KW_TEST', "'('", 'test_opts', "')'"],
            'is_junction': True,
            'is_terminal': False
        },
        {
            'node': 'test_opts',
            'children': ['6', '7'],
            'is_junction': False,
            'is_terminal': False
        },
        {
            'node': '6',
            'children': ['number'],
            'is_junction': True,
            'is_terminal': False
        },
        {
            'node': '7',
            'children': ['string'],
            'is_junction': True,
            'is_terminal': False
        },
        {
            'node': '$end',
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': 'test1',
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': 'test1next',
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': 'test2',
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': 'test2next',
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': 'KW_TEST',
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': "'('",
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': "')'",
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': "number",
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': "string",
            'children': [],
            'is_junction': False,
            'is_terminal': True
        },
        {
            'node': '5',
            'children': [],
            'is_junction': True,
            'is_terminal': True
        }
    ]

    assert sorted(graph.get_nodes()) == sorted([x['node'] for x in expected])
    for expect in expected:
        assert graph.get_children(expect['node']) == expect['children']
        assert graph.is_junction(expect['node']) == expect['is_junction']
        assert graph.is_terminal(expect['node']) == expect['is_terminal']

def test_get_paths(graph):
    expected = [
        ('test1', 'test1next'),
        ('test2', 'test2next'),
        ('KW_TEST', "'('", 'number', "')'"),
        ('KW_TEST', "'('", 'string', "')'"),
        ()
    ]
    assert graph.get_paths() == expected

def test_make_terminal(graph):
    expected = [
        ('test1', 'test1next'),
        ('test2', 'test2next'),
        ('KW_TEST', "'('", 'test_opts', "')'"),
        ()
    ]
    graph.make_terminal('test_opts')
    assert graph.get_children('test_opts') == []
    assert graph.get_paths() == expected

def test_remove(graph):
    expected = [
        ('test2', 'test2next'),
        ("'('", 'number', "')'"),
        ("'('", 'string', "')'"),
        ()
    ]
    graph.remove('KW_TEST')
    graph.remove('2')
    assert 'KW_TEST' not in graph.get_nodes() and '2' not in graph.get_nodes()
    assert graph.get_paths() == expected
