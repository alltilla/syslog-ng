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

#include <inttypes.h>

#include "otel-protobuf-parser.hpp"

using namespace google::protobuf;

static void
_set_value(LogMessage *msg, const char *key, const char *value, LogMessageValueType type)
{
  log_msg_set_value_by_name_with_type(msg, key, value, -1, type);
}

static void
_set_value(LogMessage *msg, const char *key, const std::string &value, LogMessageValueType type)
{
  log_msg_set_value_by_name_with_type(msg, key, value.c_str(), value.length(), type);
}

static void
_set_value(LogMessage *msg, NVHandle handle, const std::string &value, LogMessageValueType type)
{
  log_msg_set_value_with_type(msg, handle, value.c_str(), value.length(), type);
}

static void
_set_value_with_prefix(LogMessage *msg, std::string &key_buffer, size_t key_prefix_length, const char *key,
                       const std::string &value, LogMessageValueType type)
{
  key_buffer.resize(key_prefix_length);
  key_buffer.append(key);
  log_msg_set_value_by_name_with_type(msg, key_buffer.c_str(), value.c_str(), value.length(), type);
}

static const std::string &
_serialize_AnyValue(const AnyValue &value, LogMessageValueType *type, std::string *buffer)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  switch (value.value_case())
    {
    case AnyValue::kArrayValue:
    case AnyValue::kKvlistValue:
      *type = LM_VT_PROTOBUF;
      value.SerializeToString(buffer);
      return *buffer;
    case AnyValue::kBytesValue:
      *type = LM_VT_BYTES;
      return value.bytes_value();
    case AnyValue::kBoolValue:
      *type = LM_VT_BOOLEAN;
      *buffer = value.bool_value() ? "true" : "false";
      return *buffer;
    case AnyValue::kDoubleValue:
      *type = LM_VT_DOUBLE;
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), value.double_value());
      *buffer = number_buf;
      return *buffer;
    case AnyValue::kIntValue:
      *type = LM_VT_INTEGER;
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi64, value.int_value());
      *buffer = number_buf;
      return *buffer;
    case AnyValue::kStringValue:
      *type = LM_VT_STRING;
      return value.string_value();
    case AnyValue::VALUE_NOT_SET:
      *type = LM_VT_NONE;
      buffer->resize(0);
      return *buffer;
    default:
      msg_error("OpenTelemetry: unexpected AnyValue type", evt_tag_int("type", value.value_case()));
      buffer->resize(0);
      return *buffer;
    }
}

static void
_add_repeated_KeyValue_fields_with_prefix(LogMessage *msg, std::string &key_buffer, size_t key_prefix_length,
                                          const char *key, const RepeatedPtrField<KeyValue> &key_values)
{
  key_buffer.resize(key_prefix_length);
  key_buffer.append(key);
  key_buffer.append(".");
  size_t length_with_dot = key_buffer.length();
  std::string value_buffer;

  for (const KeyValue &kv : key_values)
    {
      /* <prefix>.<key>.<kv-key> */
      LogMessageValueType type;
      const std::string &value_serialized = _serialize_AnyValue(kv.value(), &type, &value_buffer);
      _set_value_with_prefix(msg, key_buffer, length_with_dot, kv.key().c_str(), value_serialized, type);
    }
}

static void
_add_repeated_KeyValue_fields(LogMessage *msg, const char *key, const RepeatedPtrField<KeyValue> &key_values)
{
  std::string key_buffer;
  _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, 0, key, key_values);
}

static std::string
_extract_hostname(const grpc::string &peer)
{
  size_t first = peer.find_first_of(':');
  size_t last = peer.find_last_of(':');

  if (first != grpc::string::npos && last != grpc::string::npos)
    return peer.substr(first + 1, last - first - 1);

  return "";
}

