/*
 * Copyright (c) 2016 Balabit
 * Copyright (c) 2016 Balázs Scheidler
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

#include "scanner/list-scanner/list-scanner.h"
#include "str-repr/encode.h"
#include "compat/pcre.h"
#include "str-matcher.h"

static void
_append_comma_between_list_elements_if_needed(GString *result, gsize initial_len)
{
  /* we won't insert a comma at the very first position we were invoked at */
  if (result->len == initial_len)
    return;

  if (result->str[result->len - 1] != ',')
    g_string_append_c(result, ',');
}

static void
tf_list_concat(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  ListScanner scanner;
  gsize initial_len = result->len;

  list_scanner_init(&scanner);
  list_scanner_input_gstring_array(&scanner, argc, argv);
  while (list_scanner_scan_next(&scanner))
    {
      _append_comma_between_list_elements_if_needed(result, initial_len);
      str_repr_encode_append(result, list_scanner_get_current_value(&scanner), -1, ",");
    }
  list_scanner_deinit(&scanner);
}

TEMPLATE_FUNCTION_SIMPLE(tf_list_concat);

static void
tf_list_append(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  gsize initial_len = result->len;

  if (argc == 0)
    return;
  g_string_append_len(result, argv[0]->str, argv[0]->len);
  for (gint i = 1; i < argc; i++)
    {
      _append_comma_between_list_elements_if_needed(result, initial_len);
      str_repr_encode_append(result, argv[i]->str, argv[i]->len, ",");
    }
}

TEMPLATE_FUNCTION_SIMPLE(tf_list_append);

static gint
_list_count(gint argc, GString *argv[])
{
  ListScanner scanner;
  gint count = 0;

  if (argc != 0)
    {
      list_scanner_init(&scanner);
      list_scanner_input_gstring_array(&scanner, argc, argv);

      while (list_scanner_scan_next(&scanner))
        count++;

      list_scanner_deinit(&scanner);
    }
  return count;
}

static void
_translate_negative_list_slice_indices(gint argc, GString *argv[],
                                       gint *first_ndx, gint *last_ndx)
{
  gint count = -1;

  if (*first_ndx < 0 || *last_ndx < 0)
    count = _list_count(argc, argv);

  if (*first_ndx < 0)
    *first_ndx += count;
  if (*last_ndx < 0)
    *last_ndx += count;

}

static void
_list_slice(gint argc, GString *argv[], GString *result,
            gint first_ndx, gint last_ndx)
{
  ListScanner scanner;
  gsize initial_len = result->len;
  gint i;

  if (argc == 0)
    return;

  _translate_negative_list_slice_indices(argc, argv, &first_ndx, &last_ndx);

  /* NOTE: first_ndx and last_ndx may be negative, so these loops must cover
   * that case, by interpreting negative first_ndx as "0", and negative
   * last_ndx as "0".
   *
   * $(list-slice -100: a,b,c) - should return "a,b,c"
   * $(list-slice :-100 a,b,c) - should return ""
   */

  list_scanner_init(&scanner);
  list_scanner_input_gstring_array(&scanner, argc, argv);

  i = 0;
  while (i < first_ndx && list_scanner_scan_next(&scanner))
    i++;

  while (i >= first_ndx &&
         i < last_ndx &&
         list_scanner_scan_next(&scanner))
    {
      _append_comma_between_list_elements_if_needed(result, initial_len);
      str_repr_encode_append(result, list_scanner_get_current_value(&scanner), -1, ",");
      i++;
    }
  list_scanner_deinit(&scanner);
}

static void
_translate_negative_list_index(gint argc, GString *argv[],
                               gint *ndx)
{
  if (*ndx < 0)
    *ndx += _list_count(argc, argv);
}

static void
_list_nth(gint argc, GString *argv[], GString *result, gint ndx)
{
  ListScanner scanner;
  gint i;

  if (argc == 0)
    return;

  list_scanner_init(&scanner);
  list_scanner_input_gstring_array(&scanner, argc, argv);

  _translate_negative_list_index(argc, argv, &ndx);

  i = 0;
  while (i < ndx && list_scanner_scan_next(&scanner))
    i++;

  if (i == ndx && list_scanner_scan_next(&scanner))
    {
      g_string_append(result, list_scanner_get_current_value(&scanner));
    }
  list_scanner_deinit(&scanner);
}

/*
 * Take off the first item of the list, unencoded.
 */
static void
tf_list_head(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  _list_nth(argc, argv, result, 0);
}

