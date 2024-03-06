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
#include "expr-dict.h"
#include "object-json.h"
#include "object-message-value.h"
#include "scratch-buffers.h"
#include "compat/json.h"

struct _FilterXKeyValue
{
  gchar *key;
  FilterXExpr *value_expr;
};

FilterXKeyValue *
filterx_kv_new(const gchar *key, FilterXExpr *value_expr)
{
  FilterXKeyValue *self = g_new0(FilterXKeyValue, 1);
  self->key = g_strdup(key);
  self->value_expr = value_expr;
  return self;
}

void
filterx_kv_free(FilterXKeyValue *self)
{
  g_free(self->key);
  filterx_expr_unref(self->value_expr);
  g_free(self);
}

typedef struct _FilterXDictExpr
{
  FilterXExpr super;
  GList *key_values;
} FilterXDictExpr;

static gboolean
_eval_key_value(FilterXDictExpr *self, FilterXObject *object, FilterXKeyValue *kv)
{
  FilterXObject *value = filterx_expr_eval_typed(kv->value_expr);
  if (!value)
    return FALSE;

  if (filterx_object_is_type(value, &FILTERX_TYPE_NAME(message_value)))
    {
      FilterXObject *cloned_value = filterx_object_clone(value);
      filterx_object_unref(value);
      value = cloned_value;
    }

  gboolean result = filterx_object_setattr(object, kv->key, value);
  filterx_object_unref(value);
  return result;
}

static FilterXObject *
_eval(FilterXExpr *s)
{
  FilterXDictExpr *self = (FilterXDictExpr *) s;
  FilterXObject *object = filterx_json_new(json_object_new_object());

  for (GList *l = self->key_values; l; l = l->next)
    {
      if (!_eval_key_value(self, object, l->data))
        goto fail;
    }
  return object;
fail:
  filterx_object_unref(object);
  return NULL;
}

static void
_free(FilterXExpr *s)
{
  FilterXDictExpr *self = (FilterXDictExpr *) s;

  g_list_free_full(self->key_values, (GDestroyNotify) filterx_kv_free);
}

FilterXExpr *
filterx_dict_expr_new(GList *key_values)
{
  FilterXDictExpr *self = g_new0(FilterXDictExpr, 1);

  filterx_expr_init_instance(&self->super);
  self->super.eval = _eval;
  self->super.free_fn = _free;
  self->key_values = key_values;
  return &self->super;
}
