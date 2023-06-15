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

#include "google/protobuf/util/message_differencer.h"

#include "compat/cpp-start.h"
#include "logmsg/type-hinting.h"
#include "value-pairs/value-pairs.h"
#include "compat/cpp-end.h"

using namespace google::protobuf;
using namespace opentelemetry::proto::common::v1;
using namespace opentelemetry::proto::resource::v1;
using namespace opentelemetry::proto::collector::logs::v1;
using namespace opentelemetry::proto::collector::metrics::v1;
using namespace opentelemetry::proto::collector::trace::v1;
using namespace opentelemetry::proto::logs::v1;
using namespace opentelemetry::proto::metrics::v1;
using namespace opentelemetry::proto::trace::v1;

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

static bool
_get_bool(LogMessage *msg, const gchar *name)
{
  gssize len;
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, &len, &type);

  if (type != LM_VT_BOOLEAN)
    return false;

  gboolean b = false;
  if (!type_cast_to_boolean(value, &b, NULL))
    return false;

  return b;
}

static double
_get_double(LogMessage *msg, const gchar *name)
{
  gssize len;
  LogMessageValueType type;
  const gchar *value = log_msg_get_value_by_name_with_type(msg, name, &len, &type);

  if (type != LM_VT_DOUBLE)
    return 0;

  gdouble d = 0;
  if (!type_cast_to_double(value, &d, NULL))
    return 0;

  return d;
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

static Metric *
_create_metric(ExportMetricsServiceRequest &request, LogMessage *msg, ScopeMetrics **related_scope_metrics,
               GlobalConfig *cfg)
{
  const gchar *msg_resource_schema_url;
  gssize msg_resource_schema_url_len;
  Resource msg_resource = _get_resource_and_schema_url(msg, &msg_resource_schema_url, &msg_resource_schema_url_len,
                                                       cfg);

  const gchar *msg_scope_schema_url;
  gssize msg_scope_schema_url_len;
  InstrumentationScope msg_scope = _get_scope_and_schema_url(msg, &msg_scope_schema_url, &msg_scope_schema_url_len,
                                                             cfg);

  ResourceMetrics *resource_metrics = nullptr;
  for (int i = 0; i < request.resource_metrics_size(); i++)
    {
      ResourceMetrics &possible_resource_metrics = request.mutable_resource_metrics()->at(i);
      if (_is_message_from_resource(msg_resource, msg_resource_schema_url, msg_resource_schema_url_len,
                                    possible_resource_metrics.resource(), possible_resource_metrics.schema_url()))
        {
          resource_metrics = std::addressof(possible_resource_metrics);
          break;
        }
    }
  if (resource_metrics == nullptr)
    {
      resource_metrics = request.add_resource_metrics();
      resource_metrics->mutable_resource()->CopyFrom(msg_resource);
      resource_metrics->set_schema_url(msg_resource_schema_url);
    }

  ScopeMetrics *scope_metrics = nullptr;
  for (int i = 0; i < resource_metrics->scope_metrics_size(); i++)
    {
      ScopeMetrics &possible_scope_metrics = resource_metrics->mutable_scope_metrics()->at(i);
      if (_is_message_from_scope(msg_scope, msg_scope_schema_url, msg_scope_schema_url_len,
                                 possible_scope_metrics.scope(), possible_scope_metrics.schema_url()))
        {
          scope_metrics = std::addressof(possible_scope_metrics);
          break;
        }
    }
  if (scope_metrics == nullptr)
    {
      scope_metrics = resource_metrics->add_scope_metrics();
      scope_metrics->mutable_scope()->CopyFrom(msg_scope);
      scope_metrics->set_schema_url(msg_scope_schema_url);
    }

  *related_scope_metrics = scope_metrics;

  return scope_metrics->add_metrics();
}

static void
_add_exemplars(LogMessage *msg, std::string &key_buffer, RepeatedPtrField<Exemplar> *exemplars, GlobalConfig *cfg)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];
  size_t orig_len = key_buffer.length();

  gssize len;
  LogMessageValueType type;
  const gchar *value;
  GError *error = NULL;

  uint64_t idx = 0;
  while (true)
    {
      key_buffer.resize(orig_len);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t len_with_idx = key_buffer.length();

      key_buffer.append("value");
      value = log_msg_get_value_by_name_with_type(msg, key_buffer.c_str(), &len, &type);
      if (type == LM_VT_NULL)
        break;

      Exemplar *exemplar = exemplars->Add();

      if (type == LM_VT_INTEGER)
        {
          gint64 ll = 0;
          if (!type_cast_to_int64(value, &ll, &error))
            {
              msg_error("OpenTelemetry: Cannot parse integer value, falling back to 0",
                        evt_tag_str("name", key_buffer.c_str()),
                        evt_tag_str("value", value),
                        evt_tag_str("error", error->message));
              g_error_free(error);
            }
          exemplar->set_as_int(ll);
        }
      else if (type == LM_VT_DOUBLE)
        {
          gdouble d = 0;
          if (!type_cast_to_double(value, &d, &error))
            {
              msg_error("OpenTelemetry: Cannot parse double value, falling back to 0",
                        evt_tag_str("name", key_buffer.c_str()),
                        evt_tag_str("value", value),
                        evt_tag_str("error", error->message));
              g_error_free(error);
            }
          exemplar->set_as_double(d);
        }
      else
        {
          msg_error("OpenTelemetry: Cannot parse value, unexpected log message type, falling back to 0",
                    evt_tag_str("name", key_buffer.c_str()),
                    evt_tag_str("value", value),
                    evt_tag_str("type", log_msg_value_type_to_str(type)));
          exemplar->set_as_int(0);
        }

      key_buffer.resize(len_with_idx);
      key_buffer.append("filtered_attributes.");
      _get_and_set_repeated_KeyValues(msg, key_buffer.c_str(), exemplar->mutable_filtered_attributes(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("time_unix_nano");
      exemplar->set_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("span_id");
      value = _get_bytes(msg, key_buffer.c_str(), &len);
      exemplar->set_span_id(value, len);

      key_buffer.resize(len_with_idx);
      key_buffer.append("trace_id");
      value = _get_bytes(msg, key_buffer.c_str(), &len);
      exemplar->set_trace_id(value, len);

      idx++;
    }

}

static void
_add_number_data_points(LogMessage *msg, const char *prefix, RepeatedPtrField<NumberDataPoint> *data_points,
                        GlobalConfig *cfg)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];
  std::string key_buffer = prefix;
  size_t orig_len = key_buffer.length();

  gssize len;
  LogMessageValueType type;
  const gchar *value;
  GError *error = NULL;

  uint64_t idx = 0;
  while (true)
    {
      key_buffer.resize(orig_len);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t len_with_idx = key_buffer.length();

      key_buffer.append("value");
      value = log_msg_get_value_by_name_with_type(msg, key_buffer.c_str(), &len, &type);
      if (type == LM_VT_NULL)
        break;

      NumberDataPoint *data_point = data_points->Add();

      if (type == LM_VT_INTEGER)
        {
          gint64 ll = 0;
          if (!type_cast_to_int64(value, &ll, &error))
            {
              msg_error("OpenTelemetry: Cannot parse integer value, falling back to 0",
                        evt_tag_str("name", key_buffer.c_str()),
                        evt_tag_str("value", value),
                        evt_tag_str("error", error->message));
              g_error_free(error);
            }
          data_point->set_as_int(ll);
        }
      else if (type == LM_VT_DOUBLE)
        {
          gdouble d = 0;
          if (!type_cast_to_double(value, &d, &error))
            {
              msg_error("OpenTelemetry: Cannot parse double value, falling back to 0",
                        evt_tag_str("name", key_buffer.c_str()),
                        evt_tag_str("value", value),
                        evt_tag_str("error", error->message));
              g_error_free(error);
            }
          data_point->set_as_double(d);
        }
      else
        {
          msg_error("OpenTelemetry: Cannot parse value, unexpected log message type, falling back to 0",
                    evt_tag_str("name", key_buffer.c_str()),
                    evt_tag_str("value", value),
                    evt_tag_str("type", log_msg_value_type_to_str(type)));
          data_point->set_as_int(0);
        }

      key_buffer.resize(len_with_idx);
      key_buffer.append("attributes.");
      _get_and_set_repeated_KeyValues(msg, key_buffer.c_str(), data_point->mutable_attributes(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("start_time_unix_nano");
      data_point->set_start_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("time_unix_nano");
      data_point->set_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("exemplars.");
      _add_exemplars(msg, key_buffer, data_point->mutable_exemplars(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("flags");
      data_point->set_flags(_get_uint32(msg, key_buffer.c_str()));

      idx++;
    }
}

static void
_set_metric_gauge_values(LogMessage *msg, Gauge *gauge, GlobalConfig *cfg)
{
  _add_number_data_points(msg, ".otel.metric.data.gauge.data_points.", gauge->mutable_data_points(), cfg);
}

static void
_set_metric_sum_values(LogMessage *msg, Sum *sum, GlobalConfig *cfg)
{
  _add_number_data_points(msg, ".otel.metric.data.sum.data_points.", sum->mutable_data_points(), cfg);

  int32_t aggregation_temporality_int = _get_int32(msg, ".otel.metric.data.sum.aggregation_temporality");
  AggregationTemporality aggregation_temporality = AggregationTemporality_IsValid(aggregation_temporality_int) \
                                                   ? (AggregationTemporality) aggregation_temporality_int \
                                                   : AGGREGATION_TEMPORALITY_UNSPECIFIED;
  sum->set_aggregation_temporality(aggregation_temporality);

  sum->set_is_monotonic(_get_bool(msg, ".otel.metric.data.sum.is_monotonic"));
}

static void
_add_histogram_data_points(LogMessage *msg, const char *prefix, RepeatedPtrField<HistogramDataPoint> *data_points,
                           GlobalConfig *cfg)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];
  std::string key_buffer = prefix;
  size_t orig_len = key_buffer.length();

  NVHandle handle;
  gssize len;
  LogMessageValueType type;
  const gchar *value;

  uint64_t idx = 0;
  while (true)
    {
      key_buffer.resize(orig_len);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t len_with_idx = key_buffer.length();

      key_buffer.append("count");
      handle = log_msg_get_value_handle(key_buffer.c_str());
      value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
      if (!value)
        break;

      HistogramDataPoint *data_point = data_points->Add();

      data_point->set_count(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("attributes.");
      _get_and_set_repeated_KeyValues(msg, key_buffer.c_str(), data_point->mutable_attributes(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("start_time_unix_nano");
      data_point->set_start_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("time_unix_nano");
      data_point->set_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("sum");
      data_point->set_sum(_get_double(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("bucket_counts.");
      size_t len_with_bucket_counts = key_buffer.length();
      uint64_t bucket_count_idx = 0;
      while (true)
        {
          key_buffer.resize(len_with_bucket_counts);
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, bucket_count_idx);
          key_buffer.append(number_buf);

          handle = log_msg_get_value_handle(key_buffer.c_str());
          value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
          if (!value)
            break;

          data_point->add_bucket_counts(_get_uint64(msg, key_buffer.c_str()));

          bucket_count_idx++;
        }

      key_buffer.resize(len_with_idx);
      key_buffer.append("explicit_bounds.");
      size_t len_with_explicit_bounds = key_buffer.length();
      uint64_t explicit_bound_idx = 0;
      while (true)
        {
          key_buffer.resize(len_with_explicit_bounds);
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, explicit_bound_idx);
          key_buffer.append(number_buf);

          handle = log_msg_get_value_handle(key_buffer.c_str());
          value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
          if (!value)
            break;

          data_point->add_explicit_bounds(_get_double(msg, key_buffer.c_str()));

          explicit_bound_idx++;
        }

      key_buffer.resize(len_with_idx);
      key_buffer.append("exemplars.");
      _add_exemplars(msg, key_buffer, data_point->mutable_exemplars(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("flags");
      data_point->set_flags(_get_uint32(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("min");
      data_point->set_min(_get_double(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("max");
      data_point->set_max(_get_double(msg, key_buffer.c_str()));

      idx++;
    }
}

static void
_set_metric_histogram_values(LogMessage *msg, Histogram *histogram, GlobalConfig *cfg)
{
  _add_histogram_data_points(msg, ".otel.metric.data.histogram.data_points.", histogram->mutable_data_points(), cfg);

  int32_t aggregation_temporality_int = _get_int32(msg, ".otel.metric.data.histogram.aggregation_temporality");
  AggregationTemporality aggregation_temporality = AggregationTemporality_IsValid(aggregation_temporality_int) \
                                                   ? (AggregationTemporality) aggregation_temporality_int \
                                                   : AGGREGATION_TEMPORALITY_UNSPECIFIED;
  histogram->set_aggregation_temporality(aggregation_temporality);
}

static void
_add_buckets(LogMessage *msg, std::string &key_buffer, ExponentialHistogramDataPoint_Buckets *buckets)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];
  size_t orig_len = key_buffer.length();

  NVHandle handle;
  gssize len;
  LogMessageValueType type;
  const gchar *value;

  key_buffer.append("offset");
  buckets->set_offset(_get_int32(msg, key_buffer.c_str()));

  key_buffer.resize(orig_len);
  key_buffer.append("bucket_counts.");

  size_t len_with_bucket_counts = key_buffer.length();
  uint64_t idx = 0;
  while (true)
    {
      key_buffer.resize(len_with_bucket_counts);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);

      handle = log_msg_get_value_handle(key_buffer.c_str());
      value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
      if (!value)
        break;

      buckets->add_bucket_counts(_get_uint64(msg, key_buffer.c_str()));

      idx++;
    }
}

static void
_add_exponential_histogram_data_points(LogMessage *msg, const char *prefix,
                                       RepeatedPtrField<ExponentialHistogramDataPoint> *data_points, GlobalConfig *cfg)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];
  std::string key_buffer = prefix;
  size_t orig_len = key_buffer.length();

  NVHandle handle;
  gssize len;
  LogMessageValueType type;
  const gchar *value;

  uint64_t idx = 0;
  while (true)
    {
      key_buffer.resize(orig_len);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t len_with_idx = key_buffer.length();

      key_buffer.append("count");
      handle = log_msg_get_value_handle(key_buffer.c_str());
      value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
      if (!value)
        break;

      ExponentialHistogramDataPoint *data_point = data_points->Add();

      data_point->set_count(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("attributes.");
      _get_and_set_repeated_KeyValues(msg, key_buffer.c_str(), data_point->mutable_attributes(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("start_time_unix_nano");
      data_point->set_start_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("time_unix_nano");
      data_point->set_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("sum");
      data_point->set_sum(_get_double(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("scale");
      data_point->set_scale(_get_int32(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("zero_count");
      data_point->set_zero_count(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("positive.");
      _add_buckets(msg, key_buffer, data_point->mutable_positive());

      key_buffer.resize(len_with_idx);
      key_buffer.append("negative.");
      _add_buckets(msg, key_buffer, data_point->mutable_negative());

      key_buffer.resize(len_with_idx);
      key_buffer.append("flags");
      data_point->set_flags(_get_uint32(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("exemplars.");
      _add_exemplars(msg, key_buffer, data_point->mutable_exemplars(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("min");
      data_point->set_min(_get_double(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("max");
      data_point->set_max(_get_double(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("zero_threshold");
      data_point->set_zero_threshold(_get_double(msg, key_buffer.c_str()));

      idx++;
    }
}

static void
_set_metric_exponential_histogram_values(LogMessage *msg, ExponentialHistogram *exponential_histogram,
                                         GlobalConfig *cfg)
{
  _add_exponential_histogram_data_points(msg, ".otel.metric.data.exponential_histogram.data_points.",
                                         exponential_histogram->mutable_data_points(), cfg);

  int32_t aggregation_temporality_int = _get_int32(msg,
                                                   ".otel.metric.data.exponential_histogram.aggregation_temporality");
  AggregationTemporality aggregation_temporality = AggregationTemporality_IsValid(aggregation_temporality_int) \
                                                   ? (AggregationTemporality) aggregation_temporality_int \
                                                   : AGGREGATION_TEMPORALITY_UNSPECIFIED;
  exponential_histogram->set_aggregation_temporality(aggregation_temporality);
}

static void
_add_summary_data_points(LogMessage *msg, const char *prefix, RepeatedPtrField<SummaryDataPoint> *data_points,
                         GlobalConfig *cfg)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];
  std::string key_buffer = prefix;
  size_t orig_len = key_buffer.length();

  NVHandle handle;
  gssize len;
  LogMessageValueType type;
  const gchar *value;

  uint64_t idx = 0;
  while (true)
    {
      key_buffer.resize(orig_len);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t len_with_idx = key_buffer.length();

      key_buffer.append("count");
      handle = log_msg_get_value_handle(key_buffer.c_str());
      value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
      if (!value)
        break;

      SummaryDataPoint *data_point = data_points->Add();

      data_point->set_count(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("start_time_unix_nano");
      data_point->set_start_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("time_unix_nano");
      data_point->set_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("sum");
      data_point->set_sum(_get_double(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("attributes.");
      _get_and_set_repeated_KeyValues(msg, key_buffer.c_str(), data_point->mutable_attributes(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("quantile_values.");
      size_t len_with_quantile_values = key_buffer.length();
      uint64_t quantile_value_idx = 0;
      while (true)
        {
          key_buffer.resize(len_with_quantile_values);
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, quantile_value_idx);
          key_buffer.append(number_buf);
          key_buffer.append(".");
          size_t len_with_quantile_value_idx = key_buffer.length();

          key_buffer.append("quantile");
          handle = log_msg_get_value_handle(key_buffer.c_str());
          value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
          if (!value)
            break;

          SummaryDataPoint_ValueAtQuantile *value_at_quantile = data_point->add_quantile_values();

          value_at_quantile->set_quantile(_get_double(msg, key_buffer.c_str()));

          key_buffer.resize(len_with_quantile_value_idx);
          key_buffer.append("value");
          value_at_quantile->set_value(_get_double(msg, key_buffer.c_str()));

          quantile_value_idx++;
        }

      key_buffer.resize(len_with_idx);
      key_buffer.append("flags");
      data_point->set_flags(_get_uint32(msg, key_buffer.c_str()));

      idx++;
    }
}

static void
_set_metric_summary_values(LogMessage *msg, Summary *summary, GlobalConfig *cfg)
{
  _add_summary_data_points(msg, ".otel.metric.data.summary.data_points.", summary->mutable_data_points(), cfg);
}

bool
otel::protobuf::formatter::add_to_request(ExportMetricsServiceRequest &request, LogMessage *msg, GlobalConfig *cfg)
{
  ScopeMetrics *scope_metrics;
  Metric *metric = _create_metric(request, msg, &scope_metrics, cfg);
  if (!metric || !scope_metrics)
    {
      msg_error("OpenTelemetry: Failed to create metric");
      return false;
    }

  const gchar *value;
  gssize len;
  LogMessageValueType type;

  value = _get_string(msg, ".otel.metric.name", &len);
  metric->set_name(value, len);

  value = _get_string(msg, ".otel.metric.description", &len);
  metric->set_description(value, len);

  value = _get_string(msg, ".otel.metric.unit", &len);
  metric->set_unit(value, len);

  value = log_msg_get_value_by_name_with_type(msg, ".otel.metric.data.type", &len, &type);
  if (type != LM_VT_STRING)
    {
      msg_error("OpenTelemetry: Failed to determine metric data type, invalid log message type",
                evt_tag_str("name", ".otel.metric.data.type"),
                evt_tag_str("value", value),
                evt_tag_str("log_msg_type", log_msg_value_type_to_str(type)));
      goto error;
    }

  if (strncmp(value, "gauge", len) == 0)
    {
      _set_metric_gauge_values(msg, metric->mutable_gauge(), cfg);
    }
  else if (strncmp(value, "sum", len) == 0)
    {
      _set_metric_sum_values(msg, metric->mutable_sum(), cfg);
    }
  else if (strncmp(value, "histogram", len) == 0)
    {
      _set_metric_histogram_values(msg, metric->mutable_histogram(), cfg);
    }
  else if (strncmp(value, "exponential_histogram", len) == 0)
    {
      _set_metric_exponential_histogram_values(msg, metric->mutable_exponential_histogram(), cfg);
    }
  else if (strncmp(value, "summary", len) == 0)
    {
      _set_metric_summary_values(msg, metric->mutable_summary(), cfg);
    }
  else
    {
      msg_error("OpenTelemetry: Failed to determine metric data type, unexpected type",
                evt_tag_str("name", ".otel.metric.data.type"),
                evt_tag_str("value", value));
      goto error;
    }

  return true;

error:
  scope_metrics->mutable_metrics()->RemoveLast();
  return false;
}

static Span *
_create_span(ExportTraceServiceRequest &request, LogMessage *msg, GlobalConfig *cfg)
{
  const gchar *msg_resource_schema_url;
  gssize msg_resource_schema_url_len;
  Resource msg_resource = _get_resource_and_schema_url(msg, &msg_resource_schema_url, &msg_resource_schema_url_len,
                                                       cfg);

  const gchar *msg_scope_schema_url;
  gssize msg_scope_schema_url_len;
  InstrumentationScope msg_scope = _get_scope_and_schema_url(msg, &msg_scope_schema_url, &msg_scope_schema_url_len,
                                                             cfg);

  ResourceSpans *resource_spans = nullptr;
  for (int i = 0; i < request.resource_spans_size(); i++)
    {
      ResourceSpans &possible_resource_spans = request.mutable_resource_spans()->at(i);
      if (_is_message_from_resource(msg_resource, msg_resource_schema_url, msg_resource_schema_url_len,
                                    possible_resource_spans.resource(), possible_resource_spans.schema_url()))
        {
          resource_spans = std::addressof(possible_resource_spans);
          break;
        }
    }
  if (resource_spans == nullptr)
    {
      resource_spans = request.add_resource_spans();
      resource_spans->mutable_resource()->CopyFrom(msg_resource);
      resource_spans->set_schema_url(msg_resource_schema_url);
    }

  ScopeSpans *scope_spans = nullptr;
  for (int i = 0; i < resource_spans->scope_spans_size(); i++)
    {
      ScopeSpans &possible_scope_spans = resource_spans->mutable_scope_spans()->at(i);
      if (_is_message_from_scope(msg_scope, msg_scope_schema_url, msg_scope_schema_url_len,
                                 possible_scope_spans.scope(), possible_scope_spans.schema_url()))
        {
          scope_spans = std::addressof(possible_scope_spans);
          break;
        }
    }
  if (scope_spans == nullptr)
    {
      scope_spans = resource_spans->add_scope_spans();
      scope_spans->mutable_scope()->CopyFrom(msg_scope);
      scope_spans->set_schema_url(msg_scope_schema_url);
    }

  return scope_spans->add_spans();
}

bool
otel::protobuf::formatter::add_to_request(ExportTraceServiceRequest &request, LogMessage *msg, GlobalConfig *cfg)
{
  Span *span = _create_span(request, msg, cfg);
  if (!span)
    {
      msg_error("OpenTelemetry: Failed to create span");
      return false;
    }

  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];
  std::string key_buffer;
  NVHandle handle;
  const gchar *value;
  gssize len;
  LogMessageValueType type;

  value = _get_bytes(msg, ".otel.span.trace_id", &len);
  span->set_trace_id(value, len);

  value = _get_bytes(msg, ".otel.span.span_id", &len);
  span->set_span_id(value, len);

  value = _get_string(msg, ".otel.span.trace_state", &len);
  span->set_trace_state(value, len);

  value = _get_bytes(msg, ".otel.span.parent_span_id", &len);
  span->set_parent_span_id(value, len);

  value = _get_string(msg, ".otel.span.name", &len);
  span->set_name(value, len);

  int32_t kind_int = _get_int32(msg, ".otel.span.kind");
  Span_SpanKind kind = Span_SpanKind_IsValid(kind_int) ? (Span_SpanKind) kind_int : Span_SpanKind_SPAN_KIND_UNSPECIFIED;
  span->set_kind(kind);

  span->set_start_time_unix_nano(_get_uint64(msg, ".otel.span.start_time_unix_nano"));
  span->set_end_time_unix_nano(_get_uint64(msg, ".otel.span.end_time_unix_nano"));
  _get_and_set_repeated_KeyValues(msg, ".otel.span.attributes.", span->mutable_attributes(), cfg);
  span->set_dropped_attributes_count(_get_uint32(msg, ".otel.span.dropped_attributes_count"));

  key_buffer = ".otel.span.events.";
  size_t len_with_events = key_buffer.length();
  uint64_t event_idx = 0;
  while (true)
    {
      key_buffer.resize(len_with_events);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, event_idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t len_with_idx = key_buffer.length();

      key_buffer.append("time_unix_nano");
      handle = log_msg_get_value_handle(key_buffer.c_str());
      value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
      if (!value)
        break;

      Span_Event *event = span->add_events();

      event->set_time_unix_nano(_get_uint64(msg, key_buffer.c_str()));

      key_buffer.resize(len_with_idx);
      key_buffer.append("name");
      value = _get_string(msg, key_buffer.c_str(), &len);
      event->set_name(value, len);

      key_buffer.resize(len_with_idx);
      key_buffer.append("attributes.");
      _get_and_set_repeated_KeyValues(msg, key_buffer.c_str(), event->mutable_attributes(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("dropped_attributes_count");
      event->set_dropped_attributes_count(_get_uint32(msg, key_buffer.c_str()));

      event_idx++;
    }

  span->set_dropped_events_count(_get_uint32(msg, ".otel.span.dropped_events_count"));

  key_buffer = ".otel.span.links.";
  size_t len_with_links = key_buffer.length();
  uint64_t link_idx = 0;
  while (true)
    {
      key_buffer.resize(len_with_links);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, link_idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t len_with_idx = key_buffer.length();

      key_buffer.append("trace_id");
      handle = log_msg_get_value_handle(key_buffer.c_str());
      value = log_msg_get_value_if_set_with_type(msg, handle, &len, &type);
      if (!value)
        break;

      Span_Link *link = span->add_links();

      value = _get_bytes(msg, key_buffer.c_str(), &len);
      link->set_trace_id(value, len);

      key_buffer.resize(len_with_idx);
      key_buffer.append("span_id");
      value = _get_bytes(msg, key_buffer.c_str(), &len);
      link->set_span_id(value, len);

      key_buffer.resize(len_with_idx);
      key_buffer.append("trace_state");
      value = _get_string(msg, key_buffer.c_str(), &len);
      link->set_trace_state(value, len);

      key_buffer.resize(len_with_idx);
      key_buffer.append("attributes.");
      _get_and_set_repeated_KeyValues(msg, key_buffer.c_str(), link->mutable_attributes(), cfg);

      key_buffer.resize(len_with_idx);
      key_buffer.append("dropped_attributes_count");
      link->set_dropped_attributes_count(_get_uint32(msg, key_buffer.c_str()));

      link_idx++;
    }

  span->set_dropped_links_count(_get_uint32(msg, ".otel.span.dropped_links_count"));

  Status *status = span->mutable_status();
  value = _get_string(msg, ".otel.span.status.message", &len);
  status->set_message(value, len);

  int32_t code_int = _get_int32(msg, ".otel.span.status.code");
  Status_StatusCode code = Status_StatusCode_IsValid(code_int) ? (Status_StatusCode) code_int
                           : Status_StatusCode_STATUS_CODE_UNSET;
  status->set_code(code);

  return true;
}
