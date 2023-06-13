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

#include <criterion/criterion.h>

#include "otel-protobuf-formatter.hpp"

#include "compat/cpp-start.h"
#include "apphook.h"
#include "cfg.h"
#include "compat/cpp-end.h"

using namespace otel;
using namespace protobuf::formatter;

using namespace opentelemetry::proto::resource::v1;
using namespace opentelemetry::proto::common::v1;
using namespace opentelemetry::proto::logs::v1;

static LogMessage *
_create_log_msg_with_dummy_resource_and_scope()
{
  LogMessage *msg = log_msg_new_empty();

  log_msg_set_value_by_name_with_type(msg, ".otel.resource.attributes.attr_0", "val_0", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.resource.dropped_attributes_count", "1", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.resource.schema_url", "resource_schema_url", -1, LM_VT_STRING);

  log_msg_set_value_by_name_with_type(msg, ".otel.scope.name", "scope", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.scope.version", "v1.2.3", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.resource.attributes.attr_1", "val_1", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.scope.dropped_attributes_count", "2", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.scope.schema_url", "scope_schema_url", -1, LM_VT_STRING);

  return msg;
}

Test(otel_protobuf_formatter, get_message_type)
{
  LogMessage *msg = log_msg_new_empty();
  cr_assert_eq(get_message_type(msg), MessageType::UNKNOWN);

  log_msg_set_value_by_name_with_type(msg, ".otel.type", "log", -1, LM_VT_BYTES);
  cr_assert_eq(get_message_type(msg), MessageType::UNKNOWN);

  log_msg_set_value_by_name_with_type(msg, ".otel.type", "log", -1, LM_VT_STRING);
  cr_assert_eq(get_message_type(msg), MessageType::LOG);

  log_msg_set_value_by_name_with_type(msg, ".otel.type", "metric", -1, LM_VT_STRING);
  cr_assert_eq(get_message_type(msg), MessageType::METRIC);

  log_msg_set_value_by_name_with_type(msg, ".otel.type", "span", -1, LM_VT_STRING);
  cr_assert_eq(get_message_type(msg), MessageType::SPAN);

  log_msg_set_value_by_name_with_type(msg, ".otel.type", "almafa", -1, LM_VT_STRING);
  cr_assert_eq(get_message_type(msg), MessageType::UNKNOWN);

  log_msg_unref(msg);
}

