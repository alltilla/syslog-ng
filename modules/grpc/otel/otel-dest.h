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

#ifndef OTEL_DEST_H
#define OTEL_DEST_H

#include "syslog-ng.h"

#include "compat/cpp-start.h"

#include "driver.h"
#include "credentials/grpc-credentials-builder.h"

typedef struct OtelDestDriver_ OtelDestDriver;

LogDriver *otel_dd_new(GlobalConfig *cfg);
void otel_dd_set_url(LogDriver *s, const gchar *url);
void otel_dd_set_compression(LogDriver *s, gboolean enable);
void otel_dd_set_batch_bytes(LogDriver *s, glong b);
void otel_dd_add_int_channel_arg(LogDriver *s, const gchar *name, glong value);
void otel_dd_add_string_channel_arg(LogDriver *s, const gchar *name, const gchar *value);
GrpcClientCredentialsBuilderW *otel_dd_get_credentials_builder(LogDriver *s);

#include "compat/cpp-end.h"

#endif