LogMessage *
create_log_msg_with_metadata(const grpc::string &peer,
                             const Resource &resource, const std::string &resource_schema_url,
                             const InstrumentationScope &scope, const std::string &scope_schema_url)
{
  LogMessage *msg = log_msg_new_empty();
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* HOST */
  std::string hostname = _extract_hostname(peer);
  if (hostname.length())
    log_msg_set_value(msg, LM_V_HOST, hostname.c_str(), hostname.length());

  /* .otel.resource.attributes */
  _add_repeated_KeyValue_fields(msg, ".otel.resource.attributes", resource.attributes());

  /* .otel.resource.dropped_attributes_count */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, resource.dropped_attributes_count());
  _set_value(msg, ".otel.resource.dropped_attributes_count", number_buf, LM_VT_INTEGER);

  /* .otel.resource.schema_url */
  _set_value(msg, ".otel.resource.schema_url", resource_schema_url, LM_VT_STRING);

  /* .otel.scope.name */
  _set_value(msg, ".otel.scope.name", scope.name(), LM_VT_STRING);

  /* .otel.scope.version */
  _set_value(msg, ".otel.scope.version", scope.version(), LM_VT_STRING);

  /* .otel.scope.attributes */
  _add_repeated_KeyValue_fields(msg, ".otel.scope.attributes", scope.attributes());

  /* .otel.scope.dropped_attributes_count */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, scope.dropped_attributes_count());
  _set_value(msg, ".otel.scope.dropped_attributes_count", number_buf, LM_VT_INTEGER);

  /* .otel.scope.schema_url */
  _set_value(msg, ".otel.scope.schema_url", scope_schema_url, LM_VT_STRING);

  return msg;
}

void
parse_LogRecord(LogMessage *msg, const LogRecord &log_record)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* .otel.type */
  log_msg_set_value_by_name_with_type(msg, ".otel.type", "log", -1, LM_VT_STRING);

  /* .otel.log.time_unix_nano */
  const guint64 time_unix_nano = log_record.time_unix_nano();
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, time_unix_nano);
  _set_value(msg, ".otel.log.time_unix_nano", number_buf, LM_VT_INTEGER);

  msg->timestamps[LM_TS_RECVD].ut_sec = time_unix_nano / 1000000;
  msg->timestamps[LM_TS_RECVD].ut_usec = time_unix_nano % 1000000;

  /* .otel.log.observed_time_unix_nano */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, log_record.observed_time_unix_nano());
  _set_value(msg, ".otel.log.observed_time_unix_nano", number_buf, LM_VT_INTEGER);

  /* .otel.log.severity_number */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, log_record.severity_number());
  _set_value(msg, ".otel.log.severity_number", number_buf, LM_VT_INTEGER);

  /* .otel.log.severity_text */
  _set_value(msg, ".otel.log.severity_text", log_record.severity_text(), LM_VT_STRING);

  /* MESSAGE */
  LogMessageValueType body_lmvt;
  std::string body_str_buffer;
  const std::string &body_str = _serialize_AnyValue(log_record.body(), &body_lmvt, &body_str_buffer);
  _set_value(msg, LM_V_MESSAGE, body_str, body_lmvt);

  /* .otel.log.body */
  NVHandle body_handle = log_msg_get_value_handle(".otel.log.body");
  log_msg_set_value_indirect_with_type(msg, body_handle, LM_V_MESSAGE, 0, body_str.length(), body_lmvt);

  /* .otel.log.attributes */
  _add_repeated_KeyValue_fields(msg, ".otel.log.attributes", log_record.attributes());

  /* .otel.log.dropped_attributes_count */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, log_record.dropped_attributes_count());
  _set_value(msg, ".otel.log.dropped_attributes_count", number_buf, LM_VT_INTEGER);

  /* .otel.log.flags */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, log_record.flags());
  _set_value(msg, ".otel.log.flags", number_buf, LM_VT_INTEGER);

  /* .otel.log.trace_id */
  _set_value(msg, ".otel.log.trace_id", log_record.trace_id(), LM_VT_BYTES);

  /* .otel.log.span_id */
  _set_value(msg, ".otel.log.span_id", log_record.span_id(), LM_VT_BYTES);
}

