/*
 * Copyright (c) 2023 Attila Szakacs
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 2 as published
 * by the Free Software Foundation, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * As an additional exemption you are allowed to compile & link against the
 * OpenSSL libraries as published by the OpenSSL project. See the file
 * COPYING for details.
 *
 */

#ifndef SYSLOG_NG_OTEL_REWRITE_HPP
#define SYSLOG_NG_OTEL_REWRITE_HPP

#include "compat/cpp-start.h"
#include "logmsg/logmsg.h"
#include "value-pairs/value-pairs.h"
#include "compat/cpp-end.h"

#include "syslog-ng-otel-rewrite.h"

#include <list>
#include <string>

namespace syslogng {
namespace grpc {
namespace otel {

class SyslogNgOtelRewrite
{
public:
  SyslogNgOtelRewrite(GlobalConfig *cfg);
  ~SyslogNgOtelRewrite();

  void process(LogMessage *msg);

private:
  ValuePairs *vp;
  LogTemplateOptions template_options;
  LogTemplateEvalOptions template_eval_options;

  std::string name_buffer;
  size_t name_prefix_len;
};

}
}
}

#endif
