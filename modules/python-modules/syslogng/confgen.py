#############################################################################
# Copyright (c) 2022 Balazs Scheidler <bazsi77@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# As an additional exemption you are allowed to compile & link against the
# OpenSSL libraries as published by the OpenSSL project. See the file
# COPYING for details.
#
#############################################################################

try:
    from _syslogng import register_config_generator
except ImportError:
    def register_config_generator(context, name, config_generator):
        pass

try:
    import jinja2

    def register_jinja_config_generator(context, name, template):
        def jinja_confgen_fn(args):
            jinja2_env = jinja2.Environment()
            jinja2_template = jinja2_env.from_string(template)
            return jinja2_template.render(args=args)
        register_config_generator(context, name, jinja_confgen_fn)
except ImportError:
    def register_jinja_config_generator(context, name, template):
        pass
