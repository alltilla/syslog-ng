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

from tempfile import NamedTemporaryFile

from utils.MergeYm import merge_grammars
from utils.ConfigGraph import BisonGraph, SyntaxGraph, cut_at_types, remove_code_blocks, OptionParser
from argparse import ArgumentParser, REMAINDER

contexts = [
    'LL_CONTEXT_SOURCE',
    'LL_CONTEXT_DESTINATION'
]

def get_options_dict(graph):
    all_options = set()
    paths = filter(lambda x: x[0] in contexts, graph.get_paths())
    for path in paths:
        options = OptionParser(path).get_options()
        for option in options:
            all_options.add(option)
    options_dict = {}
    for context in contexts:
        options_dict[context] = {}
    for option in all_options:
        context = option.drivers[0][0]
        driver = option.drivers[0][1]
        if driver not in options_dict[context].keys():
            options_dict[context][driver] = []
        entry = {}
        entry['keyword'] = option.keyword
        entry['types'] = option.types
        if option.parents:
            parent = option.parents[0]
            if parent not in options_dict[context][driver].keys():
                options_dict[context][driver][parent] = []
            options_dict[context][driver][parent].append(entry)
        else:
            options_dict[context][driver].append(entry)
    return options_dict

def get_graph():
    with NamedTemporaryFile(mode='w+') as yaccfile:
        merge_grammars(yaccfile.name)
        graph = BisonGraph(yaccfile.name)
    cut_at_types(graph)
    remove_code_blocks(graph)
    return graph

def deep_print(block, depth=1):
    options = list(block['options'])
    options.sort()
    for option in options:
        keyword = option[0]
        types = option[1]
        if keyword:
            print('  '*depth+keyword+': '+'<'+types+'>')
        else:
            print('  '*depth+'<'+types+'>')
    for key in block['blocks'].keys():
        print('  '*depth+key+':')
        deep_print(block['blocks'][key], depth+1)


def main():
    parser = ArgumentParser()
    parser.add_argument('context', type=str, help='source/destination')
    parser.add_argument('driver', type=str, help='driver')
    args = parser.parse_args()

    graph = get_graph()
    paths = filter(lambda x: x[0] in contexts, graph.get_paths())
    db = {}
    for context in contexts:
        db[context] = {}
    for path in paths:
        for option in OptionParser(path).get_options():
            context = option.drivers[0][0]
            driver = option.drivers[0][1]
            if not driver in db[context].keys():
                db[context][driver] = {'options':set(), 'blocks':{}}
            insert_to = db[context][driver]
            for parent in option.parents:
                if not parent in insert_to['blocks'].keys():
                    insert_to['blocks'][parent] = {'options':set(), 'blocks':{}}
                insert_to = insert_to['blocks'][parent]
            keyword = option.keyword
            if keyword == None:
                keyword = ''
            insert_to['options'].add((keyword, ' '.join(option.types)))
    # import json
    # print(json.dumps(db, indent=2))

    print(args.context+' '+args.driver+':')
    deep_print(db[args.context][args.driver])



if __name__ == '__main__':
    main()
