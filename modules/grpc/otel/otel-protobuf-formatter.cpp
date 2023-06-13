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

#include "otel-protobuf-formatter.hpp"

#include "compat/cpp-start.h"
#include "logmsg/type-hinting.h"
#include "value-pairs/value-pairs.h"
#include "compat/cpp-end.h"

using namespace google::protobuf;
using namespace opentelemetry::proto::common::v1;
using namespace opentelemetry::proto::collector::logs::v1;
using namespace opentelemetry::proto::logs::v1;

otel::MessageType
otel::get_message_type(LogMessage *msg)
{
  gssize len;
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, ".otel.type", &len, &type);

  if (type != LM_VT_STRING)
    return MessageType::UNKNOWN;

  if (strncmp(value, "log", len) == 0)
    return MessageType::LOG;

  if (strncmp(value, "metric", len) == 0)
    return MessageType::METRIC;

  if (strncmp(value, "span", len) == 0)
    return MessageType::SPAN;

  return MessageType::UNKNOWN;
}

static uint64_t
_get_uint64(LogMessage *msg, const gchar *name)
{
  gssize len;
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, &len, &type);

  if (type != LM_VT_INTEGER)
    return 0;

  return std::strtoull(value, nullptr, 10);
}

static int32_t
_get_int32(LogMessage *msg, const gchar *name)
{
  gssize len;
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, &len, &type);

  if (type != LM_VT_INTEGER)
    return 0;

  return std::strtol(value, nullptr, 10);
}

static uint32_t
_get_uint32(LogMessage *msg, const gchar *name)
{
  gssize len;
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, &len, &type);

  if (type != LM_VT_INTEGER)
    return 0;

  return std::strtoul(value, nullptr, 10);
}

static const gchar *
_get_string(LogMessage *msg, const gchar *name, gssize *len)
{
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, len, &type);

  if (type != LM_VT_STRING)
    return "";

  return value;
}

static const gchar *
_get_bytes(LogMessage *msg, const gchar *name, gssize *len)
{
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, len, &type);

  if (type != LM_VT_BYTES)
    {
      *len = 0;
      return NULL;
    }

  return value;
}

static void
_set_AnyValue(const gchar *value, gssize len, LogMessageValueType type, AnyValue *any_value,
              const gchar *name_for_error_log)
{
  GError *error = NULL;

  switch (type)
    {
    case LM_VT_PROTOBUF:
      any_value->ParseFromArray(value, len);
      break;
    case LM_VT_BYTES:
      any_value->set_bytes_value(value, len);
      break;
    case LM_VT_BOOLEAN:
    {
      gboolean b = FALSE;
      if (!type_cast_to_boolean(value, &b, &error))
        {
          msg_error("OpenTelemetry: Cannot parse boolean value, falling back to FALSE",
                    evt_tag_str("name", name_for_error_log),
                    evt_tag_str("value", value),
                    evt_tag_str("error", error->message));
          g_error_free(error);
        }
      any_value->set_bool_value(b);
      break;
    }
    case LM_VT_DOUBLE:
    {
      gdouble d = 0;
      if (!type_cast_to_double(value, &d, &error))
        {
          msg_error("OpenTelemetry: Cannot parse double value, falling back to 0",
                    evt_tag_str("name", name_for_error_log),
                    evt_tag_str("value", value),
                    evt_tag_str("error", error->message));
          g_error_free(error);
        }
      any_value->set_double_value(d);
      break;
    }
    case LM_VT_INTEGER:
    {
      gint64 ll = 0;
      if (!type_cast_to_int64(value, &ll, &error))
        {
          msg_error("OpenTelemetry: Cannot parse integer value, falling back to 0",
                    evt_tag_str("name", name_for_error_log),
                    evt_tag_str("value", value),
                    evt_tag_str("error", error->message));
          g_error_free(error);
        }
      any_value->set_int_value(ll);
      break;
    }
    case LM_VT_STRING:
      any_value->set_string_value(value, len);
      break;
    case LM_VT_NULL:
      break;
    default:
      msg_error("OpenTelemetry: Cannot parse value",
                evt_tag_str("name", name_for_error_log),
                evt_tag_str("value", value),
                evt_tag_str("type", log_msg_value_type_to_str(type)));
      break;
    }
}

