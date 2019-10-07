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

import yacc2graph

def assert_rule(rule, number, parent, symbols):
  assert rule.number == number and rule.parent == parent and rule.symbols == symbols

def test_yacc2rules():
  yacc = """
%token test1
%token test2
%token test1next
%token test2next
%%
start
    : test
    ;
test
    : test1 test1next
    | test2 test2next
    ;
"""

  rules = yacc2graph.yacc2rules(yacc)

  assert_rule(rules[0], 0, '$accept', ['start', '$end'])
  assert_rule(rules[1], 1, 'start', ['test'])
  assert_rule(rules[2], 2, 'test', ['test1', 'test1next'])
  assert_rule(rules[3], 3, 'test', ['test2', 'test2next'])

def test_yacc2graph():
  yacc = """
%token KW_TEST1
%token KW_TEST2
%token test1_type
%token test2_type
%%
start
    : {asd;} test_opts {asd;} {asd;}
    ;
test_opts
    : test_opt
    | test_opts
    ;
test_opt
    : KW_TEST1 '(' test1_type ')'
    | KW_TEST2 '(' test2_type ')'
    ;
"""

  graph = yacc2graph.yacc2graph(yacc)

def test_print_graph():
  with open('/home/alltilla/Work/repos/OSE/build/modules/afsocket/afsocket-grammar.y', 'r') as myfile:
    yacc = myfile.read()
    graph = yacc2graph.yacc2graph(yacc)
    lines = yacc2graph.get_options(graph)

  print()
  #for line in lines:
    #print(line)
