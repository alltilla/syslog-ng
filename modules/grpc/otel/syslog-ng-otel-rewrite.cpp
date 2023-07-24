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

#include "syslog-ng-otel-rewrite.hpp"

#include "compat/cpp-start.h"
#include "logmsg/type-hinting.h"
#include "compat/cpp-end.h"

#define get_SyslogNgOtelRewrite(s) (((SyslogNgOtelRewriteWrapper *) s)->cpp)

struct SyslogNgOtelRewriteWrapper_
{
  LogRewrite super;
  syslogng::grpc::otel::SyslogNgOtelRewrite *cpp;
};

static LogTemplate *
_create_template(const char *template_string, GlobalConfig *cfg)
{
  LogTemplate *template_obj = log_template_new(cfg, NULL);
  g_assert(log_template_compile(template_obj, template_string, NULL));
  return template_obj;
}

syslogng::grpc::otel::SyslogNgOtelRewrite::SyslogNgOtelRewrite(GlobalConfig *cfg)
{
  vp = value_pairs_new(cfg);
  value_pairs_add_scope(vp, "all-nv-pairs");
  value_pairs_set_include_bytes(vp, TRUE);

  LogTemplate *pri_template = _create_template("${PRI}", cfg);
  value_pairs_add_pair(vp, "PRI", pri_template);
  log_template_unref(pri_template);

  LogTemplate *tags_template = _create_template("${TAGS}", cfg);
  value_pairs_add_pair(vp, "TAGS", tags_template);
  log_template_unref(tags_template);

  value_pairs_add_glob_pattern(vp, "MESSAGE", FALSE);
  value_pairs_add_glob_pattern(vp, "SOURCE", FALSE);

  log_template_options_defaults(&template_options);
  template_eval_options = {&template_options, LTZ_LOCAL, -1, NULL, LM_VT_STRING};

  name_buffer.assign(".otel.log.attributes.");
  name_prefix_len = name_buffer.length();
}

syslogng::grpc::otel::SyslogNgOtelRewrite::~SyslogNgOtelRewrite()
{
  value_pairs_unref(vp);
}

static bool
_is_number(const char *name)
{
  for (int i = 0; i < 3; i++)
    {
      if (!g_ascii_isdigit(name[i]))
        break;

      if (name[i+1] == '\0')
        return true;
    }

  return false;
}

static void
_calculate_new_name(const char *name, std::string *name_buffer, size_t name_prefix_len, LogMessageValueType type)
{
  name_buffer->resize(name_prefix_len);
  name_buffer->append("sng.");
  name_buffer->append(log_msg_value_type_to_str(type));
  name_buffer->append(".");
  name_buffer->append(name);
}

static gboolean
_format_nvpairs_for_otel(const gchar *name, LogMessageValueType type, const gchar *value,
                         gsize value_len, gpointer user_data)
{
  gpointer *args = (gpointer *) user_data;
  LogMessage *msg = (LogMessage *) args[0];
  std::string *name_buffer = (std::string *) args[1];
  size_t name_prefix_len = *(size_t *) args[2];

  if (_is_number(name))
    return FALSE;

  _calculate_new_name(name, name_buffer, name_prefix_len, type);
  NVHandle new_handle = log_msg_get_value_handle(name_buffer->c_str());

  gssize existing_value_len;
  if (log_msg_get_value_if_set(msg, new_handle, &existing_value_len))
    {
      msg_info("syslog-ng-otel rewrite: Error while renaming name-value pair, destination nv-pair already exists. "
               "This should only happen in extremely rare cases. Please do not use name-value pairs starting with "
               ".otel.log.attributes.sng. Overwriting",
               evt_tag_msg_reference(msg),
               evt_tag_str("source_name", name),
               evt_tag_str("destination_name", name_buffer->c_str()));
    }

  /* Format everything as bytes, the type hint is present in the name */
  log_msg_set_value_with_type(msg, new_handle, value, value_len, LM_VT_BYTES);
  log_msg_unset_value_by_name(msg, name);

  return FALSE;
}

void
syslogng::grpc::otel::SyslogNgOtelRewrite::process(LogMessage *msg)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* .otel.log.attributes.sng.<...> */
  gpointer user_data[3];
  user_data[0] = msg;
  user_data[1] = &name_buffer;
  user_data[2] = &name_prefix_len;
  value_pairs_foreach(vp, _format_nvpairs_for_otel, msg, &template_eval_options, &user_data);

  /* .otel.type */
  log_msg_set_value_by_name_with_type(msg, ".otel.type", "log", -1, LM_VT_STRING);

  /* .otel.log.body */
  gssize message_len;
  LogMessageValueType message_type;
  log_msg_get_value_with_type(msg, LM_V_MESSAGE, &message_len, &message_type);
  NVHandle message_handle = log_msg_get_value_handle(".otel.log.body");
  log_msg_set_value_indirect_with_type(msg, message_handle, LM_V_MESSAGE, 0, message_len, message_type);

  /* .otel.log.time_unix_nano */
  const guint64 time_unix_nano = msg->timestamps[LM_TS_STAMP].ut_sec * 1000000000 +
                                 msg->timestamps[LM_TS_STAMP].ut_usec * 1000;
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, time_unix_nano);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.time_unix_nano", number_buf, -1, LM_VT_INTEGER);

  /* .otel.log.observed_time_unix_nano */
  const guint64 observed_time_unix_nano = msg->timestamps[LM_TS_RECVD].ut_sec * 1000000000 +
                                          msg->timestamps[LM_TS_RECVD].ut_usec * 1000;
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, observed_time_unix_nano);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.observed_time_unix_nano", number_buf, -1, LM_VT_INTEGER);
}

static void
_free(LogPipe *s)
{
  delete get_SyslogNgOtelRewrite(s);
  log_rewrite_free_method(s);
}

static LogPipe *
_clone(LogPipe *s)
{
  SyslogNgOtelRewriteWrapper *self = (SyslogNgOtelRewriteWrapper *) s;

  LogRewrite *cloned = syslog_ng_otel_rewrite_new(s->cfg);
  log_rewrite_clone_method(cloned, &self->super);

  return &cloned->super;
}

static void
_process(LogRewrite *s, LogMessage **pmsg, const LogPathOptions *path_options)
{
  SyslogNgOtelRewriteWrapper *self = (SyslogNgOtelRewriteWrapper *) s;

  LogMessage *msg = log_msg_make_writable(pmsg, path_options);
  get_SyslogNgOtelRewrite(s)->process(msg);
}

LogRewrite *
syslog_ng_otel_rewrite_new(GlobalConfig *cfg)
{
  SyslogNgOtelRewriteWrapper *self = g_new0(SyslogNgOtelRewriteWrapper, 1);

  self->cpp = new syslogng::grpc::otel::SyslogNgOtelRewrite(cfg);

  log_rewrite_init_instance(&self->super, cfg);
  self->super.super.free_fn = _free;
  self->super.super.clone = _clone;
  self->super.process = _process;
  return &self->super;
}