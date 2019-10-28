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

from json import dumps
from tempfile import NamedTemporaryFile

from utils.MergeYm import merge_grammars
from utils.ConfigGraph import BisonGraph, SyntaxGraph, cut_at_types, remove_code_blocks, OptionParser


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
    # g = SyntaxGraph(paths)
    # g.print_path()
    options = []
    for path in paths:
        #path = list(filter(lambda x: not x.startswith('$@'), list(path)))
        OptionParser(path).parse_and_merge(options)
    return options

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
            if not root_driver:
                continue
            entry['root_driver'] = root_driver
            if context not in database:
                database[context] = []
            database[context].append(entry)
    return database

def main():
    with NamedTemporaryFile(mode='w+') as yaccfile:
        merge_grammars(yaccfile.name)
        graph = BisonGraph(yaccfile.name)
    cut_at_types(graph)
    remove_code_blocks(graph)
    options = get_options(graph)
    database = build_database(options)
    print(dumps(database, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