static void
_get_and_set_AnyValue(LogMessage *msg, const gchar *name, AnyValue *any_value)
{
  LogMessageValueType type;
  gssize len;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, &len, &type);
  _set_AnyValue(value, len, type, any_value, name);
}

gboolean
_set_KeyValue_vp_fn(const gchar *name, LogMessageValueType type, const gchar *value,
                    gsize value_len, gpointer user_data)
{
  gpointer *args = (gpointer *) user_data;
  RepeatedPtrField<KeyValue> *key_values = (RepeatedPtrField<KeyValue> *) args[0];
  size_t prefix_len = *(size_t *) args[1];

  KeyValue *key_value = key_values->Add();
  key_value->set_key(name + prefix_len);
  _set_AnyValue(value, value_len, type, key_value->mutable_value(), name);

  return FALSE;
}

static void
_get_and_set_repeated_KeyValues(LogMessage *msg, const gchar *name_prefix, RepeatedPtrField<KeyValue> *key_values,
                                GlobalConfig *cfg)
{
  ValuePairs *vp = value_pairs_new(cfg);
  value_pairs_set_include_bytes(vp, TRUE);

  std::string glob_pattern = name_prefix;
  size_t prefix_len = glob_pattern.length();
  glob_pattern.append("*");
  value_pairs_add_glob_pattern(vp, glob_pattern.c_str(), TRUE);

  LogTemplateOptions template_options;
  log_template_options_defaults(&template_options);
  LogTemplateEvalOptions options = {&template_options, LTZ_LOCAL, 11, NULL, LM_VT_STRING};

  gpointer user_data[2];
  user_data[0] = key_values;
  user_data[1] = &prefix_len;

  value_pairs_foreach(vp, _set_KeyValue_vp_fn, msg, &options, &user_data);

  value_pairs_unref(vp);
}

static Resource
_get_resource_and_schema_url(LogMessage *msg, const gchar **schema_url, gssize *schema_url_len, GlobalConfig *cfg)
{
  Resource resource;

  resource.set_dropped_attributes_count(_get_uint32(msg, ".otel.resource.dropped_attributes_count"));
  _get_and_set_repeated_KeyValues(msg, ".otel.resource.attributes.", resource.mutable_attributes(), cfg);
  *schema_url = _get_string(msg, ".otel.resource.schema_url", schema_url_len);

  return resource;
}

static InstrumentationScope
_get_scope_and_schema_url(LogMessage *msg, const gchar **schema_url, gssize *schema_url_len, GlobalConfig *cfg)
{
  InstrumentationScope scope;

  const gchar *value;
  gssize len;

  value = _get_string(msg, ".otel.scope.name", &len);
  scope.set_name(value, len);
  value = _get_string(msg, ".otel.scope.version", &len);
  scope.set_version(value, len);
  scope.set_dropped_attributes_count(_get_uint32(msg, ".otel.scope.dropped_attributes_count"));
  _get_and_set_repeated_KeyValues(msg, ".otel.scope.attributes.", scope.mutable_attributes(), cfg);
  *schema_url = _get_string(msg, ".otel.scope.schema_url", schema_url_len);

  return scope;
}

static bool
_is_message_from_resource(const Resource &msg_resource, const gchar *msg_schema_url, gssize msg_schema_url_len,
                          const Resource &resource, const std::string &schema_url)
{
  return schema_url.length() == (std::size_t) msg_schema_url_len && schema_url == msg_schema_url &&
         util::MessageDifferencer().Equivalent(msg_resource, resource);
}

static bool
_is_message_from_scope(const InstrumentationScope &msg_scope, const gchar *msg_schema_url, gssize msg_schema_url_len,
                       const InstrumentationScope &scope, const std::string &schema_url)
{
  return schema_url.length() == (std::size_t) msg_schema_url_len && schema_url == msg_schema_url &&
         util::MessageDifferencer().Equivalent(msg_scope, scope);
}

