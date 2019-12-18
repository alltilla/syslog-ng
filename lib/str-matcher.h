/*
 * Copyright (c) 2019 One Identity
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
#include "compat/pcre.h"

typedef struct _StringMatcher StringMatcher;

gboolean string_matcher_prepare(StringMatcher *self, gpointer user_data);
gboolean string_matcher_match(StringMatcher *self, const char *string, gsize string_len, gpointer user_data);
void string_matcher_free(StringMatcher *self);
const gchar *string_matcher_get_pattern(StringMatcher *self);

StringMatcher *string_matcher_literal_new(const gchar *pattern);
StringMatcher *string_matcher_prefix_new(const gchar *pattern);
StringMatcher *string_matcher_substring_new(const gchar *pattern);
StringMatcher *string_matcher_glob_new(const gchar *pattern);
StringMatcher *string_matcher_pcre_new(const gchar *pattern);

#define STRING_MATCHER_PCRE_NO_LIMIT -1

typedef struct _StringMatcherPcrePrepareParams
{
  gint compile_flags;
  gint study_flags;
  const guchar *table;
  gint max_matches;
} StringMatcherPcrePrepareParams;

typedef struct _StringMatcherPcreMatchParams
{
  gint match_flags;
  gint *matches;
  gint *match_num;
  gint offset;
} StringMatcherPcreMatchParams;

void string_matcher_pcre_prepare_params_defaults(StringMatcherPcrePrepareParams *params);
void string_matcher_pcre_match_params_defaults(StringMatcherPcreMatchParams *params);
gint string_matcher_pcre_get_matches_size(StringMatcher *s);
pcre *string_matcher_pcre_get_pcre(StringMatcher *s);
pcre_extra *string_matcher_pcre_get_pcre_extra(StringMatcher *s);

#endif
