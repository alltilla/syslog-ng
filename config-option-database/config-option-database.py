#!/usr/bin/python3
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

from yacc2graph import PluginExecutor
from argparse import ArgumentParser, REMAINDER

def parse_args():
    parser = ArgumentParser(description='Config Graph Executor')
    parser.add_argument('plugin', type=str, help='plugin to be executed')
    parser.add_argument('--debug', '-d', action='store_true', help='enable debug logging')
    parser.add_argument('arguments', nargs=REMAINDER, help='arguments passed to the plugin')
    return parser.parse_args()

def main():
    args = parse_args()
    cg = PluginExecutor(debug=args.debug)
    cg.run_plugin(args.plugin, args.arguments)

if __name__ == '__main__':
    main()