static LogRecord *
_create_log_record(ExportLogsServiceRequest &request, LogMessage *msg, GlobalConfig *cfg)
{
  const gchar *msg_resource_schema_url;
  gssize msg_resource_schema_url_len;
  Resource msg_resource = _get_resource_and_schema_url(msg, &msg_resource_schema_url, &msg_resource_schema_url_len,
                                                       cfg);

  const gchar *msg_scope_schema_url;
  gssize msg_scope_schema_url_len;
  InstrumentationScope msg_scope = _get_scope_and_schema_url(msg, &msg_scope_schema_url, &msg_scope_schema_url_len,
                                                             cfg);

  ResourceLogs *resource_logs = nullptr;
  for (int i = 0; i < request.resource_logs_size(); i++)
    {
      ResourceLogs &possible_resource_logs = request.mutable_resource_logs()->at(i);
      if (_is_message_from_resource(msg_resource, msg_resource_schema_url, msg_resource_schema_url_len,
                                    possible_resource_logs.resource(), possible_resource_logs.schema_url()))
        {
          resource_logs = std::addressof(possible_resource_logs);
          break;
        }
    }
  if (resource_logs == nullptr)
    {
      resource_logs = request.add_resource_logs();
      resource_logs->mutable_resource()->CopyFrom(msg_resource);
      resource_logs->set_schema_url(msg_resource_schema_url);
    }

  ScopeLogs *scope_logs = nullptr;
  for (int i = 0; i < resource_logs->scope_logs_size(); i++)
    {
      ScopeLogs &possible_scope_logs = resource_logs->mutable_scope_logs()->at(i);
      if (_is_message_from_scope(msg_scope, msg_scope_schema_url, msg_scope_schema_url_len,
                                 possible_scope_logs.scope(), possible_scope_logs.schema_url()))
        {
          scope_logs = std::addressof(possible_scope_logs);
          break;
        }
    }
  if (scope_logs == nullptr)
    {
      scope_logs = resource_logs->add_scope_logs();
      scope_logs->mutable_scope()->CopyFrom(msg_scope);
      scope_logs->set_schema_url(msg_scope_schema_url);
    }

  return scope_logs->add_log_records();
}

bool
otel::protobuf::formatter::add_to_request(ExportLogsServiceRequest &request, LogMessage *msg, GlobalConfig *cfg)
{
  LogRecord *log_record = _create_log_record(request, msg, cfg);
  if (!log_record)
    {
      msg_error("OpenTelemetry: Failed to create log record");
      return false;
    }

  const gchar *value;
  gssize len;

  log_record->set_time_unix_nano(_get_uint64(msg, ".otel.log.time_unix_nano"));
  log_record->set_observed_time_unix_nano(_get_uint64(msg, ".otel.log.observed_time_unix_nano"));

  int32_t severity_number_int = _get_int32(msg, ".otel.log.severity_number");
  SeverityNumber severity_number = SeverityNumber_IsValid(severity_number_int) ? (SeverityNumber) severity_number_int \
                                   : SEVERITY_NUMBER_UNSPECIFIED;
  log_record->set_severity_number(severity_number);

  value = _get_string(msg, ".otel.log.severity_text", &len);
  log_record->set_severity_text(value, len);

  _get_and_set_AnyValue(msg, ".otel.log.body", log_record->mutable_body());
  _get_and_set_repeated_KeyValues(msg, ".otel.log.attributes.", log_record->mutable_attributes(), cfg);
  log_record->set_dropped_attributes_count(_get_uint32(msg, ".otel.log.dropped_attributes_count"));
  log_record->set_flags(_get_uint32(msg, ".otel.log.flags"));

  value = _get_bytes(msg, ".otel.log.trace_id", &len);
  log_record->set_trace_id(value, len);

  value = _get_bytes(msg, ".otel.log.span_id", &len);
  log_record->set_span_id(value, len);

  return true;
}
