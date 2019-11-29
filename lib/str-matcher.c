/*
 * Copyright (c) 2019 Balabit
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

#include "str-matcher.h"
#include "compat/pcre.h"
#include "messages.h"

#include <string.h>

typedef struct _StringMatcher
{
  gchar *pattern;
  gboolean prepared;

  gboolean (*prepare_fn)(StringMatcher *self, gpointer user_data);
  gboolean (*match_fn)(StringMatcher *self, const char *string, gsize string_len);
  void (*free_fn)(StringMatcher *self);
} StringMatcher;

gboolean
string_matcher_prepare(StringMatcher *self, gpointer user_data)
{
  gboolean result = TRUE;

  if (self->prepare_fn)
    result = self->prepare_fn(self, user_data);

  self->prepared = result;

  return result;
}

gboolean
string_matcher_match(StringMatcher *self, const char *string, gsize string_len)
{
  g_assert((self->prepare_fn && self->prepared) || (!self->prepare_fn));

  if (self->match_fn)
    return self->match_fn(self, string, string_len);
  else
    g_assert_not_reached();
}

static void
string_matcher_init_instance(StringMatcher *self, const gchar *pattern)
{
  self->pattern = g_strdup(pattern);
}

void
string_matcher_free(StringMatcher *self)
{
  if (self->free_fn)
    self->free_fn(self);
  g_free(self->pattern);
  g_free(self);
}

static gboolean
string_matcher_literal_match(StringMatcher *s, const char *string, gsize string_len)
{
  return (strcmp(string, s->pattern) == 0);
}

StringMatcher *
string_matcher_literal_new(const gchar *pattern)
{
  StringMatcher *self = g_new0(StringMatcher, 1);

  string_matcher_init_instance(self, pattern);
  self->match_fn = string_matcher_literal_match;

  return self;
}

static gboolean
string_matcher_prefix_match(StringMatcher *s, const char *string, gsize string_len)
{
  return (strncmp(string, s->pattern, strlen(s->pattern)) == 0);
}

StringMatcher *
string_matcher_prefix_new(const gchar *pattern)
{
  StringMatcher *self = g_new0(StringMatcher, 1);

  string_matcher_init_instance(self, pattern);
  self->match_fn = string_matcher_prefix_match;

  return self;
}

static gboolean
string_matcher_substring_match(StringMatcher *s, const char *string, gsize string_len)
{
  return (strstr(string, s->pattern) != NULL);
}

StringMatcher *
string_matcher_substring_new(const gchar *pattern)
{
  StringMatcher *self = g_new0(StringMatcher, 1);

  string_matcher_init_instance(self, pattern);
  self->match_fn = string_matcher_substring_match;

  return self;
}
