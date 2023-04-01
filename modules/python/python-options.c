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

#include "python-options.h"
#include "python-types.h"
#include "python-logtemplate.h"
#include "str-utils.h"
#include "string-list.h"

/* Python Option */

struct _PythonOption
{
  gchar *name;

  PyObject *(*create_value_py_object)(const PythonOption *s);
  PythonOption *(*clone)(const PythonOption *s);
  void (*free_fn)(PythonOption *s);
};

static void
python_option_init_instance(PythonOption *s, const gchar *name)
{
  s->name = __normalize_key(name);
}

const gchar *
python_option_get_name(const PythonOption *s)
{
  return s->name;
}

PyObject *
python_option_create_value_py_object(const PythonOption *s)
{
  g_assert(s->create_value_py_object);

  PyGILState_STATE gstate = PyGILState_Ensure();
  PyObject *value = s->create_value_py_object(s);
  PyGILState_Release(gstate);

  return value;
}

PythonOption *
python_option_clone(const PythonOption *s)
{
  g_assert(s->clone);
  return s->clone(s);
}

void
python_option_free(PythonOption *s)
{
  if (s->free_fn)
    s->free_fn(s);

  g_free(s->name);
  g_free(s);
}

/* String */

typedef struct _PythonOptionString
{
  PythonOption super;
  gchar *value;
} PythonOptionString;

static PyObject *
_string_create_value_py_object(const PythonOption *s)
{
  PythonOptionString *self = (PythonOptionString *) s;
  return py_string_from_string(self->value, -1);
}

static PythonOption *
_string_clone(const PythonOption *s)
{
  PythonOptionString *self = (PythonOptionString *) s;
  return python_option_string_new(python_option_get_name(s), self->value);
}

static void
_string_free_fn(PythonOption *s)
{
  PythonOptionString *self = (PythonOptionString *) s;
  g_free(self->value);
}

PythonOption *
python_option_string_new(const gchar *name, const gchar *value)
{
  PythonOptionString *self = g_new0(PythonOptionString, 1);
  python_option_init_instance(&self->super, name);

  self->super.create_value_py_object = _string_create_value_py_object;
  self->super.clone = _string_clone;
  self->super.free_fn = _string_free_fn;
  self->value = g_strdup(value);

  return &self->super;
}

/* Long */

typedef struct _PythonOptionLong
{
  PythonOption super;
  gint64 value;
} PythonOptionLong;

static PyObject *
_long_create_value_py_object(const PythonOption *s)
{
  PythonOptionLong *self = (PythonOptionLong *) s;
  return py_long_from_long(self->value);
}

static PythonOption *
_long_clone(const PythonOption *s)
{
  PythonOptionLong *self = (PythonOptionLong *) s;
  return python_option_long_new(python_option_get_name(s), self->value);
}

PythonOption *
python_option_long_new(const gchar *name, gint64 value)
{
  PythonOptionLong *self = g_new0(PythonOptionLong, 1);
  python_option_init_instance(&self->super, name);

  self->super.create_value_py_object = _long_create_value_py_object;
  self->super.clone = _long_clone;
  self->value = value;

  return &self->super;
}

/* Double */

typedef struct _PythonOptionDouble
{
  PythonOption super;
  gdouble value;
} PythonOptionDouble;

static PyObject *
_double_create_value_py_object(const PythonOption *s)
{
  PythonOptionDouble *self = (PythonOptionDouble *) s;
  return py_double_from_double(self->value);
}

static PythonOption *
_double_clone(const PythonOption *s)
{
  PythonOptionDouble *self = (PythonOptionDouble *) s;
  return python_option_double_new(python_option_get_name(s), self->value);
}

PythonOption *
python_option_double_new(const gchar *name, gdouble value)
{
  PythonOptionDouble *self = g_new0(PythonOptionDouble, 1);
  python_option_init_instance(&self->super, name);

  self->super.create_value_py_object = _double_create_value_py_object;
  self->super.clone = _double_clone;
  self->value = value;

  return &self->super;
}

/* Boolean */

typedef struct _PythonOptionBoolean
{
  PythonOption super;
  gboolean value;
} PythonOptionBoolean;

static PyObject *
_boolean_create_value_py_object(const PythonOption *s)
{
  PythonOptionBoolean *self = (PythonOptionBoolean *) s;
  return py_boolean_from_boolean(self->value);
}

