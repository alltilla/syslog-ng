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

from utils.BisonGraph import BisonGraph
from utils.MergeYm import merge_grammars
from utils.OptionParser import path_to_options

def _make_types_terminal(graph):
    types = [
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

    for opt_type in types:
        if not opt_type in graph.get_nodes():
            continue
        graph.make_terminal(opt_type)

def _remove_code_blocks(graph):
    for node in filter(lambda x: x.startswith('$@'), graph.get_nodes()):
        graph.remove(node)

def get_driver_options():
    with NamedTemporaryFile(mode='w') as yaccfile:
        merge_grammars(yaccfile.name)
        graph = BisonGraph(yaccfile.name)
    _make_types_terminal(graph)
    _remove_code_blocks(graph)
    paths = filter(lambda path: path[0] in ['LL_CONTEXT_SOURCE', 'LL_CONTEXT_DESTINATION'], graph.get_paths())
    options = set()
    for path in paths:
        for option in path_to_options(path):
            options.add(option)
    return options

