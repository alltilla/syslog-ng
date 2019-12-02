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

#include "syslog-ng.h"
#include "str-matcher.h"

#include <criterion/criterion.h>
#include <criterion/parameterized.h>

typedef struct _StringMatcherParams
{
  gchar *pattern;
  gchar *test_string;
  gboolean match;
  gboolean prepare;
  gpointer prepare_user_data;
  gpointer match_user_data;
} StringMatcherParams;

ParameterizedTestParameters(str_matcher, test_literal)
{
  static StringMatcherParams test_params[] = {
    { .prepare = FALSE, .pattern = "almafa", .test_string = "almafa", .match = TRUE },
    { .prepare = FALSE, .pattern = "almafa", .test_string = "barackfa", .match = FALSE },
    { .prepare = TRUE, .pattern = "foo", .test_string = "foo", .match = TRUE },
    { .prepare = TRUE, .pattern = "foo", .test_string = "bar", .match = FALSE }
  };

  return cr_make_param_array(StringMatcherParams, test_params, G_N_ELEMENTS(test_params));
}

ParameterizedTest(StringMatcherParams *test_params, str_matcher, test_literal)
{
  StringMatcher *literal_matcher = string_matcher_literal_new(test_params->pattern);

  if (test_params->prepare)
    cr_assert(string_matcher_prepare(literal_matcher, test_params->prepare_user_data));

  cr_assert(string_matcher_match(literal_matcher, test_params->test_string, strlen(test_params->test_string),
                                 test_params->match_user_data) == test_params->match);

  string_matcher_free(literal_matcher);
}

ParameterizedTestParameters(str_matcher, test_prefix)
{
  static StringMatcherParams test_params[] = {
    { .prepare = FALSE, .pattern = "almafa", .test_string = "almafa van az udvaron", .match = TRUE },
    { .prepare = FALSE, .pattern = "almafa", .test_string = "barackfa nincs az udvaron", .match = FALSE },
    { .prepare = FALSE, .pattern = "almafa", .test_string = "alma", .match = FALSE },
    { .prepare = TRUE, .pattern = "foo", .test_string = "foo bar", .match = TRUE },
    { .prepare = TRUE, .pattern = "foo", .test_string = "bar foo", .match = FALSE },
    { .prepare = TRUE, .pattern = "foo", .test_string = "fo", .match = FALSE }
  };

  return cr_make_param_array(StringMatcherParams, test_params, G_N_ELEMENTS(test_params));
}

ParameterizedTest(StringMatcherParams *test_params, str_matcher, test_prefix)
{
  StringMatcher *prefix_matcher = string_matcher_prefix_new(test_params->pattern);

  if (test_params->prepare)
    cr_assert(string_matcher_prepare(prefix_matcher, test_params->prepare_user_data));

  cr_assert(string_matcher_match(prefix_matcher, test_params->test_string, strlen(test_params->test_string),
                                 test_params->match_user_data) == test_params->match);

  string_matcher_free(prefix_matcher);
}

ParameterizedTestParameters(str_matcher, test_substring)
{
  static StringMatcherParams test_params[] = {
    { .prepare = FALSE, .pattern = "almafa", .test_string = "barackfa, almafa, szilvafa", .match = TRUE },
    { .prepare = FALSE, .pattern = "almafa", .test_string = "barack, alma, szilva", .match = FALSE },
    { .prepare = FALSE, .pattern = "almafa", .test_string = "alma", .match = FALSE },
    { .prepare = TRUE, .pattern = "bar", .test_string = "foo bar baz", .match = TRUE },
    { .prepare = TRUE, .pattern = "foo", .test_string = "fo ba ba", .match = FALSE },
    { .prepare = TRUE, .pattern = "foo", .test_string = "fo", .match = FALSE }
  };

  return cr_make_param_array(StringMatcherParams, test_params, G_N_ELEMENTS(test_params));
}

ParameterizedTest(StringMatcherParams *test_params, str_matcher, test_substring)
{
  StringMatcher *substring_matcher = string_matcher_substring_new(test_params->pattern);

  if (test_params->prepare)
    cr_assert(string_matcher_prepare(substring_matcher, test_params->prepare_user_data));

  cr_assert(string_matcher_match(substring_matcher, test_params->test_string, strlen(test_params->test_string),
                                 test_params->match_user_data) == test_params->match);

  string_matcher_free(substring_matcher);
}