/* This testcase also tests the the handling of different types of KeyValues. */
Test(otel_protobuf_formatter, log_record)
{
  LogMessage *msg = _create_log_msg_with_dummy_resource_and_scope();

  log_msg_set_value_by_name_with_type(msg, ".otel.log.time_unix_nano", "123", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.observed_time_unix_nano", "456", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.severity_number", "17", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.severity_text", "my_error_text", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string_body", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.a_string_key", "string", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.b_int_key", "42", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.c_double_key", "42.123456", -1, LM_VT_DOUBLE);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.d_bool_key", "true", -1, LM_VT_BOOLEAN);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.e_null_key", "", -1, LM_VT_NULL);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.f_bytes_key", "\0\1\2\3", 4, LM_VT_BYTES);

  AnyValue any_value_for_kv_list;
  KeyValueList *kv_list = any_value_for_kv_list.mutable_kvlist_value();
  KeyValue *kv_1 = kv_list->add_values();
  kv_1->set_key("kv_1");
  kv_1->mutable_value()->set_string_value("kv_1_val");
  KeyValue *kv_2 = kv_list->add_values();
  kv_2->set_key("kv_2");
  kv_2->mutable_value()->set_string_value("kv_2_val");
  std::string any_value_kv_list_serialized = any_value_for_kv_list.SerializeAsString();
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.g_protobuf_kv_list_key",
                                      any_value_kv_list_serialized.c_str(), any_value_kv_list_serialized.length(),
                                      LM_VT_PROTOBUF);

  AnyValue any_value_for_array;
  ArrayValue *array = any_value_for_array.mutable_array_value();
  AnyValue *array_value_1 = array->add_values();
  array_value_1->set_int_value(1337);
  AnyValue *array_value_2 = array->add_values();
  array_value_2->set_int_value(7331);
  std::string any_value_array_serialized = any_value_for_array.SerializeAsString();
  log_msg_set_value_by_name_with_type(msg, ".otel.log.attributes.h_protobuf_array_key",
                                      any_value_array_serialized.c_str(), any_value_array_serialized.length(),
                                      LM_VT_PROTOBUF);

  log_msg_set_value_by_name_with_type(msg, ".otel.log.dropped_attributes_count", "11", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.flags", "22", -1, LM_VT_INTEGER);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.trace_id", "\0\1\2\3\4\5\6\7\0\1\2\3\4\5\6\7", 16, LM_VT_BYTES);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.span_id", "\0\1\2\3\4\5\6\7", 8, LM_VT_BYTES);

  ExportLogsServiceRequest request;
  cr_assert(add_to_request(request, msg, configuration));

  cr_assert_eq(request.resource_logs_size(), 1);
  const ResourceLogs &resource_logs = request.resource_logs().at(0);
  cr_assert_eq(resource_logs.scope_logs_size(), 1);
  const ScopeLogs &scope_logs = resource_logs.scope_logs().at(0);
  cr_assert_eq(scope_logs.log_records_size(), 1);
  const LogRecord &log_record = scope_logs.log_records().at(0);

  cr_assert_eq(log_record.time_unix_nano(), 123);
  cr_assert_eq(log_record.observed_time_unix_nano(), 456);
  cr_assert_eq(log_record.severity_number(), SeverityNumber::SEVERITY_NUMBER_ERROR);
  cr_assert_str_eq(log_record.severity_text().c_str(), "my_error_text");
  cr_assert_eq(log_record.body().value_case(), AnyValue::kStringValue);
  cr_assert_str_eq(log_record.body().string_value().c_str(), "string_body");

  auto &attributes = log_record.attributes();
  cr_assert_eq(log_record.attributes_size(), 8);
  cr_assert_str_eq(attributes.at(0).key().c_str(), "a_string_key");
  cr_assert_eq(attributes.at(0).value().value_case(), AnyValue::kStringValue);
  cr_assert_str_eq(attributes.at(0).value().string_value().c_str(), "string");
  cr_assert_str_eq(attributes.at(1).key().c_str(), "b_int_key");
  cr_assert_eq(attributes.at(1).value().value_case(), AnyValue::kIntValue);
  cr_assert_eq(attributes.at(1).value().int_value(), 42);
  cr_assert_str_eq(attributes.at(2).key().c_str(), "c_double_key");
  cr_assert_eq(attributes.at(2).value().value_case(), AnyValue::kDoubleValue);
  cr_assert_float_eq(attributes.at(2).value().double_value(), 42.123456, std::numeric_limits<double>::epsilon());
  cr_assert_str_eq(attributes.at(3).key().c_str(), "d_bool_key");
  cr_assert_eq(attributes.at(3).value().value_case(), AnyValue::kBoolValue);
  cr_assert_eq(attributes.at(3).value().bool_value(), true);
  cr_assert_str_eq(attributes.at(4).key().c_str(), "e_null_key");
  cr_assert_eq(attributes.at(4).value().value_case(), AnyValue::VALUE_NOT_SET);
  cr_assert_str_eq(attributes.at(5).key().c_str(), "f_bytes_key");
  cr_assert_eq(attributes.at(5).value().value_case(), AnyValue::kBytesValue);
  cr_assert_eq(attributes.at(5).value().bytes_value().length(), 4);
  cr_assert_eq(memcmp(attributes.at(5).value().bytes_value().c_str(), "\0\1\2\3", 4), 0);
  cr_assert_str_eq(attributes.at(6).key().c_str(), "g_protobuf_kv_list_key");
  cr_assert_eq(attributes.at(6).value().value_case(), AnyValue::kKvlistValue);
  cr_assert_eq(attributes.at(6).value().kvlist_value().values_size(), 2);
  cr_assert_str_eq(attributes.at(6).value().kvlist_value().values().at(0).key().c_str(), "kv_1");
  cr_assert_str_eq(attributes.at(6).value().kvlist_value().values().at(0).value().string_value().c_str(), "kv_1_val");
  cr_assert_str_eq(attributes.at(6).value().kvlist_value().values().at(1).key().c_str(), "kv_2");
  cr_assert_str_eq(attributes.at(6).value().kvlist_value().values().at(1).value().string_value().c_str(), "kv_2_val");
  cr_assert_str_eq(attributes.at(7).key().c_str(), "h_protobuf_array_key");
  cr_assert_eq(attributes.at(7).value().value_case(), AnyValue::kArrayValue);
  cr_assert_eq(attributes.at(7).value().array_value().values_size(), 2);
  cr_assert_eq(attributes.at(7).value().array_value().values().at(0).int_value(), 1337);
  cr_assert_eq(attributes.at(7).value().array_value().values().at(1).int_value(), 7331);

  cr_assert_eq(log_record.dropped_attributes_count(), 11);
  cr_assert_eq(log_record.flags(), 22);
  cr_assert_eq(log_record.trace_id().length(), 16);
  cr_assert_eq(memcmp(log_record.trace_id().c_str(), "\0\1\2\3\4\5\6\7\0\1\2\3\4\5\6\7", 16), 0);
  cr_assert_eq(log_record.span_id().length(), 8);
  cr_assert_eq(memcmp(log_record.span_id().c_str(), "\0\1\2\3\4\5\6\7", 8), 0);

  log_msg_unref(msg);
}

