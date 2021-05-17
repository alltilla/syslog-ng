#!/usr/bin/env python
#############################################################################
# Copyright (c) 2020 One Identity
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
from pathlib2 import Path
from psutil import TimeoutExpired

import src.testcase_parameters.testcase_parameters as tc_parameters
from src.executors.process_executor import ProcessExecutor
from src.executors.params_builder import build_args_for_executor, ParamMode


class Loggen(object):

    AVAILABLE_LOGGEN_PARAMS = {
        "inet": ("--inet", ParamMode.SET),
        "unix": ("--unix", ParamMode.SET),
        "stream": ("--stream", ParamMode.SET),
        "dgram": ("--dgram", ParamMode.SET),
        "use_ssl": ("--use-ssl", ParamMode.SET),
        "dont_parse": ("--dont-parse", ParamMode.SET),
        "read_file": ("--read-file=", ParamMode.CONCAT),
        "skip_tokens": ("--skip_tokens=", ParamMode.CONCAT),
        "loop_reading": ("--loop-reading", ParamMode.SET),
        "rate": ("--rate=", ParamMode.CONCAT),
        "interval": ("--interval=", ParamMode.CONCAT),
        "permanent": ("--permanent", ParamMode.SET),
        "syslog_proto": ("--syslog-proto", ParamMode.SET),
        "proxied": ("--proxied", ParamMode.SET),
        "sdata": ("--sdata", ParamMode.SET),
        "no_framing": ("--no-framing", ParamMode.SET),
        "active_connections": ("--active-connections=", ParamMode.CONCAT),
        "idle_connections": ("--idle-connections=", ParamMode.CONCAT),
        "ipv6": ("--ipv6", ParamMode.SET),
        "debug": ("--debug", ParamMode.SET),
        "number": ("--number=", ParamMode.CONCAT),
        "csv": ("--csv", ParamMode.SET),
        "quiet": ("--quiet", ParamMode.CONCAT),
        "size": ("--size=", ParamMode.CONCAT),
    }

    instanceIndex = -1
    @staticmethod
    def __get_new_instance_index():
        Loggen.instanceIndex += 1
        return Loggen.instanceIndex

    def __init__(self):
        self.loggen_proc = None
        self.loggen_bin_path = tc_parameters.INSTANCE_PATH.get_loggen_bin()

    def start(
        self, target, port, inet=None, unix=None, stream=None, dgram=None, use_ssl=None, dont_parse=None, read_file=None, skip_tokens=None, loop_reading=None,
        rate=None, interval=None, permanent=None, syslog_proto=None, proxied=None, sdata=None, no_framing=None, active_connections=None,
        idle_connections=None, ipv6=None, debug=None, number=None, csv=None, quiet=None, size=None,
    ):

        if self.loggen_proc is not None and self.loggen_proc.is_running():
            raise Exception("Loggen is already running, you shouldn't call start")

        loggen_args = build_args_for_executor(Loggen.AVAILABLE_LOGGEN_PARAMS, ["self", "target", "port"], **locals())

        instanceIndex = Loggen.__get_new_instance_index()
        self.loggen_stdout_path = Path(tc_parameters.WORKING_DIR, "loggen_stdout_{}".format(instanceIndex))
        self.loggen_stderr_path = Path(tc_parameters.WORKING_DIR, "loggen_stderr_{}".format(instanceIndex))

        self.loggen_proc = ProcessExecutor().start(
            [self.loggen_bin_path] + loggen_args + [target, port],
            self.loggen_stdout_path,
            self.loggen_stderr_path,
        )

        return self.loggen_proc

    def stop(self):
        if self.loggen_proc is None:
            return

        self.loggen_proc.terminate()
        try:
            self.loggen_proc.wait(4)
        except TimeoutExpired:
            self.loggen_proc.kill()

        self.loggen_proc = None

    def get_sent_message_count(self):
        if not self.loggen_stderr_path.exists():
            return 0

        # loggen puts the count= messages to the stderr
        f = open(str(self.loggen_stderr_path), "r")
        content = f.read()
        f.close()

        start_pattern = "count="
        if start_pattern not in content:
            return 0
        index_start = content.rindex(start_pattern) + len(start_pattern)

        end_pattern = ", "
        if end_pattern not in content:
            return 0
        index_end = content.find(end_pattern, index_start)

        return int(content[index_start:index_end])
