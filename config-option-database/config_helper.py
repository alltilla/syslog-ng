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
from utils.ConfigGraph import BisonGraph, cut_at_types, remove_code_blocks, OptionParser
from argparse import ArgumentParser

def get_paths():
    with NamedTemporaryFile(mode='w+') as yaccfile:
        merge_grammars(yaccfile.name)
        graph = BisonGraph(yaccfile.name)
    cut_at_types(graph)
    remove_code_blocks(graph)
    return graph.get_paths()

def get_db():
    contexts = ['LL_CONTEXT_SOURCE', 'LL_CONTEXT_DESTINATION']
    paths = filter(lambda x: x[0] in contexts, get_paths())
    db = dict.fromkeys(contexts, {})
    for path in paths:
        for option in OptionParser(path).get_options():
            context, driver = option.drivers[0]
            keyword = option.keyword
            db[context].setdefault(driver, {'options': set(), 'blocks': {}})
            add_to = db[context][driver]
            for parent in option.parents:
                add_to['blocks'].setdefault(parent, {'options':set(), 'blocks':{}})
                add_to = add_to['blocks'][parent]
            add_to['options'].add((keyword if keyword else '', ' '.join(option.types)))
    return db

def print_options(db, context, driver):
    print('{} {}:'.format(context, driver))
    print_options_helper(db[context][driver], 1)

def print_options_helper(block, depth):
    indent = '  ' * depth
    for keyword, arguments in sorted(block['options']):
        print('{}{}<{}>'.format(indent, (keyword + ': ') if keyword else '', arguments))
    for key in sorted(block['blocks'].keys()):
        print('{}{}:'.format(indent, key))
        print_options_helper(block['blocks'][key], depth + 1)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('context', type=str, help='source/destination')
    parser.add_argument('driver', type=str, help='driver')
    args = parser.parse_args()
    return args.context, args.driver

def main():
    context, driver = parse_args()
    print_options(get_db(), context, driver)

if __name__ == '__main__':
    main()
