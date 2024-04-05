/*
 * Copyright (c) 2024 Attila Szakacs
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

#include "filterx/object-list-interface.h"
#include "filterx/object-primitive.h"

guint64
filterx_list_len(FilterXObject *s)
{
  FilterXList *self = (FilterXList *) s;
  return self->len(self);
}

FilterXObject *
filterx_list_get_subscript(FilterXObject *s, gint64 index)
{
  FilterXObject *index_obj = filterx_integer_new(index);
  FilterXObject *result = filterx_object_get_subscript(s, index_obj);

  filterx_object_unref(index_obj);
  return result;
}

gboolean
filterx_list_set_subscript(FilterXObject *s, gint64 index, FilterXObject *new_value)
{
  FilterXObject *index_obj = filterx_integer_new(index);
  gboolean result = filterx_object_set_subscript(s, index_obj, new_value);

  filterx_object_unref(index_obj);
  return result;
}

gboolean
filterx_list_append(FilterXObject *s, FilterXObject *new_value)
{
  return filterx_object_set_subscript(s, NULL, new_value);
}

static gboolean
_normalize_index(FilterXList *self, gint64 index, guint64 *normalized_index, const gchar **error)
{
  guint64 len = filterx_list_len(&self->super);

  if (index >= 0)
    {
      if (index >= len)
        {
          *error = "Index out of range";
          return FALSE;
        }

      *normalized_index = (guint64) index;
      return TRUE;
    }

  if (len > G_MAXINT64)
    {
      *error = "Index exceeds maximal supported value";
      return FALSE;
    }

  *normalized_index = len + index;
  if (*normalized_index < 0)
    {
      *error = "Index out of range";
      return FALSE;
    }

  return TRUE;
}

static FilterXObject *
_get_subscript(FilterXObject *s, FilterXObject *key)
{
  FilterXList *self = (FilterXList *) s;

  gint64 index;
  if (!filterx_integer_unwrap(key, &index))
    {
      msg_error("FilterX: Failed to get element from list",
                evt_tag_str("error", "Index must be integer"),
                evt_tag_str("index_type", key->type->name));
      return NULL;
    }

  guint64 normalized_index;
  const gchar *error;
  if (!_normalize_index(self, index, &normalized_index, &error))
    {
      msg_error("FilterX: Failed to get element from list",
                evt_tag_str("error", error),
                evt_tag_printf("index", "%" G_GINT64_FORMAT, index),
                evt_tag_printf("len", "%" G_GUINT64_FORMAT, filterx_list_len(s)));
      return NULL;
    }

  return self->get_subscript(self, normalized_index);
}

static gboolean
_set_subscript(FilterXObject *s, FilterXObject *key, FilterXObject *new_value)
{
  FilterXList *self = (FilterXList *) s;

  if (!key)
    return self->append(self, new_value);

  gint64 index;
  if (!filterx_integer_unwrap(key, &index))
    {
      msg_error("FilterX: Failed to set element of list",
                evt_tag_str("error", "Index must be integer"),
                evt_tag_str("index_type", key->type->name));
      return FALSE;
    }

  guint64 normalized_index;
  const gchar *error;
  if (!_normalize_index(self, index, &normalized_index, &error))
    {
      msg_error("FilterX: Failed to set element of list",
                evt_tag_str("error", error),
                evt_tag_printf("index", "%" G_GINT64_FORMAT, index),
                evt_tag_printf("len", "%" G_GUINT64_FORMAT, filterx_list_len(s)));
      return FALSE;
    }

  return self->set_subscript(self, normalized_index, new_value);
}

static gboolean
_has_subscript(FilterXObject *s, FilterXObject *key)
{
  FilterXList *self = (FilterXList *) s;

  if (!key)
    {
      msg_error("FilterX: Failed to check index of list",
                evt_tag_str("error", "Index must be sey"));
      return FALSE;
    }

  gint64 index;
  if (!filterx_integer_unwrap(key, &index))
    {
      msg_error("FilterX: Failed to check index of list",
                evt_tag_str("error", "Index must be integer"),
                evt_tag_str("index_type", key->type->name));
      return FALSE;
    }

  guint64 normalized_index;
  const gchar *error;
  return _normalize_index(self, index, &normalized_index, &error);
}

static gboolean
_unset_key(FilterXObject *s, FilterXObject *key)
{
  FilterXList *self = (FilterXList *) s;

  if (!key)
    {
      msg_error("FilterX: Failed to unset element of list",
                evt_tag_str("error", "Index must be set"));
      return FALSE;
    }

  gint64 index;
  if (!filterx_integer_unwrap(key, &index))
    {
      msg_error("FilterX: Failed to unset element of list",
                evt_tag_str("error", "Index must be integer"),
                evt_tag_str("index_type", key->type->name));
      return FALSE;
    }

  guint64 normalized_index;
  const gchar *error;
  if (!_normalize_index(self, index, &normalized_index, &error))
    {
      msg_error("FilterX: Failed to unset element of list",
                evt_tag_str("error", error),
                evt_tag_printf("index", "%" G_GINT64_FORMAT, index),
                evt_tag_printf("len", "%" G_GUINT64_FORMAT, filterx_list_len(s)));
      return FALSE;
    }

  return self->unset_index(self, normalized_index);
}

void
filterx_list_init_instance(FilterXList *self, FilterXType *type)
{
  g_assert(type->is_mutable);
  g_assert(type->get_subscript == _get_subscript);
  g_assert(type->set_subscript == _set_subscript);
  g_assert(type->has_subscript == _has_subscript);
  g_assert(type->unset_key == _unset_key);

  filterx_object_init_instance(&self->super, type);
}

FILTERX_DEFINE_TYPE(list, FILTERX_TYPE_NAME(object),
                    .is_mutable = TRUE,
                    .get_subscript = _get_subscript,
                    .set_subscript = _set_subscript,
                    .has_subscript = _has_subscript,
                    .unset_key = _unset_key,
                   );