TEMPLATE_FUNCTION_SIMPLE(tf_list_head);

static void
tf_list_nth(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  gint64 ndx = 0;
  const gchar *ndx_spec;

  if (argc < 1)
    return;

  ndx_spec = argv[0]->str;
  /* get start position from first argument */
  if (!parse_dec_number(ndx_spec, &ndx))
    {
      msg_error("$(list-nth) parsing failed, index must be the first argument",
                evt_tag_str("ndx", ndx_spec));
      return;
    }

  _list_nth(argc - 1, &argv[1], result, ndx);
}

TEMPLATE_FUNCTION_SIMPLE(tf_list_nth);

static void
tf_list_tail(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  if (argc == 0)
    return;

  _list_slice(argc, argv, result, 1, INT_MAX);
}

TEMPLATE_FUNCTION_SIMPLE(tf_list_tail);

static void
tf_list_count(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  gint count = _list_count(argc, argv);
  format_uint32_padded(result, -1, ' ', 10, count);
}

TEMPLATE_FUNCTION_SIMPLE(tf_list_count);

/* $(list-slice FIRST:LAST list ...) */
static void
tf_list_slice(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  gint64 first_ndx = 0, last_ndx = INT_MAX;
  const gchar *slice_spec, *first_spec, *last_spec;
  gchar *colon;

  if (argc < 1)
    return;

  slice_spec = argv[0]->str;
  first_spec = slice_spec;
  colon = strchr(first_spec, ':');
  if (colon)
    {
      last_spec = colon + 1;
      *colon = 0;
    }
  else
    last_spec = NULL;

  /* get start position from first argument */
  if (first_spec && first_spec[0] &&
      !parse_dec_number(first_spec, &first_ndx))
    {
      msg_error("$(list-slice) parsing failed, first could not be parsed",
                evt_tag_str("start", first_spec));
      return;
    }

  /* get last position from second argument */
  if (last_spec && last_spec[0] &&
      !parse_dec_number(last_spec, &last_ndx))
    {
      msg_error("$(list-slice) parsing failed, last could not be parsed",
                evt_tag_str("last", last_spec));
      return;
    }
  _list_slice(argc - 1, &argv[1], result,
              (gint) first_ndx, (gint) last_ndx);
}

TEMPLATE_FUNCTION_SIMPLE(tf_list_slice);

static void
tf_explode(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  gsize initial_len = result->len;
  GString *separator;

  if (argc < 1)
    return;

  separator = argv[0];

  for (gint i = 1; i < argc; i++)
    {
      gchar **strv = g_strsplit(argv[i]->str, separator->str, -1);

      for (gchar **str = &strv[0]; *str != NULL; str++)
        {
          _append_comma_between_list_elements_if_needed(result, initial_len);
          str_repr_encode_append(result, *str, -1, ",");
        }
      g_strfreev(strv);
    }
}

TEMPLATE_FUNCTION_SIMPLE(tf_explode);

static void
tf_implode(LogMessage *msg, gint argc, GString *argv[], GString *result)
{
  ListScanner scanner;
  gsize initial_len = result->len;
  GString *separator;

  if (argc < 1)
    return;

  separator = argv[0];

  list_scanner_init(&scanner);
  list_scanner_input_gstring_array(&scanner, argc - 1, &argv[1]);
  while (list_scanner_scan_next(&scanner))
    {
      if (result->len > initial_len)
        g_string_append_len(result, separator->str, separator->len);
      g_string_append_len(result,
                          list_scanner_get_current_value(&scanner),
                          list_scanner_get_current_value_len(&scanner));
    }
  list_scanner_deinit(&scanner);
}

TEMPLATE_FUNCTION_SIMPLE(tf_implode);

typedef struct _ListSearchState
{
  TFSimpleFuncState super;
  StringMatcher *matcher;
  gchar *mode;
  gint start_index;
} ListSearchState;

static void
list_search_state_free(gpointer s)
{
  ListSearchState *self = (ListSearchState *)s;

  string_matcher_free(self->matcher);
  g_free(self->mode);
  tf_simple_func_free_state(&self->super);
}

static gboolean
_list_search_parse_options(gchar **mode, gint *start_index, gint *argc, gchar **argv[], GError **error)
{
  gboolean result = TRUE;
  GOptionContext *ctx;
  GOptionEntry list_search_options[] =
  {
    { "mode", 0, 0, G_OPTION_ARG_STRING, mode, NULL, NULL },
    { "start-index", 0, 0, G_OPTION_ARG_INT, start_index, NULL, NULL },
    { NULL }
  };

  ctx = g_option_context_new((*argv)[0]);
  g_option_context_add_main_entries(ctx, list_search_options, NULL);
  result = g_option_context_parse(ctx, argc, argv, error);

  g_option_context_free(ctx);
  return result;
}