ParameterizedTestParameters(str_matcher, test_glob)
{
  static StringMatcherParams test_params[] = {
    { .pattern = "al*fa", .test_string = "almafa", .match = TRUE },
    { .pattern = "al??fa", .test_string = "almafa", .match = TRUE },
    { .pattern = "alma*fa", .test_string = "almafa", .match = TRUE },
    { .pattern = "al*fa", .test_string = "alma", .match = FALSE },
    { .pattern = "almafa", .test_string = "al*fa", .match = FALSE }
  };

  return cr_make_param_array(StringMatcherParams, test_params, G_N_ELEMENTS(test_params));
}

ParameterizedTest(StringMatcherParams *test_params, str_matcher, test_glob)
{
  StringMatcher *glob_matcher = string_matcher_glob_new(test_params->pattern);

  cr_assert(string_matcher_prepare(glob_matcher, test_params->prepare_user_data));
  cr_assert(string_matcher_match(glob_matcher, test_params->test_string, strlen(test_params->test_string),
                                 test_params->match_user_data) == test_params->match);

  string_matcher_free(glob_matcher);
}

ParameterizedTestParameters(str_matcher, test_pcre)
{
  static StringMatcherParams test_params[] = {
    { .pattern = "al.*fa", .test_string = "almafa", .match = TRUE },
    { .pattern = "al.*fa", .test_string = "alma", .match = FALSE },
    { .pattern = "al.+fa", .test_string = "almafa", .match = TRUE },
    { .pattern = "al.+fa", .test_string = "alma", .match = FALSE },
    { .pattern = "alma.?fa", .test_string = "almafa", .match = TRUE },
    { .pattern = "alma.?fa", .test_string = "alma", .match = FALSE },
    { .pattern = "al..fa", .test_string = "almafa", .match = TRUE },
    { .pattern = "al..fa", .test_string = "almfa", .match = FALSE },
    { .pattern = "barackfa", .test_string = "almafa barackfa szilvafa", .match = TRUE },
    { .pattern = "^barackfa$", .test_string = "almafa barackfa szilvafa", .match = FALSE },
    { .pattern = "(foo)", .test_string = "foo", .match = TRUE },
    { .pattern = "(foo)", .test_string = "bar", .match = FALSE },
    { .pattern = "(foo|bar)", .test_string = "bar", .match = TRUE },
    { .pattern = "(foo|bar)", .test_string = "baz", .match = FALSE },
    { .pattern = "(?:foo|bar)", .test_string = "foo", .match = TRUE },
    { .pattern = "(?:foo|bar)", .test_string = "baz", .match = FALSE },
    { .pattern = "foo|bar", .test_string = "foo", .match = TRUE },
    { .pattern = "foo|bar", .test_string = "baz", .match = FALSE },
    { .pattern = "syslog-[a-z]+", .test_string = "syslog-ng", .match = TRUE },
    { .pattern = "syslog-[a-z]+", .test_string = "syslog-42", .match = FALSE },
    { .pattern = "syslog-[^a-z]+", .test_string = "syslog-42", .match = TRUE },
    { .pattern = "syslog-[^a-z]+", .test_string = "syslog-ng", .match = FALSE },
    { .pattern = "syslog-[a-z]{2,}", .test_string = "syslog-ng", .match = TRUE },
    { .pattern = "syslog-[a-z]{2,}", .test_string = "syslog-n", .match = FALSE },
    { .pattern = "\\w+\\s\\w+", .test_string = "almafa barackfa", .match = TRUE },
    { .pattern = "\\w+\\s\\w+", .test_string = "almafa", .match = FALSE },
    { .pattern = "\\d+\\s\\d+", .test_string = "123 456", .match = TRUE },
    { .pattern = "\\d+\\s\\d+", .test_string = "123456", .match = FALSE },
  };

  return cr_make_param_array(StringMatcherParams, test_params, G_N_ELEMENTS(test_params));
}

ParameterizedTest(StringMatcherParams *test_params, str_matcher, test_pcre)
{
  StringMatcher *pcre_matcher = string_matcher_pcre_new(test_params->pattern);

  cr_assert(string_matcher_prepare(pcre_matcher, test_params->prepare_user_data));
  cr_assert(string_matcher_match(pcre_matcher, test_params->test_string, strlen(test_params->test_string),
                                 test_params->match_user_data) == test_params->match);

  string_matcher_free(pcre_matcher);
}

TestSuite(str_matcher);