static void
_add_repeated_Exemplar_fields_with_prefix(LogMessage *msg, std::string &key_buffer, size_t key_prefix_length,
                                          const char *key, RepeatedPtrField<Exemplar> exemplars)
{
  key_buffer.resize(key_prefix_length);
  key_buffer.append(key);
  key_buffer.append(".");
  size_t length_with_dot = key_buffer.length();
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  uint64_t idx = 0;
  for (const Exemplar &exemplar : exemplars)
    {
      key_buffer.resize(length_with_dot);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t length_with_idx = key_buffer.length();

      /* <prefix>.<key>.<idx>.filtered_attributes.<...> */
      _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, length_with_idx, "filtered_attributes",
                                                exemplar.filtered_attributes());

      /* <prefix>.<key>.<idx>.time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, exemplar.time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "time_unix_nano", number_buf, LM_VT_INTEGER);

      /* <prefix>.<key>.<idx>.value */
      switch (exemplar.value_case())
        {
        case Exemplar::kAsDouble:
          g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), exemplar.as_double());
          _set_value_with_prefix(msg, key_buffer, length_with_idx, "value", number_buf, LM_VT_DOUBLE);
          break;
        case Exemplar::kAsInt:
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi64, exemplar.as_int());
          _set_value_with_prefix(msg, key_buffer, length_with_idx, "value", number_buf, LM_VT_INTEGER);
          break;
        case Exemplar::VALUE_NOT_SET:
          break;
        default:
          msg_error("OpenTelemetry: unexpected Exemplar type", evt_tag_int("type", exemplar.value_case()));
        }

      /* <prefix>.<key>.<idx>.span_id */
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "span_id", exemplar.span_id(), LM_VT_BYTES);

      /* <prefix>.<key>.<idx>.trace_id */
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "trace_id", exemplar.trace_id(), LM_VT_BYTES);

      idx++;
    }
}

static void
_add_NumberDataPoints_fields_with_prefix(LogMessage *msg, std::string &key_buffer, size_t key_prefix_length,
                                         const char *key, RepeatedPtrField<NumberDataPoint> data_points)
{
  key_buffer.resize(key_prefix_length);
  key_buffer.append(key);
  key_buffer.append(".");
  size_t length_with_dot = key_buffer.length();
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  uint64_t idx = 0;
  for (const NumberDataPoint &data_point : data_points)
    {
      key_buffer.resize(length_with_dot);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t length_with_idx = key_buffer.length();

      /* <prefix>.<key>.<idx>.attributes */
      _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, length_with_idx, "attributes",
                                                data_point.attributes());

      /* <prefix>.<key>.<idx>.start_time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.start_time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "start_time_unix_nano", number_buf, LM_VT_INTEGER);

      /* <prefix>.<key>.<idx>.time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "time_unix_nano", number_buf, LM_VT_INTEGER);

      /* <prefix>.<key>.<idx>.value */
      switch (data_point.value_case())
        {
        case NumberDataPoint::kAsDouble:
          g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.as_double());
          _set_value_with_prefix(msg, key_buffer, length_with_idx, "value", number_buf, LM_VT_DOUBLE);
          break;
        case NumberDataPoint::kAsInt:
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi64, data_point.as_int());
          _set_value_with_prefix(msg, key_buffer, length_with_idx, "value", number_buf, LM_VT_INTEGER);
          break;
        case NumberDataPoint::VALUE_NOT_SET:
          break;
        default:
          msg_error("OpenTelemetry: unexpected NumberDataPoint type", evt_tag_int("type", data_point.value_case()));
        }

      /* <prefix>.<key>.<idx>.exemplars.<...> */
      _add_repeated_Exemplar_fields_with_prefix(msg, key_buffer, length_with_idx, "exemplars", data_point.exemplars());

      /* <prefix>.<key>.<idx>.flags */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, data_point.flags());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "flags", number_buf, LM_VT_INTEGER);

      idx++;
    }
}

static void
_add_NumberDataPoints_fields(LogMessage *msg, const char *key, RepeatedPtrField<NumberDataPoint> data_points)
{
  std::string key_buffer;
  _add_NumberDataPoints_fields_with_prefix(msg, key_buffer, 0, key, data_points);
}

static void
_add_metric_data_gauge_fields(LogMessage *msg, const Gauge &gauge)
{
  /* .otel.metric.data.gauge.data_points.<...> */
  _add_NumberDataPoints_fields(msg, ".otel.metric.data.gauge.data_points", gauge.data_points());
}