static gboolean
_list_search_init_matcher(ListSearchState *state, gint argc, gchar *argv[], GError **error)
{
  if (argc < 2)
    {
      g_set_error(error, LOG_TEMPLATE_ERROR, LOG_TEMPLATE_ERROR_COMPILE,
                  "$(list-search) Pattern is missing. Usage: $(list-search [options] <pattern> ${list})");
      return FALSE;
    }
  else if (argc < 3)
    {
      g_set_error(error, LOG_TEMPLATE_ERROR, LOG_TEMPLATE_ERROR_COMPILE,
                  "$(list-search) List is missing. Usage: $(list-search [options] <pattern> ${list}");
      return FALSE;
    }

  gboolean result = FALSE;
  gchar *pattern = argv[1];

  if (state->mode == NULL || strcmp(state->mode, "literal") == 0)
    {
      state->matcher = string_matcher_literal_new(pattern);
      result = string_matcher_prepare(state->matcher, GINT_TO_POINTER(FALSE));
    }
  else if (strcmp(state->mode, "prefix") == 0)
    {
      state->matcher = string_matcher_prefix_new(pattern);
      result = string_matcher_prepare(state->matcher, GINT_TO_POINTER(FALSE));
    }
  else if (strcmp(state->mode, "substring") == 0)
    {
      state->matcher = string_matcher_substring_new(pattern);
      result = string_matcher_prepare(state->matcher, GINT_TO_POINTER(FALSE));
    }
  else if (strcmp(state->mode, "glob") == 0)
    {
      state->matcher = string_matcher_glob_new(pattern);
      result = string_matcher_prepare(state->matcher, NULL);
    }
  else if (strcmp(state->mode, "pcre") == 0)
    {
      StringMatcherPcrePrepareParams params;
      string_matcher_pcre_prepare_params_defaults(&params);
      params.compile_flags |= PCRE_ANCHORED;

      state->matcher = string_matcher_pcre_new(pattern);
      result = string_matcher_prepare(state->matcher, &params);
    }
  else
    {
      g_set_error(error, LOG_TEMPLATE_ERROR, LOG_TEMPLATE_ERROR_COMPILE,
                  "$(list-search) Invalid list-search mode: %s. "
                  "Valid modes are: literal, prefix, substring, glob, pcre", state->mode);
      return FALSE;
    }

  if (!result)
    {
      g_set_error(error, LOG_TEMPLATE_ERROR, LOG_TEMPLATE_ERROR_COMPILE,
                  "$(list-search) Failed to prepare pattern: %s", pattern);
      string_matcher_free(state->matcher);
    }

  return result;
}

static gboolean
tf_list_search_prepare(LogTemplateFunction *self, gpointer s, LogTemplate *parent, gint argc, gchar *argv[],
                       GError **error)
{
  ListSearchState *state = (ListSearchState *)s;

  if (!_list_search_parse_options(&state->mode, &state->start_index, &argc, &argv, error))
    return FALSE;

  if (!_list_search_init_matcher(state, argc, argv, error))
    return FALSE;

  if (!tf_simple_func_prepare(self, state, parent, argc, argv, error))
    return FALSE;

  return TRUE;
}

static void
tf_list_search_call(LogTemplateFunction *self, gpointer s, const LogTemplateInvokeArgs *args, GString *result)
{
  ListSearchState *state = (ListSearchState *)s;
  ListScanner scanner;
  gint index = state->start_index;

  list_scanner_init(&scanner);
  list_scanner_input_gstring_array(&scanner, state->super.argc - 1, &args->argv[1]);
  list_scanner_skip_n(&scanner, index);

  while (list_scanner_scan_next(&scanner))
    {
      if (string_matcher_match(state->matcher,
                               list_scanner_get_current_value(&scanner),
                               list_scanner_get_current_value_len(&scanner),
                               NULL))
        {
          format_int32_padded(result, -1, ' ', 10, index);
          break;
        }
      index++;
    }
  list_scanner_deinit(&scanner);
}

TEMPLATE_FUNCTION(ListSearchState, tf_list_search, tf_list_search_prepare, tf_simple_func_eval,
                  tf_list_search_call, list_search_state_free, NULL);
