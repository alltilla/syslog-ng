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


class FileSourceEntrypoint(Entrypoint):
    def __init__(self, path):
        self.path = path
        super(FileSourceEntrypoint, self).__init__()

    def write_log(self, content, counter=1):
        with open_file(self.path, "a+") as f:
            for _ in range(counter):
                f.write(content)
                f.flush()


class FileSourceConfigStatement(ConfigStatement):
    def __init__(self, path, options):
        self.set_path(path)
        super(FileSourceConfigStatement, self).__init__("file", options)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def render(self):
        config_snippet = "file (\n"
        config_snippet += "  '{}'\n".format(self.get_path())
        for option_name, option_name_value in self.options.items():
            config_snippet += "  {}({})\n".format(option_name, option_name_value)
        config_snippet += ");"
        return config_snippet


class FileSource(Source):
    def __init__(self, file_name, **options):
        config = FileSourceConfigStatement(file_name, options)
        stats = SourceStats(config.driver_name, config.get_path())
        entrypoint = FileSourceEntrypoint(config.get_path())
        super(FileSource, self).__init__(config, stats, entrypoint)