static void
_add_metric_data_sum_fields(LogMessage *msg, const Sum &sum)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* .otel.metric.data.sum.data_points.<...> */
  _add_NumberDataPoints_fields(msg, ".otel.metric.data.sum.data_points", sum.data_points());

  /* .otel.metric.data.sum.aggregation_temporality */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, sum.aggregation_temporality());
  _set_value(msg, ".otel.metric.data.sum.aggregation_temporality", number_buf, LM_VT_INTEGER);

  /* .otel.metric.data.sum.is_monotonic */
  _set_value(msg, ".otel.metric.data.sum.is_monotonic", sum.is_monotonic() ? "true" : "false", LM_VT_BOOLEAN);
}

static void
_add_metric_data_histogram_fields(LogMessage *msg, const Histogram &histogram)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* .otel.metric.data.histogram.data_points.<...> */
  std::string key_buffer = ".otel.metric.data.histogram.data_points.";
  size_t length_with_dot = key_buffer.length();

  uint64_t idx = 0;
  for (const HistogramDataPoint &data_point : histogram.data_points())
    {
      key_buffer.resize(length_with_dot);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t length_with_idx = key_buffer.length();

      /* .otel.metric.data.histogram.data_points.<idx>.attributes.<...> */
      _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, length_with_idx, "attributes",
                                                data_point.attributes());

      /* .otel.metric.data.histogram.data_points.<idx>.start_time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.start_time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "start_time_unix_nano", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.histogram.data_points.<idx>.time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "time_unix_nano", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.histogram.data_points.<idx>.count */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.count());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "count", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.histogram.data_points.<idx>.sum */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.sum());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "sum", number_buf, LM_VT_DOUBLE);

      /* .otel.metric.data.histogram.data_points.<idx>.bucket_counts.<...> */
      key_buffer.resize(length_with_idx);
      key_buffer.append("bucket_counts.");
      size_t length_with_bucket_count = key_buffer.length();

      uint64_t bucket_count_idx = 0;
      for (uint64 bucket_count : data_point.bucket_counts())
        {
          key_buffer.resize(length_with_bucket_count);
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, bucket_count_idx);
          key_buffer.append(number_buf);

          /* .otel.metric.data.histogram.data_points.<idx>.bucket_counts.<idx> */
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, bucket_count);
          _set_value(msg, key_buffer.c_str(), number_buf, LM_VT_INTEGER);

          bucket_count_idx++;
        }

      /* .otel.metric.data.histogram.data_points.<idx>.explicit_bounds.<...> */
      key_buffer.resize(length_with_idx);
      key_buffer.append("explicit_bounds.");
      size_t length_with_explicit_bound = key_buffer.length();
      uint64_t explicit_bound_idx = 0;

      for (double explicit_bound : data_point.explicit_bounds())
        {
          key_buffer.resize(length_with_explicit_bound);
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, explicit_bound_idx);
          key_buffer.append(number_buf);

          /* .otel.metric.data.histogram.data_points.<idx>.explicit_bounds.<idx> */
          g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), explicit_bound);
          _set_value(msg, key_buffer.c_str(), number_buf, LM_VT_DOUBLE);

          explicit_bound_idx++;
        }

      /* .otel.metric.data.histogram.data_points.<idx>.exemplars.<...> */
      _add_repeated_Exemplar_fields_with_prefix(msg, key_buffer, length_with_idx, "exemplars", data_point.exemplars());

      /* .otel.metric.data.histogram.data_points.<idx>.flags */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, data_point.flags());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "flags", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.histogram.data_points.<idx>.min */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.min());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "min", number_buf, LM_VT_DOUBLE);

      /* .otel.metric.data.histogram.data_points.<idx>.max */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.max());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "max", number_buf, LM_VT_DOUBLE);

      idx++;
    }

  /* .otel.metric.data.histogram.aggregation_temporality */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, histogram.aggregation_temporality());
  _set_value(msg, ".otel.metric.data.histogram.aggregation_temporality", number_buf, LM_VT_INTEGER);
}