Test(otel_protobuf_formatter, log_record_body_types)
{
  LogMessage *msg = _create_log_msg_with_dummy_resource_and_scope();

  ExportLogsServiceRequest request;

  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string", -1, LM_VT_STRING);
  cr_assert(add_to_request(request, msg, configuration));
  auto &log_records = request.resource_logs().at(0).scope_logs().at(0).log_records();
  cr_assert_eq(log_records.at(0).body().value_case(), AnyValue::kStringValue);
  cr_assert_str_eq(log_records.at(0).body().string_value().c_str(), "string");

  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "42", -1, LM_VT_INTEGER);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(log_records.at(1).body().value_case(), AnyValue::kIntValue);
  cr_assert_eq(log_records.at(1).body().int_value(), 42);

  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "42.123456", -1, LM_VT_DOUBLE);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(log_records.at(2).body().value_case(), AnyValue::kDoubleValue);
  cr_assert_float_eq(log_records.at(2).body().double_value(), 42.123456, std::numeric_limits<double>::epsilon());

  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "true", -1, LM_VT_BOOLEAN);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(log_records.at(3).body().value_case(), AnyValue::kBoolValue);
  cr_assert_eq(log_records.at(3).body().bool_value(), true);

  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "", -1, LM_VT_NULL);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(log_records.at(4).body().value_case(), AnyValue::VALUE_NOT_SET);

  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "\0\1\2\3", 4, LM_VT_BYTES);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(log_records.at(5).body().value_case(), AnyValue::kBytesValue);
  cr_assert_eq(log_records.at(5).body().bytes_value().length(), 4);
  cr_assert_eq(memcmp(log_records.at(5).body().bytes_value().c_str(), "\0\1\2\3", 4), 0);

  AnyValue any_value_for_kv_list;
  KeyValueList *kv_list = any_value_for_kv_list.mutable_kvlist_value();
  KeyValue *kv_1 = kv_list->add_values();
  kv_1->set_key("kv_1");
  kv_1->mutable_value()->set_string_value("kv_1_val");
  KeyValue *kv_2 = kv_list->add_values();
  kv_2->set_key("kv_2");
  kv_2->mutable_value()->set_string_value("kv_2_val");
  std::string any_value_kv_list_serialized = any_value_for_kv_list.SerializeAsString();
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body",
                                      any_value_kv_list_serialized.c_str(), any_value_kv_list_serialized.length(),
                                      LM_VT_PROTOBUF);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(log_records.at(6).body().value_case(), AnyValue::kKvlistValue);
  cr_assert_eq(log_records.at(6).body().kvlist_value().values_size(), 2);
  cr_assert_str_eq(log_records.at(6).body().kvlist_value().values().at(0).key().c_str(), "kv_1");
  cr_assert_str_eq(log_records.at(6).body().kvlist_value().values().at(0).value().string_value().c_str(), "kv_1_val");
  cr_assert_str_eq(log_records.at(6).body().kvlist_value().values().at(1).key().c_str(), "kv_2");
  cr_assert_str_eq(log_records.at(6).body().kvlist_value().values().at(1).value().string_value().c_str(), "kv_2_val");

  AnyValue any_value_for_array;
  ArrayValue *array = any_value_for_array.mutable_array_value();
  AnyValue *array_value_1 = array->add_values();
  array_value_1->set_int_value(1337);
  AnyValue *array_value_2 = array->add_values();
  array_value_2->set_int_value(7331);
  std::string any_value_array_serialized = any_value_for_array.SerializeAsString();
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body",
                                      any_value_array_serialized.c_str(), any_value_array_serialized.length(),
                                      LM_VT_PROTOBUF);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(log_records.at(7).body().value_case(), AnyValue::kArrayValue);
  cr_assert_eq(log_records.at(7).body().array_value().values_size(), 2);
  cr_assert_eq(log_records.at(7).body().array_value().values().at(0).int_value(), 1337);
  cr_assert_eq(log_records.at(7).body().array_value().values().at(1).int_value(), 7331);

  log_msg_unref(msg);
}