static PythonOption *
_boolean_clone(const PythonOption *s)
{
  PythonOptionBoolean *self = (PythonOptionBoolean *) s;
  return python_option_boolean_new(python_option_get_name(s), self->value);
}

PythonOption *
python_option_boolean_new(const gchar *name, gboolean value)
{
  PythonOptionBoolean *self = g_new0(PythonOptionBoolean, 1);
  python_option_init_instance(&self->super, name);

  self->super.create_value_py_object = _boolean_create_value_py_object;
  self->super.clone = _boolean_clone;
  self->value = value;

  return &self->super;
}

/* String List */

typedef struct _PythonOptionStringList
{
  PythonOption super;
  GList *value;
} PythonOptionStringList;

static PyObject *
_string_list_create_value_py_object(const PythonOption *s)
{
  PythonOptionStringList *self = (PythonOptionStringList *) s;
  return py_string_list_from_string_list(self->value);
}

static PythonOption *
_string_list_clone(const PythonOption *s)
{
  PythonOptionStringList *self = (PythonOptionStringList *) s;
  return python_option_string_list_new(python_option_get_name(s), self->value);
}

static void
_string_list_free_fn(PythonOption *s)
{
  PythonOptionStringList *self = (PythonOptionStringList *) s;
  string_list_free(self->value);
}

PythonOption *
python_option_string_list_new(const gchar *name, const GList *value)
{
  PythonOptionStringList *self = g_new0(PythonOptionStringList, 1);
  python_option_init_instance(&self->super, name);

  self->super.create_value_py_object = _string_list_create_value_py_object;
  self->super.clone = _string_list_clone;
  self->super.free_fn = _string_list_free_fn;
  self->value = string_list_clone(value);

  return &self->super;
}

/* Template */

typedef struct _PythonOptionTemplate
{
  PythonOption super;
  gchar *value;
} PythonOptionTemplate;

static PyObject *
_template_create_value_py_object(const PythonOption *s)
{
  PythonOptionTemplate *self = (PythonOptionTemplate *) s;
  PyObject *template_str = py_string_from_string(self->value, -1);
  PyObject *args = PyTuple_Pack(1, template_str);
  PyObject *py_template = PyObject_Call((PyObject *) &py_log_template_type, args, NULL);
  Py_DECREF(template_str);
  Py_DECREF(args);
  return py_template;
}

static PythonOption *
_template_clone(const PythonOption *s)
{
  PythonOptionTemplate *self = (PythonOptionTemplate *) s;
  return python_option_template_new(python_option_get_name(s), self->value);
}

static void
_template_free_fn(PythonOption *s)
{
  PythonOptionTemplate *self = (PythonOptionTemplate *) s;
  g_free(self->value);
}

PythonOption *
python_option_template_new(const gchar *name, const gchar *value)
{
  PythonOptionTemplate *self = g_new0(PythonOptionTemplate, 1);
  python_option_init_instance(&self->super, name);

  self->super.create_value_py_object = _template_create_value_py_object;
  self->super.clone = _template_clone;
  self->super.free_fn = _template_free_fn;
  self->value = g_strdup(value);

  return &self->super;
}

/* Python Options */

struct _PythonOptions
{
  GList *options;
};

PythonOptions *
python_options_new(void)
{
  PythonOptions *self = g_new0(PythonOptions, 1);
  return self;
}

void
python_options_add_option(PythonOptions *self, const PythonOption *option)
{
  self->options = g_list_append(self->options, python_option_clone(option));
}

PyObject *
python_options_create_py_dict(const PythonOptions *self)
{
  PyObject *py_dict;

  PyGILState_STATE gstate = PyGILState_Ensure();
  {
    py_dict = PyDict_New();
    for (GList *elem = self->options; elem; elem = elem->next)
      {
        const PythonOption *option = (const PythonOption *) elem->data;
        PyDict_SetItemString(py_dict,
                             python_option_get_name(option),
                             python_option_create_value_py_object(option));
      }
  }
  PyGILState_Release(gstate);

  return py_dict;
}

PythonOptions *
python_options_clone(const PythonOptions *self)
{
  PythonOptions *cloned = python_options_new();

  for (GList *elem = self->options; elem; elem = elem->next)
    {
      const PythonOption *option = (const PythonOption *) elem->data;
      python_options_add_option(cloned, option);
    }

  return cloned;
}

void
python_options_free(PythonOptions *self)
{
  if (!self)
    return;

  g_list_free_full(self->options, (GDestroyNotify) python_option_free);
  g_free(self);
}
