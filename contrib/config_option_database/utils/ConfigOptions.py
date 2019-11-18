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

from pathlib import Path
from tempfile import NamedTemporaryFile

from utils.BisonGraph import BisonGraph
from utils.OptionParser import path_to_options


ROOT_DIR = Path(__file__).parents[3]


def _merge_grammars(grammar_files, output_filepath):
    declarations = set()
    blocks = r'%%' + '\n'

    for grammar_file in grammar_files:
        with grammar_file.open() as f:
            in_block = False
            for line in f:
                if line.startswith('%token') or line.startswith(r'%left') or line.startswith('%type'):
                    declarations.add(line)
                elif line.startswith(r'%%'):
                    in_block = not in_block
                elif in_block:
                    blocks += line
    blocks += r'%%' + '\n'

    with open(output_filepath, 'w') as f:
        f.write(''.join(declarations) + blocks)


def _make_types_terminal(graph):
    types = [
        'nonnegative_integer',
        'path',
        'positive_integer',
        'string',
        'string_list',
        'string_or_number',
        'template_content',
        'yesno'
    ]

    for node in types:
        graph.make_terminal(node)


def _process_helpers(graph):
    helpers = [
        'inner_dest',
        'inner_source',
        'filter_content',
        'parser_content'
    ]
    connections = [
        ('inner_dest', 'LL_CONTEXT_INNER_DEST'),
        ('inner_source', 'LL_CONTEXT_INNER_SRC'),
    ]

    for node in helpers:
        graph.make_terminal(node)
    for from_node, to_node in connections:
        for parent in graph.get_parents(to_node):
            graph.add_arc(from_node, parent)
        graph.remove(to_node)


def _remove_code_blocks(graph):
    for node in filter(lambda x: x.startswith('$@'), graph.get_nodes()):
        graph.remove(node)


def _remove_ifdef(graph):
    nodes = graph.get_nodes()
    ifdefs = ['KW_IFDEF', 'KW_ENDIF']
    for ifdef in filter(lambda x: x in nodes, ifdefs):
        for parent in graph.get_parents(ifdef):
            graph.remove(parent)


def _init_graph(graph):
    _make_types_terminal(graph)
    _process_helpers(graph)
    _remove_code_blocks(graph)
    _remove_ifdef(graph)


def _get_grammar_and_parser_files():
    files = []
    grammar_files = []
    grammar_files.extend(list((ROOT_DIR / 'modules').rglob('*.ym')))
    grammar_files.extend(list((ROOT_DIR / 'lib').rglob('*.ym')))
    for grammar_file in grammar_files:
        parser_file = Path(grammar_file.parent / (grammar_file.name[:-11] + '-parser.c'))
        files.append((grammar_file, parser_file))
    return files


def _add_necessary_parser_files(parser_file):
    parser_files = [
        ROOT_DIR / 'lib' / 'cfg-parser.c',
        ROOT_DIR / 'modules' / 'diskq' / 'diskq-parser.c',
        ROOT_DIR / 'modules' / 'hook-commands' / 'hook-commands-parser.c',
        parser_file
    ]
    return parser_files


def _add_necessary_grammar_files(grammar_file):
    grammar_files = [
        ROOT_DIR / 'lib' / 'cfg-grammar.y',
        ROOT_DIR / 'modules' / 'diskq' / 'diskq-grammar.ym',
        ROOT_DIR / 'modules' / 'hook-commands' / 'hook-commands-grammar.ym',
        grammar_file
    ]
    return grammar_files


def get_driver_options():
    contexts = [
        'LL_CONTEXT_SOURCE',
        'LL_CONTEXT_DESTINATION',
    ]
    options = set()
    for grammar_file, parser_file in _get_grammar_and_parser_files():
        with NamedTemporaryFile(mode='w') as yaccfile:
            _merge_grammars(_add_necessary_grammar_files(grammar_file), yaccfile.name)
            graph = BisonGraph(yaccfile.name)
        _init_graph(graph)
        for path in filter(lambda path: len(path) > 0 and path[0] in contexts, graph.get_paths()):
            options |= path_to_options(path, _add_necessary_parser_files(parser_file))
    return options