Test(otel_protobuf_formatter, log_record_batching)
{
  ExportLogsServiceRequest request;
  std::string buf;
  LogMessage *msg = _create_log_msg_with_dummy_resource_and_scope();

  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string_body_0", -1, LM_VT_STRING);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(request.resource_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(0).scope_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(0).scope_logs().at(0).log_records_size(), 1);
  cr_assert_str_eq(request.resource_logs().at(0).scope_logs().at(0).log_records().at(0).body().string_value().c_str(),
                   "string_body_0");

  /* Everything same */
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string_body_1", -1, LM_VT_STRING);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(request.resource_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(0).scope_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(0).scope_logs().at(0).log_records_size(), 2);
  cr_assert_str_eq(request.resource_logs().at(0).scope_logs().at(0).log_records().at(1).body().string_value().c_str(),
                   "string_body_1");

  /* New Scope */
  log_msg_set_value_by_name_with_type(msg, ".otel.scope.name", "new_scope", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string_body_3", -1, LM_VT_STRING);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(request.resource_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(0).scope_logs_size(), 2);
  cr_assert_eq(request.resource_logs().at(0).scope_logs().at(1).log_records_size(), 1);
  cr_assert_str_eq(request.resource_logs().at(0).scope_logs().at(1).log_records().at(0).body().string_value().c_str(),
                   "string_body_3");

  /* New Scope Schema URL */
  log_msg_set_value_by_name_with_type(msg, ".otel.scope.schema_url", "new_scope_schema_url", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string_body_4", -1, LM_VT_STRING);

  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(request.resource_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(0).scope_logs_size(), 3);
  cr_assert_eq(request.resource_logs().at(0).scope_logs().at(2).log_records_size(), 1);
  cr_assert_str_eq(request.resource_logs().at(0).scope_logs().at(2).log_records().at(0).body().string_value().c_str(),
                   "string_body_4");

  /* New Resource */
  log_msg_set_value_by_name_with_type(msg, ".otel.resource.attributes.new_attr", "new_val", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string_body_5", -1, LM_VT_STRING);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(request.resource_logs_size(), 2);
  cr_assert_eq(request.resource_logs().at(1).scope_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(1).scope_logs().at(0).log_records_size(), 1);
  cr_assert_str_eq(request.resource_logs().at(1).scope_logs().at(0).log_records().at(0).body().string_value().c_str(),
                   "string_body_5");

  /* New Resource Schema URL */
  log_msg_set_value_by_name_with_type(msg, ".otel.resource.schema_url", "new_resource_schema_url", -1, LM_VT_STRING);
  log_msg_set_value_by_name_with_type(msg, ".otel.log.body", "string_body_6", -1, LM_VT_STRING);
  cr_assert(add_to_request(request, msg, configuration));
  cr_assert_eq(request.resource_logs_size(), 3);
  cr_assert_eq(request.resource_logs().at(2).scope_logs_size(), 1);
  cr_assert_eq(request.resource_logs().at(2).scope_logs().at(0).log_records_size(), 1);
  cr_assert_str_eq(request.resource_logs().at(2).scope_logs().at(0).log_records().at(0).body().string_value().c_str(),
                   "string_body_6");

  log_msg_unref(msg);
}

void
setup(void)
{
  app_startup();
  configuration = cfg_new_snippet();
}

void
teardown(void)
{
  cfg_free(configuration);
  app_shutdown();
}

TestSuite(otel_protobuf_formatter, .init = setup, .fini = teardown);
