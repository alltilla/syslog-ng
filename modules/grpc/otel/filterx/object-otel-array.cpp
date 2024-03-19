/*
 * Copyright (c) 2024 Attila Szakacs
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

#include "object-otel-array.hpp"
#include "otel-field.hpp"

#include "compat/cpp-start.h"
#include "filterx/object-primitive.h"
#include "filterx/object-string.h"
#include "compat/cpp-end.h"

#include <google/protobuf/reflection.h>
#include <stdexcept>

using namespace syslogng::grpc::otel::filterx;
using opentelemetry::proto::common::v1::AnyValue;

/* C++ Implementations */

Array::Array(FilterXOtelArray *s) :
  super(s),
  array(new ArrayValue()),
  borrowed(false)
{
}

Array::Array(FilterXOtelArray *s, ArrayValue *a) :
  super(s),
  array(a),
  borrowed(true)
{
}

Array::Array(const Array &o, FilterXOtelArray *s) :
  super(s),
  array(new ArrayValue()),
  borrowed(false)
{
  array->CopyFrom(*o.array);
}

Array::Array(FilterXOtelArray *s, FilterXObject *protobuf_object) :
  super(s),
  array(new ArrayValue()),
  borrowed(false)
{
  gsize length;
  const gchar *value = filterx_protobuf_get_value(protobuf_object, &length);

  if (!value)
    {
      delete array;
      throw std::runtime_error("Argument is not a protobuf object");
    }

  if (!array->ParsePartialFromArray(value, length))
    {
      delete array;
      throw std::runtime_error("Failed to parse from protobuf object");
    }
}

Array::~Array()
{
  if (!borrowed)
    delete array;
}

std::string
Array::marshal(void)
{
  return array->SerializePartialAsString();
}

bool
Array::set_subscript(uint64_t index, FilterXObject *value)
{
  return any_field_converter.FilterXObjectDirectSetter(array->mutable_values(index), value);
}

bool
Array::append(FilterXObject *value)
{
  return any_field_converter.FilterXObjectDirectSetter(array->add_values(), value);
}

FilterXObject *
Array::get_subscript(uint64_t index)
{
  AnyValue *any_value = array->mutable_values(index);
  return any_field_converter.FilterXObjectDirectGetter(any_value);
}

uint64_t
Array::len() const
{
  return (uint64_t) array->values_size();
}

const ArrayValue &
Array::get_value() const
{
  return *array;
}

/* C Wrappers */

static void
_free(FilterXObject *s)
{
  FilterXOtelArray *self = (FilterXOtelArray *) s;

  delete self->cpp;
  self->cpp = NULL;
}

static gboolean
_set_subscript(FilterXList *s, uint64_t index, FilterXObject *new_value)
{
  FilterXOtelArray *self = (FilterXOtelArray *) s;

  return self->cpp->set_subscript(index, new_value);
}

static gboolean
_append(FilterXList *s, FilterXObject *new_value)
{
  FilterXOtelArray *self = (FilterXOtelArray *) s;

  return self->cpp->append(new_value);
}

static FilterXObject *
_get_subscript(FilterXList *s, uint64_t index)
{
  FilterXOtelArray *self = (FilterXOtelArray *) s;

  return self->cpp->get_subscript(index);
}

static uint64_t
_len(FilterXList *s)
{
  FilterXOtelArray *self = (FilterXOtelArray *) s;

  return self->cpp->len();
}

static gboolean
_truthy(FilterXObject *s)
{
  return TRUE;
}

static gboolean
_marshal(FilterXObject *s, GString *repr, LogMessageValueType *t)
{
  FilterXOtelArray *self = (FilterXOtelArray *) s;

  std::string serialized = self->cpp->marshal();

  g_string_truncate(repr, 0);
  g_string_append_len(repr, serialized.c_str(), serialized.length());
  *t = LM_VT_PROTOBUF;
  return TRUE;
}

