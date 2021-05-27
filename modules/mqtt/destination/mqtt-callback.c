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


#include "mqtt-worker.h"
#include "mqtt-destination.h"
#include "thread-utils.h"
#include "apphook.h"
#include "mqtt-callback.h"

#include <stdio.h>

void 
mqtt_connect_callback(struct mosquitto *mosq, void *obj, int rc)
{
    // TODO
    msg_error("connect callback");
}

void 
mqtt_disconnect_callback(struct mosquitto *mosq, void *obj, int rc)
{
    // TODO
    msg_error("disconnect callback");
}

void 
mqtt_publish_callback(struct mosquitto *mosq, void *obj, int mid)
{
    // TODO
    msg_error("publish callback");
}

void 
mqtt_message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message * message)
{
    // TODO
    msg_error("message callback");
}

void 
mqtt_subscribe_callback(struct mosquitto *mosq, void *obj, int mid, int qos_count, const int* grabted_qos)
{
    // TODO
    msg_error("subscribe callback");
}

void 
mqtt_unsubscribe_callback(struct mosquitto *mosq, void *obj, int mid)
{
    // TODO
    msg_error("unscribe callback");
}

void 
mqtt_log_callback(struct mosquitto *mosq, void *obj, int level, const char *str)
{
    // TODO
    msg_error("log callback", evt_tag_int("level", level), evt_tag_str("str", str));
}

