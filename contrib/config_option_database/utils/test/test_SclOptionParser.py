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

from utils.SclOptionParser import SclOptionParser


def test_get_next_option():
    test_string = r'''
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

# Use this block to do something

@requires http
@requires json-plugin
@requires basicfuncs

block destination test            (
  opt1()  
opt2(  '')  
  opt3  (    '\')' )
  opt4(""  )
     
   
opt5( "\\   \")) ()())) ")
  opt6(yes   )   opt7  (  123.456  )
  opt8    (   567890) opt9(  almafa  )

  ...)
{
    tcp();
};
'''
    expected = [
        ('destination', 'test', 'opt1', ('<n/a>',), tuple()),
        ('destination', 'test', 'opt2', ('<string>',), tuple()),
        ('destination', 'test', 'opt3', ('<string>',), tuple()),
        ('destination', 'test', 'opt4', ('<string>',), tuple()),
        ('destination', 'test', 'opt5', ('<string>',), tuple()),
        ('destination', 'test', 'opt6', ('<yesno>',), tuple()),
        ('destination', 'test', 'opt7', ('<number>',), tuple()),
        ('destination', 'test', 'opt8', ('<number>',), tuple()),
        ('destination', 'test', 'opt9', ('<string>',), tuple())
    ]

    scl_parser = SclOptionParser(test_string)
    actual = []
    while True:
        option = scl_parser.get_next_option()
        if not option:
            break
        actual.append(option)

    assert expected == actual


def test_scl_with_no_option():
    test_string = r'block source test(){};'

    scl_parser = SclOptionParser(test_string)
    assert scl_parser.get_next_option() == ('source', 'test', '', tuple(), tuple())
    assert scl_parser.get_next_option() is None


def test_no_block():
    test_string = r'''
template-function "test" "$(format-json --pair @timestamp='${R_ISODATE}'";
'''

    scl_parser = SclOptionParser(test_string)
    assert scl_parser.get_next_option() is None


def test_invalid_block():
    test_string = 'blockparser test(opt1("alma")) {'

    scl_parser = SclOptionParser(test_string)
    assert scl_parser.get_next_option() is None


def test_invalid_option():
    test_string = 'block source test("alma") {'

    scl_parser = SclOptionParser(test_string)
    assert scl_parser.get_next_option() is None
