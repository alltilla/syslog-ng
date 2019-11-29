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
  StringMatchMode mode;
  gchar *pattern;
  GPatternSpec *glob;
  pcre *pcre;
  pcre_extra *pcre_extra;
} StringMatcher;

static gboolean
string_matcher_prepare_glob(StringMatcher *self)
{
  self->glob = g_pattern_spec_new(self->pattern);

  return TRUE;
}

static gboolean
string_matcher_prepare_pcre(StringMatcher *self)
{
  const gchar *errptr;
  gint erroffset;
  gint rc;

  self->pcre = pcre_compile2(self->pattern, PCRE_ANCHORED, &rc, &errptr, &erroffset, NULL);
  if (!self->pcre)
    {
      msg_error("Error while compiling regular expression",
                evt_tag_str("regular_expression", self->pattern),
                evt_tag_str("error_at", &self->pattern[erroffset]),
                evt_tag_int("error_offset", erroffset),
                evt_tag_str("error_message", errptr),
                evt_tag_int("error_code", rc));
      return FALSE;
    }
  self->pcre_extra = pcre_study(self->pcre, PCRE_STUDY_JIT_COMPILE, &errptr);
  if (errptr)
    {
      msg_error("Error while optimizing regular expression",
                evt_tag_str("regular_expression", self->pattern),
                evt_tag_str("error_message", errptr));
      pcre_free(self->pcre);
      if (self->pcre_extra)
        pcre_free_study(self->pcre_extra);
      return FALSE;
    }

  return TRUE;
}

gboolean
string_matcher_prepare(StringMatcher *self)
{
  switch (self->mode)
    {
    case SMM_GLOB:
      return string_matcher_prepare_glob(self);
    case SMM_PCRE:
      return string_matcher_prepare_pcre(self);
    default:
      return TRUE;
    }
}

static gboolean
string_matcher_match_pcre(StringMatcher *self, const char *string, gsize string_len)
{
  gint rc;
  gint num_matches;

  if (pcre_fullinfo(self->pcre, self->pcre_extra, PCRE_INFO_CAPTURECOUNT, &num_matches) < 0)
    g_assert_not_reached();
  if (num_matches > 256)
    num_matches = 256;

  gsize matches_size = 3 * (num_matches + 1);
  gint *matches = g_alloca(matches_size * sizeof(gint));

  rc = pcre_exec(self->pcre, self->pcre_extra, string, string_len, 0, 0, matches, matches_size);
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

gboolean
string_matcher_match(StringMatcher *self, const char *string, gsize string_len)
{
  switch (self->mode)
    {
    case SMM_LITERAL:
      return (strcmp(string, self->pattern) == 0);
    case SMM_PREFIX:
      return (strncmp(string, self->pattern, strlen(self->pattern)) == 0);
    case SMM_SUBSTRING:
      return (strstr(string, self->pattern) != NULL);
    case SMM_GLOB:
      return (g_pattern_match_string(self->glob, string));
    case SMM_PCRE:
      return (string_matcher_match_pcre(self, string, string_len));
    default:
      g_assert_not_reached();
    }
}

StringMatcher *
string_matcher_new(StringMatchMode mode, const gchar *pattern)
{
  StringMatcher *self = g_new0(StringMatcher, 1);

  self->mode = mode;
  self->pattern = g_strdup(pattern);

  return self;
}

void
string_matcher_free(StringMatcher *self)
{
  if (self->pattern)
    g_free(self->pattern);
  if (self->glob)
    g_pattern_spec_free(self->glob);
  if (self->pcre)
    pcre_free(self->pcre);
  if (self->pcre_extra)
    pcre_free_study(self->pcre_extra);
  g_free(self);
}