static void
_add_Buckets_fields_with_prefix(LogMessage *msg, std::string &key_buffer, size_t key_prefix_length, const char *key,
                                const ExponentialHistogramDataPoint::Buckets &buckets)
{
  key_buffer.resize(key_prefix_length);
  key_buffer.append(key);
  key_buffer.append(".");
  size_t length_with_dot = key_buffer.length();
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* <prefix>.<key>.offset */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, buckets.offset());
  _set_value_with_prefix(msg, key_buffer, length_with_dot, "offset", number_buf, LM_VT_INTEGER);

  /* <prefix>.<key>.bucket_counts.<...> */
  key_buffer.resize(length_with_dot);
  key_buffer.append("bucket_counts.");
  size_t length_with_bucket_counts = key_buffer.length();

  uint64_t idx = 0;
  for (uint64_t bucket_count : buckets.bucket_counts())
    {
      key_buffer.resize(length_with_bucket_counts);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);

      /* <prefix>.<key>.bucket_counts.<idx> */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, bucket_count);
      _set_value(msg, key_buffer.c_str(), number_buf, LM_VT_INTEGER);

      idx++;
    }
}

static void
_add_metric_data_exponential_histogram_fields(LogMessage *msg, const ExponentialHistogram &exponential_histogram)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* .otel.metric.data.exponential_histogram.data_points.<...> */
  std::string key_buffer = ".otel.metric.data.exponential_histogram.data_points.";
  size_t length_with_dot = key_buffer.length();

  uint64_t idx = 0;
  for (const ExponentialHistogramDataPoint &data_point : exponential_histogram.data_points())
    {
      key_buffer.resize(length_with_dot);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t length_with_idx = key_buffer.length();

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.attributes.<...> */
      _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, length_with_idx, "attributes",
                                                data_point.attributes());

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.start_time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.start_time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "start_time_unix_nano", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "time_unix_nano", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.count */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.count());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "count", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.sum */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.sum());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "sum", number_buf, LM_VT_DOUBLE);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.scale */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, data_point.scale());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "scale", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.zero_count */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.zero_count());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "zero_count", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.positive.<...> */
      _add_Buckets_fields_with_prefix(msg, key_buffer, length_with_idx, "positive", data_point.positive());

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.negative.<...> */
      _add_Buckets_fields_with_prefix(msg, key_buffer, length_with_idx, "negative", data_point.negative());

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.flags */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, data_point.flags());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "flags", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.exemplars */
      _add_repeated_Exemplar_fields_with_prefix(msg, key_buffer, length_with_idx, "exemplars", data_point.exemplars());

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.min */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.min());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "min", number_buf, LM_VT_DOUBLE);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.max */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.max());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "max", number_buf, LM_VT_DOUBLE);

      /* .otel.metric.data.exponential_histogram.data_points.<idx>.zero_threshold */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.zero_threshold());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "zero_threshold", number_buf, LM_VT_DOUBLE);

      idx++;
    }

  /* .otel.metric.data.exponential_histogram.aggregation_temporality */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, exponential_histogram.aggregation_temporality());
  _set_value(msg, ".otel.metric.data.exponential_histogram.aggregation_temporality", number_buf, LM_VT_INTEGER);
}

