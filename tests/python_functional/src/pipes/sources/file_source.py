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

from src.common.operations import open_file


class FileEntrypoint(Entrypoint):
    def __init__(self, file_path):
        self.file_path = file_path
        super(FileEntrypoint, self).__init__()

    def write_log(self, content, counter=1):
        with open_file(self.file_path, "a+") as f:
            for _ in range(counter):
                f.write(content)
                f.flush()


class FileConfigStatement(ConfigStatement):
    def __init__(self, pos_option, options):
        self.driver_name = "file"
        self.positional_parameters = [pos_option]
        self.options = options
        super(FileConfigStatement, self).__init__(self.driver_name, self.options)

    def get_path(self):
        return self.positional_parameters[0]

    def set_path(self, pos_option):
        self.self.positional_parameters[0] = pos_option

    def render(self):
        file_config_repr = "file (\n"
        file_config_repr += "  '%s'\n" % self.get_path()
        for option_name, option_name_value in self.options.items():
            file_config_repr += "  %s(%s)\n" % (option_name, option_name_value)
        file_config_repr += ");"
        return file_config_repr


class FileSource(Source):
    def __init__(self, file_name, **options):
        self.config = FileConfigStatement(file_name, options)
        self.stats = SourceStats(self.config.driver_name, self.config.get_path())
        self.entrypoint = FileEntrypoint(self.config.get_path())
        super(FileSource, self).__init__(self.config, self.stats, self.entrypoint)
