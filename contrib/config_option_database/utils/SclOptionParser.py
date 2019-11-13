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

from parse import parse


class SclOptionParser():
    BLOCK = 0
    KEYWORD = 1
    ATTRIBUTE = 2
    IN_SQUOTE = 3
    IN_DQUOTE = 4
    IN_NOQUOTE = 5
    END = 6

    def __init__(self, string):
        self.context = None
        self.driver = None
        self.keyword = None
        self.attribute = None

        self.state = SclOptionParser.BLOCK
        self.option_returned = False

        string = self._remove_comments(string)
        try:
            self.string = string[string.index('block'):]
        except ValueError:
            self.string = None

    def _remove_comments(self, string):
        lines = string.split('\n')
        return ''.join([line for line in lines if not line.lstrip().startswith('#')])

    def _parse_context_and_driver(self):
        tokens = parse('block {} {}({}', self.string)
        if tokens:
            self.context = tokens[0].strip()
            self.driver = tokens[1].strip()
            self.string = tokens[2]
            self.state = SclOptionParser.KEYWORD
            return True
        return False

    def _parse_keyword(self):
        self.keyword = None
        self.attribute = None
        string = self.string.lstrip()
        if string.startswith(')') or string.startswith('...'):
            self.state = SclOptionParser.END
            return True
        tokens = parse('{}({}', string)
        if tokens:
            keyword = tokens[0].strip()
            self.keyword = keyword
            self.string = tokens[1]
            self.state = SclOptionParser.ATTRIBUTE
            return True
        return False

    def _parse_attribute(self):
        self.string = self.string.lstrip()
        if self.string[0] == "'":
            self.string = self.string[1:]
            self.state = SclOptionParser.IN_SQUOTE
        elif self.string[0] == '"':
            self.string = self.string[1:]
            self.state = SclOptionParser.IN_DQUOTE
        elif self.string[0] == ')':
            self.string = self.string[1:]
            self.attribute = ('<n/a>',)
            self.state = SclOptionParser.KEYWORD
            return True
        else:
            self.state = SclOptionParser.IN_NOQUOTE
        return False

    def _parse_attribute_in_quote(self, quote):
        in_string = True
        while True:
            c = self.string[0]
            if in_string:
                if c == '\\':
                    self.string = self.string[2:]
                    continue
                self.string = self.string[1:]
                if c == quote:
                    in_string = False
            else:
                self.string = self.string[1:]
                if c == ')':
                    self.state = SclOptionParser.KEYWORD
                    self.attribute = ('<string>',)
                    return True

    def _guess_noquote_attribute(self, attribute):
        try:
            float(attribute)
            self.attribute = ('<number>',)
        except ValueError:
            if attribute.strip() in ['yes', 'no', 'on', 'off']:
                self.attribute = ('<yesno>',)
            else:
                self.attribute = ('<string>',)

    def _parse_attribute_in_noquote(self):
        attribute = ''
        while True:
            c = self.string[0]
            self.string = self.string[1:]
            if c == ')':
                self.state = SclOptionParser.KEYWORD
                self._guess_noquote_attribute(attribute)
                return True
            else:
                attribute += c

    def _parse_option(self):
        if self.state == SclOptionParser.BLOCK:
            if self._parse_context_and_driver():
                return self._parse_option()

        elif self.state == SclOptionParser.KEYWORD:
            if self._parse_keyword():
                return self._parse_option()

        elif self.state == SclOptionParser.ATTRIBUTE:
            if self._parse_attribute():
                return (self.context, self.driver, self.keyword, self.attribute, tuple())
            return self._parse_option()

        elif self.state == SclOptionParser.IN_SQUOTE:
            if self._parse_attribute_in_quote("'"):
                return (self.context, self.driver, self.keyword, self.attribute, tuple())

        elif self.state == SclOptionParser.IN_DQUOTE:
            if self._parse_attribute_in_quote('"'):
                return (self.context, self.driver, self.keyword, self.attribute, tuple())

        elif self.state == SclOptionParser.IN_NOQUOTE:
            if self._parse_attribute_in_noquote():
                return (self.context, self.driver, self.keyword, self.attribute, tuple())

        elif self.state == SclOptionParser.END:
            return None

        return False

    def get_next_option(self):
        if not self.string:
            return None
        option = self._parse_option()
        if option:
            self.option_returned = True
            return option
        if option is None and not self.option_returned:
            self.option_returned = True
            return (self.context, self.driver, '', tuple(), tuple())
        return None
