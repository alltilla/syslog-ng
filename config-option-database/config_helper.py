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
from pathlib import Path
import json

from utils.MergeYm import merge_grammars
from utils.ConfigGraph import BisonGraph, get_options
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('context', type=str, help='source/destination')
    parser.add_argument('driver', type=str, help='driver')
    parser.add_argument('--rebuild', '-r', action='store_true')
    args = parser.parse_args()
    return args.context, args.driver, args.rebuild

def get_graph():
    with NamedTemporaryFile(mode='w+') as yaccfile:
        merge_grammars(yaccfile.name)
        graph = BisonGraph(yaccfile.name)
    return graph

def build_db():
    db = {'LL_CONTEXT_SOURCE': {}, 'LL_CONTEXT_DESTINATION': {}}
    for context, driver, keyword, arguments, parents in get_options(get_graph()):
        db[context].setdefault(driver, {'options': [], 'blocks': {}})
        add_to = db[context][driver]
        for parent in parents:
            add_to['blocks'].setdefault(parent, {'options': [], 'blocks':{}})
            add_to = add_to['blocks'][parent]
        add_to['options'].append((keyword if keyword else '', arguments))
    return db

def get_db(rebuild):
    cache_file = Path(__file__).parents[0] / '.cache' / 'options.json'
    Path.mkdir(cache_file.parents[0], exist_ok=True)
    if rebuild or not cache_file.exists():
        db = build_db()
        with cache_file.open('w') as f:
            json.dump(db, f, indent=2)
    else:
        with cache_file.open() as f:
            db = json.load(f)
    return db

def print_options_helper(block, depth):
    indent = '  ' * depth
    for keyword, arguments in sorted(block['options']):
        print('{}{}{}'.format(indent, (keyword + ': ') if keyword else '', ' '.join(['<'+x+'>' for x in arguments])))
    for key in sorted(block['blocks'].keys()):
        print('{}{}:'.format(indent, key))
        print_options_helper(block['blocks'][key], depth + 1)

def print_options(db, context, driver):
    print('{} {}:'.format(context, driver))
    print_options_helper(db[context][driver], 1)

def main():
    context, driver, rebuild = parse_args()
    db = get_db(rebuild)
    print_options(db, context, driver)

if __name__ == '__main__':
    main()
