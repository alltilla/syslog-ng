/*
 * Copyright (c) 2024 Attila Szakacs
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

#include "exponential-backoff.h"
#include "messages.h"

struct ExponentialBackoff_
{
  gdouble initial_seconds;
  gdouble maximum_seconds;
  gdouble multiplier;

  gdouble next_wait_seconds;
};

gdouble
exponential_backoff_peek_next_wait_seconds(ExponentialBackoff *self)
{
  return self->next_wait_seconds;;
}

gdouble
exponential_backoff_get_next_wait_seconds(ExponentialBackoff *self)
{
  gdouble wait_seconds = self->next_wait_seconds;

  self->next_wait_seconds = MAX(MIN(wait_seconds * self->multiplier, self->maximum_seconds), self->initial_seconds);

  return wait_seconds;
}

void
exponential_backoff_reset(ExponentialBackoff *self)
{
  self->next_wait_seconds = 0;
}

gboolean
exponential_backoff_validate_options(gdouble initial_seconds, gdouble maximum_seconds, gdouble multiplier)
{
  if (initial_seconds < 0)
    {
      msg_error("Cannot initialize exponential backoff with negative initial seconds",
                evt_tag_int("initial_seconds", initial_seconds));
      return FALSE;
    }

  if (maximum_seconds < 0)
    {
      msg_error("Cannot initialize exponential backoff with negative maximum seconds",
                evt_tag_int("maximum_seconds", maximum_seconds));
      return FALSE;
    }

  if (initial_seconds > maximum_seconds)
    {
      msg_error("Cannot initialize exponential backoff with larger initial seconds than maximal seconds",
                evt_tag_int("initial_seconds", initial_seconds),
                evt_tag_int("maximum_seconds", maximum_seconds));
      return FALSE;
    }

  if (multiplier < 1)
    {
      msg_error("Cannot initialize exponential backoff with a multiplier smaller than 1",
                evt_tag_int("multiplier", multiplier));
      return FALSE;
    }

  return TRUE;
}

void
exponential_backoff_free(ExponentialBackoff *self)
{
  g_free(self);
}

ExponentialBackoff *
exponential_backoff_new(gdouble initial_seconds, gdouble maximum_seconds, gdouble multiplier)
{
  g_assert(exponential_backoff_validate_options(initial_seconds, maximum_seconds, multiplier));

  ExponentialBackoff *self = g_new0(ExponentialBackoff, 1);

  self->initial_seconds = initial_seconds;
  self->maximum_seconds = maximum_seconds;
  self->multiplier = multiplier;

  exponential_backoff_reset(self);

  return self;
}