FilterXObject *
_filterx_otel_array_clone(FilterXObject *s)
{
  FilterXOtelArray *self = (FilterXOtelArray *) s;

  FilterXOtelArray *clone = g_new0(FilterXOtelArray, 1);
  filterx_list_init_instance(&clone->super, &FILTERX_TYPE_NAME(otel_array));

  clone->super.get_subscript = _get_subscript;
  clone->super.set_subscript = _set_subscript;
  clone->super.append = _append;
  clone->super.len = _len;

  try
    {
      clone->cpp = new Array(*self->cpp, clone);
    }
  catch (const std::runtime_error &)
    {
      g_assert_not_reached();
    }

  return &clone->super.super;
}

FilterXObject *
filterx_otel_array_new_from_args(GPtrArray *args)
{
  FilterXOtelArray *self = g_new0(FilterXOtelArray, 1);
  filterx_list_init_instance(&self->super, &FILTERX_TYPE_NAME(otel_array));

  self->super.get_subscript = _get_subscript;
  self->super.set_subscript = _set_subscript;
  self->super.append = _append;
  self->super.len = _len;

  try
    {
      if (!args || args->len == 0)
        self->cpp = new Array(self);
      else if (args->len == 1)
        self->cpp = new Array(self, (FilterXObject *) g_ptr_array_index(args, 0));
      else
        throw std::runtime_error("Invalid number of arguments");
    }
  catch (const std::runtime_error &e)
    {
      msg_error("FilterX: Failed to create OTel Array object", evt_tag_str("error", e.what()));
      filterx_object_unref(&self->super.super);
      return NULL;
    }

  return &self->super.super;
}

static FilterXObject *
_new_borrowed(ArrayValue *array)
{
  FilterXOtelArray *self = g_new0(FilterXOtelArray, 1);
  filterx_list_init_instance(&self->super, &FILTERX_TYPE_NAME(otel_array));

  self->super.get_subscript = _get_subscript;
  self->super.set_subscript = _set_subscript;
  self->super.append = _append;
  self->super.len = _len;

  self->cpp = new Array(self, array);

  return &self->super.super;
}

gpointer
grpc_otel_filterx_array_construct_new(Plugin *self)
{
  return (gpointer) &filterx_otel_array_new_from_args;
}

FilterXObject *
OtelArrayField::FilterXObjectGetter(google::protobuf::Message *message, ProtoReflectors reflectors)
{
  try
    {
      Message *nestedMessage = reflectors.reflection->MutableMessage(message, reflectors.fieldDescriptor);
      ArrayValue *array = dynamic_cast<ArrayValue *>(nestedMessage);
      return _new_borrowed(array);
    }
  catch(const std::bad_cast &e)
    {
      g_assert_not_reached();
    }
}

bool
OtelArrayField::FilterXObjectSetter(google::protobuf::Message *message, ProtoReflectors reflectors,
                                    FilterXObject *object)
{
  if (!filterx_object_is_type(object, &FILTERX_TYPE_NAME(otel_array)))
    {
      msg_error("otel-array: Failed to convert field, type is unsupported",
                evt_tag_str("field", reflectors.fieldDescriptor->name().c_str()),
                evt_tag_str("expected_type", reflectors.fieldDescriptor->type_name()),
                evt_tag_str("type", object->type->name));
      return false;
    }

  FilterXOtelArray *filterx_array = (FilterXOtelArray *) object;
  ArrayValue *array_value;

  try
    {
      array_value = dynamic_cast<ArrayValue *>(reflectors.reflection->MutableMessage(message, reflectors.fieldDescriptor));
    }
  catch(const std::bad_cast &e)
    {
      g_assert_not_reached();
    }

  array_value->CopyFrom(filterx_array->cpp->get_value());

  Array *new_array;
  try
    {
      new_array = new Array(filterx_array, array_value);
    }
  catch (const std::runtime_error &)
    {
      g_assert_not_reached();
    }

  delete filterx_array->cpp;
  filterx_array->cpp = new_array;

  return true;
}

OtelArrayField syslogng::grpc::otel::filterx::otel_array_converter;

FILTERX_DEFINE_TYPE(otel_array, FILTERX_TYPE_NAME(list),
                    .is_mutable = TRUE,
                    .marshal = _marshal,
                    .clone = _filterx_otel_array_clone,
                    .truthy = _truthy,
                    .list_factory = filterx_otel_array_new,
                    .dict_factory = filterx_otel_kvlist_new,
                    .free_fn = _free,
                   );
