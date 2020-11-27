#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2018 Balabit
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
import logging

from src.common.blocking import wait_until_true
from src.common.blocking import wait_until_true_custom
from src.common.operations import open_file

from pathlib2 import Path

logger = logging.getLogger(__name__)


class File(object):
    def __init__(self, file_path):
        self.path = Path(file_path)
        self.__opened_file = None

    def __del__(self):
        if self.is_opened():
            self.close()

    def wait_for_creation(self):
        file_created = wait_until_true(self.path.exists)
        if file_created:
            logger.debug("File has been created:\n{}".format(self.path))
        else:
            logger.debug("File not created:\n{}".format(self.path))
        return file_created

    def open(self, mode):
        self.__opened_file = open_file(self.path, mode)
        return self.__opened_file

    def close(self):
        self.__opened_file.close()
        self.__opened_file = None

    def is_opened(self):
        return self.__opened_file is not None

    def read(self): # TODO: rename to readline
        if not self.is_opened():
            raise Exception("File was not opened before trying to read from it.")
        return self.__opened_file.readline()

    def read_all(self):
        content = ""
        while True:
            buffer = self.read()
            if buffer == "":
                break
            content += buffer
        return content

    def write(self, content):
        self.__opened_file.write(content)
        self.__opened_file.flush()

    def wait_for_lines(self, lines, timeout, poll_freq):
        def find_lines_in_file(lines_to_find, lines_found, f):
            line_read = f.read()
            for line_to_find in lines_to_find:
                if line_to_find in line_read:
                    lines_found.append(line_read)
                    lines_to_find.remove(line_to_find)
                    break
            everything_is_found = lines_to_find == []
            return everything_is_found

        lines_found = []
        if not wait_until_true_custom(find_lines_in_file, (lines, lines_found, self), timeout=timeout, poll_freq=poll_freq):
            raise Exception("Could not found all lines. Lines remaining: {}".format(lines))
        return lines_found

    def wait_for_number_of_lines(self, number_of_lines, timeout, poll_freq):
        return self.wait_for_lines(["\n"] * number_of_lines, timeout, poll_freq)
