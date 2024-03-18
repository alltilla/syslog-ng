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
#include "filterx/object-json-internal.h"
#include "filterx/object-null.h"
#include "filterx/object-primitive.h"
#include "filterx/object-string.h"
#include "filterx/filterx-weakrefs.h"
#include "filterx/object-dict-interface.h"

struct FilterXJsonObject_
{
  FilterXDict super;
  FilterXWeakRef root_container;
  struct json_object *object;
};

static gboolean
_truthy(FilterXObject *s)
{
  return TRUE;
}

static gboolean
_marshal(FilterXObject *s, GString *repr, LogMessageValueType *t)
{
  FilterXJsonObject *self = (FilterXJsonObject *) s;

  *t = LM_VT_JSON;

  const gchar *json_repr = json_object_to_json_string_ext(self->object, JSON_C_TO_STRING_PLAIN);
  g_string_append(repr, json_repr);

  return TRUE;
}

static gboolean
_map_to_json(FilterXObject *s, struct json_object **json_obj)
{
  FilterXJsonObject *self = (FilterXJsonObject *) s;

  *json_obj = json_object_get(self->object);
  return TRUE;
}

FilterXObject *
_clone(FilterXObject *s)
{
  FilterXJsonObject *self = (FilterXJsonObject *) s;

  struct json_object *json_obj = filterx_json_deep_copy(self->object);
  if (!json_obj)
    return NULL;

  return filterx_json_object_new_sub(json_obj, NULL);
}

static FilterXObject *
_get_subscript(FilterXDict *s, FilterXObject *key)
{
  FilterXJsonObject *self = (FilterXJsonObject *) s;

  const gchar *key_str = filterx_string_get_value(key, NULL);
  if (!key_str)
    return NULL;

  struct json_object *result = NULL;
  if (!json_object_object_get_ex(self->object, key_str, &result))
    return NULL;

  return filterx_json_convert_json_to_object_cached(&s->super, &self->root_container, result);
}

static gboolean
_set_subscript(FilterXDict *s, FilterXObject *key, FilterXObject *new_value)
{
  FilterXJsonObject *self = (FilterXJsonObject *) s;

  const gchar *key_str = filterx_string_get_value(key, NULL);
  if (!key_str)
    return FALSE;

  struct json_object *new_json_value = NULL;
  if (!filterx_object_map_to_json(new_value, &new_json_value))
    return FALSE;

  filterx_json_associate_cached_object(new_json_value, new_value);

  if (json_object_object_add(self->object, key_str, new_json_value) != 0)
    {
      json_object_put(new_json_value);
      return FALSE;
    }

  self->super.super.modified_in_place = TRUE;
  FilterXObject *root_container = filterx_weakref_get(&self->root_container);
  if (root_container)
    {
      root_container->modified_in_place = TRUE;
      filterx_object_unref(root_container);
    }

  return TRUE;
}

static guint64
_len(FilterXDict *s)
{
  FilterXJsonObject *self = (FilterXJsonObject *) s;

  return json_object_object_length(self->object);
}

/* NOTE: consumes root ref */
FilterXObject *
filterx_json_object_new_sub(struct json_object *json_obj, FilterXObject *root)
{
  FilterXJsonObject *self = g_new0(FilterXJsonObject, 1);
  filterx_dict_init_instance(&self->super, &FILTERX_TYPE_NAME(json_object));

  self->super.get_subscript = _get_subscript;
  self->super.set_subscript = _set_subscript;
  self->super.len = _len;

  filterx_weakref_set(&self->root_container, root);
  filterx_object_unref(root);
  self->object = json_obj;

  return &self->super.super;
}

static void
_free(FilterXObject *s)
{
  FilterXJsonObject *self = (FilterXJsonObject *) s;

  json_object_put(self->object);
  filterx_weakref_clear(&self->root_container);
}

FilterXObject *
filterx_json_object_new_from_repr(const gchar *repr, gssize repr_len)
{
  struct json_tokener *tokener = json_tokener_new();
  struct json_object *json_obj;

  json_obj = json_tokener_parse_ex(tokener, repr, repr_len < 0 ? strlen(repr) : repr_len);
  if (repr_len >= 0 && json_tokener_get_error(tokener) == json_tokener_continue)
    {
      /* pass the closing NUL character */
      json_obj = json_tokener_parse_ex(tokener, "", 1);
    }

  json_tokener_free(tokener);
  return filterx_json_object_new_sub(json_obj, NULL);
}

FilterXObject *
filterx_json_object_new_empty(void)
{
  return filterx_json_object_new_sub(json_object_new_object(), NULL);
}

FILTERX_DEFINE_TYPE(json_object, FILTERX_TYPE_NAME(dict),
                    .is_mutable = TRUE,
                    .truthy = _truthy,
                    .free_fn = _free,
                    .marshal = _marshal,
                    .map_to_json = _map_to_json,
                    .clone = _clone,
                    .list_factory = filterx_json_array_new_empty,
                    .dict_factory = filterx_json_object_new_empty,
                   );
