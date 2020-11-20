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
from src.pipes.sources.source import Source
from src.pipes.interfaces.config_statement import ConfigStatement
from src.pipes.interfaces.stats import SourceStats
from src.pipes.interfaces.io import Entrypoint

from src.driver_io.file.file import File
from pathlib2 import Path
import src.testcase_parameters.testcase_parameters as tc_parameters


class FileSourceEntrypoint(Entrypoint):
    def __init__(self, path):
        self.file = File(path)
        self.file.open("a+")
        super(FileSourceEntrypoint, self).__init__()

    def write_log(self, content):
        self.file.write(content)

    def write_logs(self, contents):
        for content in contents:
            self.write_log(content)

class FileSourceConfigStatement(ConfigStatement):
    def __init__(self, path, options):
        self.set_path(path)
        super(FileSourceConfigStatement, self).__init__("file", options)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = str(Path(tc_parameters.WORKING_DIR, path))

    def render(self):
        config_snippet = "file (\n"
        config_snippet += "  '{}'\n".format(self.get_path())
        for option_name, option_name_value in self.options.items():
            config_snippet += "  {}({})\n".format(option_name, option_name_value)
        config_snippet += ");"
        return config_snippet


class FileSource(Source):
    def __init__(self, file_name, **options):
        self.__config = FileSourceConfigStatement(file_name, options)
        self.__stats = SourceStats(self.__config.driver_name, self.__config.get_path())
        self.__entrypoint = FileSourceEntrypoint(self.__config.get_path())
        super(FileSource, self).__init__()

    @property
    def config(self):
        return self.__config

    @property
    def stats(self):
        raise self.__stats

    @property
    def entrypoint(self):
        return self.__entrypoint
