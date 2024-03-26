/*
 * Copyright (c) 2023 Balazs Scheidler <balazs.scheidler@axoflow.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * As an additional exemption you are allowed to compile & link against the
 * OpenSSL libraries as published by the OpenSSL project. See the file
 * COPYING for details.
 *
 */
#include <criterion/criterion.h>
#include "filterx/object-json.h"
#include "apphook.h"
#include "filterx-lib.h"

static void
assert_object_json_equals(FilterXObject *obj, const gchar *expected_json_repr)
{
  struct json_object *jso = NULL;

  cr_assert(filterx_object_map_to_json(obj, &jso) == TRUE, "error mapping to json, expected json was: %s",
            expected_json_repr);
  const gchar *json_repr = json_object_to_json_string_ext(jso, JSON_C_TO_STRING_PLAIN);
  cr_assert_str_eq(json_repr, expected_json_repr);
  json_object_put(jso);
}

Test(filterx_json, test_filterx_object_json_from_repr)
{
  FilterXObject *fobj;

  fobj = filterx_json_new_from_repr("{\"foo\": \"foovalue\"}", -1);
  cr_assert(filterx_object_is_type(fobj, &FILTERX_TYPE_NAME(json_object)));
  assert_object_json_equals(fobj, "{\"foo\":\"foovalue\"}");
  assert_marshaled_object(fobj, "{\"foo\":\"foovalue\"}", LM_VT_JSON);
  filterx_object_unref(fobj);

  fobj = filterx_json_new_from_repr("[\"foo\", \"bar\"]", -1);
  cr_assert(filterx_object_is_type(fobj, &FILTERX_TYPE_NAME(json_array)));
  assert_object_json_equals(fobj, "[\"foo\",\"bar\"]");
  assert_marshaled_object(fobj, "foo,bar", LM_VT_LIST);
  filterx_object_unref(fobj);

  fobj = filterx_json_new_from_repr("[1, 2]", -1);
  cr_assert(filterx_object_is_type(fobj, &FILTERX_TYPE_NAME(json_array)));
  assert_object_json_equals(fobj, "[1,2]");
  assert_marshaled_object(fobj, "[1,2]", LM_VT_JSON);
  filterx_object_unref(fobj);

  fobj = filterx_json_array_new_from_syslog_ng_list("\"foo\",bar", -1);
  cr_assert(filterx_object_is_type(fobj, &FILTERX_TYPE_NAME(json_array)));
  assert_object_json_equals(fobj, "[\"foo\",\"bar\"]");
  assert_marshaled_object(fobj, "foo,bar", LM_VT_LIST);
  filterx_object_unref(fobj);

  fobj = filterx_json_array_new_from_syslog_ng_list("1,2", -1);
  cr_assert(filterx_object_is_type(fobj, &FILTERX_TYPE_NAME(json_array)));
  assert_object_json_equals(fobj, "[\"1\",\"2\"]");
  assert_marshaled_object(fobj, "1,2", LM_VT_LIST);
  filterx_object_unref(fobj);
}

static void
setup(void)
{
  app_startup();
}

static void
teardown(void)
{
  app_shutdown();
}

TestSuite(filterx_json, .init = setup, .fini = teardown);
