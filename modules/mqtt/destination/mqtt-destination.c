/*
 * Copyright (c) 2020 Balabit
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

#include "mqtt-destination.h"
#include "mqtt-worker.h"
#include "mqtt-parser.h"

#include "plugin.h"
#include "messages.h"
#include "misc.h"
#include "stats/stats-registry.h"
#include "logqueue.h"
#include "driver.h"
#include "plugin-types.h"
#include "logthrdest/logthrdestdrv.h"

/*
 * Configuration
 */

void
mqtt_destination_dd_set_host (LogDriver *d, const gchar *host)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;
  g_string_assign(self->host, host);
}

void
mqtt_destination_dd_set_port (LogDriver *d, const glong port)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;
  self->port = (gint)port;
}

void
mqtt_destination_dd_set_topic(LogDriver *d, const gchar *topic)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;
  g_string_assign(self->topic, topic);
}

void
mqtt_destination_dd_set_clean_session (LogDriver *d, const gboolean clean_session)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;
  self->clean_session = clean_session;
}

void
mqtt_destination_dd_set_keepalive (LogDriver *d, const glong keepalive)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;
  self->keepalive = (gint)keepalive;
}

/*
 * Utilities
 */
static const gchar *
_format_stats_instance(LogThreadedDestDriver *d)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;
  static gchar persist_name[1024];

  g_snprintf(persist_name, sizeof(persist_name),
             "mqtt-destination,%s.%d.%s", self->host->str, self->port, self->topic->str);
  return persist_name;
}

static const gchar *
_format_persist_name(const LogPipe *d)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;
  static gchar persist_name[1024];

  if (d->persist_name)
    g_snprintf(persist_name, sizeof(persist_name), "mqtt-destination.%s", d->persist_name);
  else
    g_snprintf(persist_name, sizeof(persist_name), "mqtt-destination.%s.%d.%s", self->host->str, self->port, self->topic->str);

  return persist_name;
}


static gboolean
_dd_init(LogPipe *d)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;

  if (!log_threaded_dest_driver_init_method(d))
    return FALSE;

  return TRUE;
}

gboolean
_dd_deinit(LogPipe *s)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)s;

  return log_threaded_dest_driver_deinit_method(s);
}

static void
_dd_free(LogPipe *d)
{
  MQTTDestinationDriver *self = (MQTTDestinationDriver *)d;

  g_string_free(self->host, TRUE);
  g_string_free(self->topic, TRUE);

  log_threaded_dest_driver_free(d);
}

LogDriver *
mqtt_destination_dd_new(GlobalConfig *cfg)
{
  MQTTDestinationDriver *self = g_new0(MQTTDestinationDriver, 1);
  self->host = g_string_new("");
  self->topic = g_string_new("");

  log_threaded_dest_driver_init_instance(&self->super, cfg);
  self->super.super.super.super.init = _dd_init;
  self->super.super.super.super.deinit = _dd_deinit;
  self->super.super.super.super.free_fn = _dd_free;

  self->super.format_stats_instance = _format_stats_instance;
  self->super.super.super.super.generate_persist_name = _format_persist_name;
  self->super.stats_source = stats_register_type("mqtt-destination");
  self->super.worker.construct = mqtt_destination_dw_new;

  return (LogDriver *)self;
}
