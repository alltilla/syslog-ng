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
#include "filterx/expr-setattr.h"
#include "filterx/object-primitive.h"

typedef struct _FilterXSetAttr
{
  FilterXExpr super;
  FilterXExpr *object;
  gchar *attr_name;
  FilterXExpr *new_value;
} FilterXSetAttr;

static FilterXObject *
_eval(FilterXExpr *s)
{
  FilterXSetAttr *self = (FilterXSetAttr *) s;
  FilterXObject *result = NULL;

  FilterXObject *object = filterx_expr_eval_typed(self->object);
  if (!object)
    return NULL;

  FilterXObject *new_value = filterx_expr_eval_typed(self->new_value);
  if (!new_value)
    goto exit;

  result = filterx_object_clone(new_value);
  filterx_object_unref(new_value);

  if (!filterx_object_setattr(object, self->attr_name, result))
    {
      filterx_object_unref(result);
      result = NULL;
    }

exit:
  filterx_object_unref(object);
  return result;
}

static void
_free(FilterXExpr *s)
{
  FilterXSetAttr *self = (FilterXSetAttr *) s;

  g_free(self->attr_name);
  filterx_expr_unref(self->object);
  filterx_expr_unref(self->new_value);
}

FilterXExpr *
filterx_setattr_new(FilterXExpr *object, const gchar *attr_name, FilterXExpr *new_value)
{
  FilterXSetAttr *self = g_new0(FilterXSetAttr, 1);

  filterx_expr_init_instance(&self->super);
  self->super.eval = _eval;
  self->super.free_fn = _free;
  self->object = object;
  self->attr_name = g_strdup(attr_name);
  self->new_value = new_value;
  return &self->super;
}
