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

from utils.Yacc2Graph import _yacc2rules, yacc2graph, _yacc2xml

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

def test_yacc2xml():
    assert _yacc2xml(test_string)

def test_failed_yacc2xml():
    with pytest.raises(Exception) as e:
        _yacc2xml(test_string[2:])
    assert 'Failed to convert to xml:' in str(e.value)

def test_yacc2rules():
    expected = [
        (0, '$accept', ['start', '$end']),
        (1, 'start', ['test']),
        (2, 'test', ['test1', 'test1next']),
        (3, 'test', ['test2', 'test2next', 'test']),
        (4, 'test', ['KW_TEST', "'('", 'test_opts', "')'"]),
        (5, 'test', []),
        (6, 'test_opts', ['number']),
        (7, 'test_opts', ['string'])
    ]

    rules = _yacc2rules(test_string)
    assert len(rules) == len(expected)
    for number, parent, symbols in expected:
        rule = rules[number]
        assert rule.number == number and rule.parent == parent and rule.symbols == symbols

def test_yacc2graph():
    expected = [
        ('$accept', {'0': {}}),
        ('0', {'start': {'index': 0}, '$end': {'index': 1}}),
        ('start', {'1': {}}),
        ('1', {'test': {'index': 0}}),
        ('test', {'2': {}, '3': {}, '4': {}, '5': {}}),
        ('2', {'test1': {'index': 0}, 'test1next': {'index': 1}}),
        ('3', {'test2': {'index': 0}, 'test2next': {'index': 1}, 'test': {'index': 2}}),
        ('4', {'KW_TEST': {'index': 0}, "'('": {'index': 1}, 'test_opts': {'index': 2}, "')'": {'index': 3}}),
        ('test_opts', {'6': {}, '7': {}}),
        ('6', {'number': {'index': 0}}),
        ('7', {'string': {'index': 0}}),
        ('$end', {}),
        ('test1', {}),
        ('test1next', {}),
        ('test2', {}),
        ('test2next', {}),
        ('KW_TEST', {}),
        ("'('", {}),
        ("')'", {}),
        ("number", {}),
        ("string", {}),
        ('5', {})
    ]

    graph = yacc2graph(test_string)
    assert sorted(graph.nodes) == sorted([x[0] for x in expected])
    for node, children in expected:
        assert graph[node] == children