static void
_add_metric_data_summary_fields(LogMessage *msg, const Summary &summary)
{
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* .otel.metric.data.summary.data_points.<...> */
  std::string key_buffer = ".otel.metric.data.summary.data_points.";
  size_t length_with_dot = key_buffer.length();

  uint64_t idx = 0;
  for (const SummaryDataPoint &data_point : summary.data_points())
    {
      key_buffer.resize(length_with_dot);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t length_with_idx = key_buffer.length();

      /* .otel.metric.data.summary.data_points.<idx>.attributes.<...> */
      _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, length_with_idx, "attributes",
                                                data_point.attributes());

      /* .otel.metric.data.summary.data_points.<idx>.start_time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.start_time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "start_time_unix_nano", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.summary.data_points.<idx>.time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "time_unix_nano", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.summary.data_points.<idx>.count */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, data_point.count());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "count", number_buf, LM_VT_INTEGER);

      /* .otel.metric.data.summary.data_points.<idx>.sum */
      g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), data_point.sum());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "sum", number_buf, LM_VT_DOUBLE);

      /* .otel.metric.data.summary.data_points.<idx>.quantile_values.<...> */
      key_buffer.resize(length_with_idx);
      key_buffer.append("quantile_values.");
      size_t length_with_quantile_values = key_buffer.length();

      uint64_t quantile_value_idx = 0;
      for (const SummaryDataPoint::ValueAtQuantile &quantile_value : data_point.quantile_values())
        {
          key_buffer.resize(length_with_quantile_values);
          std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, quantile_value_idx);
          key_buffer.append(number_buf);
          key_buffer.append(".");
          size_t length_with_quantile_value_idx = key_buffer.length();

          /* .otel.metric.data.summary.data_points.<idx>.quantile_values.<idx>.quantile */
          g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), quantile_value.quantile());
          _set_value_with_prefix(msg, key_buffer, length_with_quantile_value_idx, "quantile", number_buf, LM_VT_DOUBLE);

          /* .otel.metric.data.summary.data_points.<idx>.quantile_values.<idx>.value */
          g_ascii_dtostr(number_buf, G_N_ELEMENTS(number_buf), quantile_value.value());
          _set_value_with_prefix(msg, key_buffer, length_with_quantile_value_idx, "value", number_buf, LM_VT_DOUBLE);

          quantile_value_idx++;
        }

      /* .otel.metric.data.summary.data_points.<idx>.flags */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, data_point.flags());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "flags", number_buf, LM_VT_INTEGER);

      idx++;
    }
}

static void
_add_metric_data_fields(LogMessage *msg, const Metric &metric)
{
  const char *type = nullptr;

  switch (metric.data_case())
    {
    case Metric::kGauge:
      type = "gauge";
      _add_metric_data_gauge_fields(msg, metric.gauge());
      break;
    case Metric::kSum:
      type = "sum";
      _add_metric_data_sum_fields(msg, metric.sum());
      break;
    case Metric::kHistogram:
      type = "histogram";
      _add_metric_data_histogram_fields(msg, metric.histogram());
      break;
    case Metric::kExponentialHistogram:
      type = "exponential_histogram";
      _add_metric_data_exponential_histogram_fields(msg, metric.exponential_histogram());
      break;
    case Metric::kSummary:
      type = "summary";
      _add_metric_data_summary_fields(msg, metric.summary());
      break;
    case Metric::DATA_NOT_SET:
      break;
    default:
      msg_error("OpenTelemetry: unexpected Metric type", evt_tag_int("type", metric.data_case()));
    }

  /* .otel.metric.data.type */
  if (type)
    log_msg_set_value_by_name_with_type(msg, ".otel.metric.data.type", type, -1, LM_VT_STRING);
}

void
parse_Metric(LogMessage *msg, const Metric &metric)
{
  /* .otel.type */
  log_msg_set_value_by_name_with_type(msg, ".otel.type", "metric", -1, LM_VT_STRING);

  /* .otel.metric.name */
  _set_value(msg, ".otel.metric.name", metric.name(), LM_VT_STRING);

  /* .otel.metric.description */
  _set_value(msg, ".otel.metric.description", metric.description(), LM_VT_STRING);

  /* .otel.metric.unit */
  _set_value(msg, ".otel.metric.unit", metric.unit(), LM_VT_STRING);

  _add_metric_data_fields(msg, metric);
}

