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

from pprint import pprint
from tempfile import NamedTemporaryFile

from utils.MergeYm import merge_grammars
from utils.ConfigGraph import ConfigGraph

class OptionParser():
    def __init__(self, tokens):
        self.tokens = list(filter(lambda x: not x.startswith('$@'), list(tokens)))

    class Option():
        def __init__(self, drivers, keyword, types, parents):
            self.drivers = drivers
            self.keyword = keyword
            self.types = types
            self.parents = parents

    def _find_leaves(self):
        leaves = set()
        lb = None

        for index, token in enumerate(self.tokens):
            if token == "'('":
                lb = index
            elif token == "')'" and lb != None:
                assert self.tokens[lb-1][0:3] == 'KW_', self.tokens
                leaves.add((lb-1, index))
                lb = None

        skip = 0
        lb = None
        for index in range(len(self.tokens)-1, 0, -1):
            token = self.tokens[index]
            if token == "'('":
                if skip:
                    skip -= 1
                    continue
                if lb and lb - index > 2:
                    leaves.add((index+1, lb-1-1))
                lb = index
            elif token == "')'" and lb:
                skip += 1

        return leaves

    def _parse_drivers(self):
        #assert self.tokens[1].startswith('KW_')
        assert self.tokens[2] == "'('"
        return [(self.tokens[0], self.tokens[1])]

    def _parse_keyword_and_types(self, leave_interval):
        leave = self.tokens[leave_interval[0]:leave_interval[1]+1]
        if "'('" in leave and "')'" in leave:
            assert leave[0].startswith('KW_') and leave[1] == "'('" and leave[-1] == "')'", leave
            keyword = leave[0]
            types = leave[2:-1]
        else:
            keyword = None
            types = leave
        return keyword, types

    def _parse_parents(self, leave_interval):
        skip = 0
        parents = []
        next_is_kw = False
        reverse_sublist = self.tokens[:leave_interval[0]]
        reverse_sublist.reverse()
        for token in reverse_sublist:
            if token == "'('":
                if skip:
                    skip -= 1
                else:
                    next_is_kw = True
            elif next_is_kw:
                parents.append(token)
                next_is_kw = False
            elif token == "')'":
                skip += 1
        parents.reverse()
        return parents[1:]

    def _get_options(self, leaves):
        options = []
        for leave_interval in leaves:
            drivers = self._parse_drivers()
            keyword, types = self._parse_keyword_and_types(leave_interval)
            parents = self._parse_parents(leave_interval)
            options.append(OptionParser.Option(drivers, keyword, types, parents))
        return options

    def _merge(self, options, option_list):
        append = True
        for option in options:
            for other in option_list:
                if option.keyword == other.keyword and option.types == other.types and option.parents == other.parents:
                    if option.drivers[0] not in other.drivers:
                        other.drivers.append(option.drivers[0])
                    append = False
                    break
            if append:
                option_list.append(option)

    def parse_and_merge(self, option_list):
        leaves = self._find_leaves()
        options = self._get_options(leaves)
        self._merge(options, option_list)


types = [
    'attribute_option',
    'date_parser_flags',
    'date_parser_stamp',
    'dnsmode',
    'facility_string',
    'filter_content',
    'filter_expr',
    'filter_fac_list',
    'filter_level_list',
    'kafka_property',
    'http_auth_header_plugin',
    'inherit_mode',
    'level_string',
    'log_flags_items',
    'matcher_flags',
    'nonnegative_integer',
    'nonnegative_integer64',
    'parser_csv_delimiters',
    'parser_csv_dialect',
    'parser_csv_flags',
    'path_check',
    'path_no_check',
    'path_secret',
    'positive_integer',
    'stateful_parser_inject_mode',
    'string',
    'string_list',
    'string_or_number',
    'synthetic_message',
    'template_content',
    'template_content_inner',
    'vp_scope_list',
    'yesno',
]

contexts = [
    'LL_CONTEXT_SOURCE',
    'LL_CONTEXT_DESTINATION',
    'LL_CONTEXT_PARSER',
    'LL_CONTEXT_PRAGMA',
    'LL_CONTEXT_FILTER',
    'LL_CONTEXT_REWRITE'
]

def get_options(graph):
    paths = filter(lambda x: x[0] in contexts, graph.get_paths())
    options = []
    for path in paths:
        OptionParser(path).parse_and_merge(options)
    return options

def cut_at_types(graph):
    for opt_type in types:
        if not opt_type in graph.get_nodes():
            continue
        graph.make_terminal(opt_type)

def build_database(options):
    database = {}
    for option in options:
        for context in contexts:
            entry = {}
            if option.keyword:
                entry['option_name'] = option.keyword
            else:
                entry['option_name'] = ''
            entry['option_value'] = option.types
            entry['parent_options'] = option.parents
            root_driver = []
            for driver in option.drivers:
                if driver[0] == context:
                    root_driver.append(driver[1])
            entry['root_driver'] = root_driver
            if context not in database:
                database[context] = []
            database[context].append(entry)
    return database

def main():
    with NamedTemporaryFile(mode='w+') as yaccfile:
        merge_grammars(yaccfile.name)
        graph = ConfigGraph(yaccfile.name)
    cut_at_types(graph)
    options = get_options(graph)
    database = build_database(options)
    pprint(database)

if __name__ == '__main__':
    main()
