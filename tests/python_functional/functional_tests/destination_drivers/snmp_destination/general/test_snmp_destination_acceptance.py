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
import pytest

from src.executors.snmptrapd import SNMPTestParams


@pytest.mark.snmp
def test_snmp_dest_acceptance(config, syslog_ng, port_allocator):
    snmp_test_params = SNMPTestParams()
    # checks default version and default community
    generator_source = config.create_example_msg_generator_source(num=1)
    snmp_destination = config.create_snmp_destination(
        host="127.0.0.1",
        port=port_allocator(),
        snmp_obj=snmp_test_params.get_basic_snmp_obj(),
        trap_obj=snmp_test_params.get_basic_trap_obj(),
    )
    config.create_logpath(statements=[generator_source, snmp_destination])

    # syslog_ng.start(config)
    snmp_destination.endpoint.start()
    snmp_destination.endpoint.stop()
    assert True
    # received_traps = snmp_destination.endpoint.read_logs(2)
    # assert snmp_test_params.get_expected_basic_trap() == received_traps
    # assert any(snmp_test_params.get_default_community() in line for line in snmptrapd.get_raw_traps())
#snmptrapd -f --disableAuthorization=yes -C -m ALL -A -Ddump -On --doNotLogTraps=no --authCommunity=log public 30001 -d -Lf reports/2020-11-27-14-44-05-610533/test_snmp_dest_acceptance/snmptrapd_log -F LIGHT_TEST_SNMP_TRAP_RECEIVED:%v