void
parse_Span(LogMessage *msg, const Span &span)
{
  /* .otel.type */
  log_msg_set_value_by_name_with_type(msg, ".otel.type", "span", -1, LM_VT_STRING);

  std::string key_buffer = ".otel.span.";
  size_t key_prefix_length = key_buffer.length();
  char number_buf[G_ASCII_DTOSTR_BUF_SIZE];

  /* .otel.span.trace_id */
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "trace_id", span.trace_id(), LM_VT_BYTES);

  /* .otel.span.span_id */
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "span_id", span.span_id(), LM_VT_BYTES);

  /* .otel.span.trace_state */
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "trace_state", span.trace_state(), LM_VT_STRING);

  /* .otel.span.parent_span_id */
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "parent_span_id", span.parent_span_id(), LM_VT_BYTES);

  /* .otel.span.name */
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "name", span.name(), LM_VT_STRING);

  /* .otel.span.kind */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, span.kind());
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "kind", number_buf, LM_VT_INTEGER);

  /* .otel.span.start_time_unix_nano */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, span.start_time_unix_nano());
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "start_time_unix_nano", number_buf, LM_VT_INTEGER);

  /* .otel.span.end_time_unix_nano */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, span.end_time_unix_nano());
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "end_time_unix_nano", number_buf, LM_VT_INTEGER);

  /* .otel.span.attributes.<...> */
  _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, key_prefix_length, "attributes", span.attributes());

  /* .otel.span.dropped_attributes_count */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, span.dropped_attributes_count());
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "dropped_attributes_count", number_buf, LM_VT_INTEGER);

  /* .otel.span.events.<...> */
  key_buffer.resize(key_prefix_length);
  key_buffer.append("events.");
  size_t length_with_events = key_buffer.length();

  uint64_t event_idx = 0;
  for (const Span::Event &event : span.events())
    {
      key_buffer.resize(length_with_events);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, event_idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t length_with_idx = key_buffer.length();

      /* .otel.span.events.<idx>.time_unix_nano */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, event.time_unix_nano());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "time_unix_nano", number_buf, LM_VT_INTEGER);

      /* .otel.span.events.<idx>.name */
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "name", event.name(), LM_VT_STRING);

      /* .otel.span.events.<idx>.attributes.<...> */
      _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, length_with_idx, "attributes", event.attributes());

      /* .otel.span.events.<idx>.dropped_attributes_count */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, event.dropped_attributes_count());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "dropped_attributes_count", number_buf,
                             LM_VT_INTEGER);

      event_idx++;
    }

  /* .otel.span.dropped_events_count */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, span.dropped_events_count());
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "dropped_events_count", number_buf, LM_VT_INTEGER);

  /* .otel.span.links.<...> */
  key_buffer.resize(key_prefix_length);
  key_buffer.append("links.");
  size_t length_with_links = key_buffer.length();

  uint64_t link_idx = 0;
  for (const Span::Link &link : span.links())
    {
      key_buffer.resize(length_with_links);
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu64, link_idx);
      key_buffer.append(number_buf);
      key_buffer.append(".");
      size_t length_with_idx = key_buffer.length();

      /* .otel.span.links.<idx>.trace_id */
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "trace_id", link.trace_id(), LM_VT_BYTES);

      /* .otel.span.links.<idx>.span_id */
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "span_id", link.span_id(), LM_VT_BYTES);

      /* .otel.span.links.<idx>.trace_state */
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "trace_state", link.trace_state(), LM_VT_STRING);

      /* .otel.span.links.<idx>.attributes.<...> */
      _add_repeated_KeyValue_fields_with_prefix(msg, key_buffer, length_with_idx, "attributes", link.attributes());

      /* .otel.span.links.<idx>.dropped_attributes_count */
      std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, link.dropped_attributes_count());
      _set_value_with_prefix(msg, key_buffer, length_with_idx, "dropped_attributes_count", number_buf,
                             LM_VT_INTEGER);

      link_idx++;
    }

  /* .otel.span.dropped_links_count */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIu32, span.dropped_links_count());
  _set_value_with_prefix(msg, key_buffer, key_prefix_length, "dropped_links_count", number_buf, LM_VT_INTEGER);

  /* .otel.span.status.<...> */
  key_buffer.resize(key_prefix_length);
  key_buffer.append("status.");
  size_t length_with_status = key_buffer.length();
  const Status &status = span.status();

  /* .otel.span.status.message */
  _set_value_with_prefix(msg, key_buffer, length_with_status, "message", status.message(), LM_VT_STRING);

  /* .otel.span.status.code */
  std::snprintf(number_buf, G_N_ELEMENTS(number_buf), "%" PRIi32, status.code());
  _set_value_with_prefix(msg, key_buffer, length_with_status, "code", number_buf, LM_VT_INTEGER);
}
