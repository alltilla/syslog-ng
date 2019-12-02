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

#ifndef STR_MATCHER_H_INCLUDED
#define STR_MATCHER_H_INCLUDED

#include "syslog-ng.h"

typedef struct _StringMatcher StringMatcher;

gboolean string_matcher_prepare(StringMatcher *self, gpointer user_data);
gboolean string_matcher_match(StringMatcher *self, const char *string, gsize string_len);
void string_matcher_free(StringMatcher *self);

StringMatcher *string_matcher_literal_new(const gchar *pattern);
StringMatcher *string_matcher_prefix_new(const gchar *pattern);
StringMatcher *string_matcher_substring_new(const gchar *pattern);
StringMatcher *string_matcher_glob_new(const gchar *pattern);

#endif