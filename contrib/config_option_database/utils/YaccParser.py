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

import xml.etree.ElementTree as xml_parser
from subprocess import DEVNULL, Popen
from tempfile import NamedTemporaryFile
from dataclasses import dataclass


@dataclass(eq=True, order=True)
class Rule():
    expandable_symbol: str
    expansion: list


def _run_in_shell(command):
    proc = Popen(command, stderr=DEVNULL, stdout=DEVNULL)
    proc.wait()
    return proc.returncode == 0


def _create_temp_file_with_content(content):
    file = NamedTemporaryFile(mode='w')
    file.write(content)
    file.flush()
    return file


def _yacc2xml(yacc_content, xml_output_path):
    temp_yacc_file = _create_temp_file_with_content(yacc_content)
    try:
        if not _run_in_shell(['bison', '--xml=' + xml_output_path, '--output=/dev/null', temp_yacc_file.name]):
            raise Exception('Failed to convert to xml:\n{}\n'.format(yacc_content))
    except FileNotFoundError:
        raise Exception('bison executable not found')


def _xml2rules(filename):
    rules = []
    root = xml_parser.parse(filename).getroot()
    for rule in root.iter('rule'):
        expandable_symbol = rule.find('lhs').text
        expansion = [symbol.text for symbol in rule.find('rhs') if symbol.tag != 'empty']
        rules.append(Rule(expandable_symbol, expansion))
    return rules


def parse_yacc(yacc_content):
    xml_output = NamedTemporaryFile()
    _yacc2xml(yacc_content, xml_output.name)
    return _xml2rules(xml_output.name)
