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

#ifndef EXPONENTIAL_BACKOFF_H
#define EXPONENTIAL_BACKOFF_H

#include "syslog-ng.h"

typedef struct ExponentialBackoff_ ExponentialBackoff;

ExponentialBackoff *exponential_backoff_new(gdouble initial_seconds, gdouble maximum_seconds, gdouble multiplier);
gboolean exponential_backoff_validate_options(gdouble initial_seconds, gdouble maximum_seconds, gdouble multiplier);
void exponential_backoff_free(ExponentialBackoff *self);

gdouble exponential_backoff_peek_next_wait_seconds(ExponentialBackoff *self);
gdouble exponential_backoff_get_next_wait_seconds(ExponentialBackoff *self);
void exponential_backoff_reset(ExponentialBackoff *self);

#endif
