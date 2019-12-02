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

#include "str-matcher.h"
#include "compat/pcre.h"
#include "messages.h"

#include <string.h>

typedef struct _StringMatcher
{
  gchar *pattern;
  gboolean prepared;

  gboolean (*prepare_fn)(StringMatcher *self, gpointer user_data);
  gboolean (*match_fn)(StringMatcher *self, const char *string, gsize string_len, gpointer user_data);
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
string_matcher_match(StringMatcher *self, const char *string, gsize string_len, gpointer user_data)
{
  g_assert((self->prepare_fn && self->prepared) || (!self->prepare_fn));

  if (self->match_fn)
    return self->match_fn(self, string, string_len, user_data);
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
string_matcher_literal_match(StringMatcher *s, const char *string, gsize string_len, gpointer user_data)
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
string_matcher_prefix_match(StringMatcher *s, const char *string, gsize string_len, gpointer user_data)
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
string_matcher_substring_match(StringMatcher *s, const char *string, gsize string_len, gpointer user_data)
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

typedef struct _StringMatcherGlob
{
  StringMatcher super;
  GPatternSpec *glob;
} StringMatcherGlob;

static gboolean
string_matcher_glob_prepare(StringMatcher *s, gpointer user_data)
{
  StringMatcherGlob *self = (StringMatcherGlob *)s;

  self->glob = g_pattern_spec_new(s->pattern);
  return TRUE;
}

static gboolean
string_matcher_glob_match(StringMatcher *s, const char *string, gsize string_len, gpointer user_data)
{
  StringMatcherGlob *self = (StringMatcherGlob *)s;

  return g_pattern_match_string(self->glob, string);
}

static void
string_matcher_glob_free(StringMatcher *s)
{
  StringMatcherGlob *self = (StringMatcherGlob *)s;

  if (self->glob)
    g_pattern_spec_free(self->glob);
}

StringMatcher *
string_matcher_glob_new(const gchar *pattern)
{
  StringMatcherGlob *self = g_new0(StringMatcherGlob, 1);

  string_matcher_init_instance(&self->super, pattern);
  self->super.prepare_fn = string_matcher_glob_prepare;
  self->super.match_fn = string_matcher_glob_match;
  self->super.free_fn = string_matcher_glob_free;

  return &self->super;
}

typedef struct _StringMatcherPcre
{
  StringMatcher super;
  pcre *pcre;
  pcre_extra *pcre_extra;
  gint max_matches;
} StringMatcherPcre;

static StringMatcherPcrePrepareOptions
string_matcher_pcre_prepare_options_default()
{
  static StringMatcherPcrePrepareOptions options = {
    .compile_flags = PCRE_ANCHORED,
    .study_flags = PCRE_STUDY_JIT_COMPILE
  };

  return options;
}

static gboolean
string_matcher_pcre_prepare(StringMatcher *s, gpointer user_data)
{
  StringMatcherPcre *self = (StringMatcherPcre *)s;
  StringMatcherPcrePrepareOptions options;
  const gchar *errptr;
  gint erroffset;
  gint rc;

  if (user_data)
    options = *(StringMatcherPcrePrepareOptions *)user_data;
  else
    options = string_matcher_pcre_prepare_options_default();

  self->pcre = pcre_compile2(s->pattern, options.compile_flags, &rc, &errptr, &erroffset, NULL);
  if (!self->pcre)
    {
      msg_error("Error while compiling regular expression",
                evt_tag_str("regular_expression", s->pattern),
                evt_tag_str("error_at", &s->pattern[erroffset]),
                evt_tag_int("error_offset", erroffset),
                evt_tag_str("error_message", errptr),
                evt_tag_int("error_code", rc));
      return FALSE;
    }
  self->pcre_extra = pcre_study(self->pcre, options.study_flags, &errptr);
  if (errptr)
    {
      msg_error("Error while optimizing regular expression",
                evt_tag_str("regular_expression", s->pattern),
                evt_tag_str("error_message", errptr));
      pcre_free(self->pcre);
      if (self->pcre_extra)
        pcre_free_study(self->pcre_extra);
      return FALSE;
    }

  return TRUE;
}

static StringMatcherPcreMatchOptions
string_matcher_pcre_match_options_default()
{
  static StringMatcherPcreMatchOptions options = {
    .match_flags = 0,
    .max_matches = STRING_MATCHER_PCRE_NO_LIMIT,
    .matches = NULL,
    .matches_size = 0,
  };

  return options;
}

gsize
string_matcher_pcre_get_matches_size(StringMatcher *s, gint max_matches)
{
  StringMatcherPcre *self = (StringMatcherPcre *)s;
  gint num_matches;

  g_assert(self->super.prepared);

  if (pcre_fullinfo(self->pcre, self->pcre_extra, PCRE_INFO_CAPTURECOUNT, &num_matches) < 0)
    g_assert_not_reached();

  if (max_matches != STRING_MATCHER_PCRE_NO_LIMIT && num_matches > max_matches)
    num_matches = max_matches;

  return 3 * (num_matches + 1);
}

static gboolean
string_matcher_pcre_match(StringMatcher *s, const char *string, gsize string_len, gpointer user_data)
{
  StringMatcherPcre *self = (StringMatcherPcre *)s;
  StringMatcherPcreMatchOptions options;
  gint rc;
  gint *matches;
  gsize matches_size;

  if (user_data)
    {
      options = *(StringMatcherPcreMatchOptions *)user_data;
      matches_size = options.matches_size;
      matches = options.matches;
    }
  else
    {
      options = string_matcher_pcre_match_options_default();
      matches_size = string_matcher_pcre_get_matches_size(&self->super, options.max_matches);
      matches = g_alloca(matches_size * sizeof(gint));
    }

  rc = pcre_exec(self->pcre, self->pcre_extra, string, string_len, 0, options.match_flags, matches, matches_size);
  if (rc == PCRE_ERROR_NOMATCH)
    {
      return FALSE;
    }
  if (rc < 0)
    {
      msg_error("Error while matching pcrep", evt_tag_int("error_code", rc));
      return FALSE;
    }
  if (rc == 0)
    {
      msg_error("Error while storing matching substrings");
      return FALSE;
    }
  return TRUE;
}

static void
string_matcher_pcre_free(StringMatcher *s)
{
  StringMatcherPcre *self = (StringMatcherPcre *)s;

  if (self->pcre)
    pcre_free(self->pcre);
  if (self->pcre_extra)
    pcre_free_study(self->pcre_extra); 
}

StringMatcher *
string_matcher_pcre_new(const gchar *pattern)
{
  StringMatcherPcre *self = g_new0(StringMatcherPcre, 1);

  string_matcher_init_instance(&self->super, pattern);
  self->super.prepare_fn = string_matcher_pcre_prepare;
  self->super.match_fn = string_matcher_pcre_match;
  self->super.free_fn = string_matcher_pcre_free;

  return &self->super;
}
