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

#ifndef MQTT_DESTINATION_H_INCLUDED
#define MQTT_DESTINATION_H_INCLUDED

#include "driver.h"
#include "logthrdest/logthrdestdrv.h"
#include <mosquitto.h>

typedef struct
{
  LogThreadedDestDriver super;
  GString * host;
  gint      port;
  GString * topic;
  gboolean  clean_session;
  gint      keepalive;
} MQTTDestinationDriver;

LogDriver *mqtt_destination_dd_new(GlobalConfig *cfg);

void mqtt_destination_dd_set_host (LogDriver *d, const gchar *host);
void mqtt_destination_dd_set_port (LogDriver *d, const glong  port);
void mqtt_destination_dd_set_topic(LogDriver *d, const gchar *topic);
void mqtt_destination_dd_set_clean_session (LogDriver *d, const gboolean clean_session);
void mqtt_destination_dd_set_keepalive (LogDriver *d, const glong keepalive);


#endif /* MQTT_DESTINATION_H_INCLUDED */