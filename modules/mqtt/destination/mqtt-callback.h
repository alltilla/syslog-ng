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

#ifndef MQTT_DESTINATION_CALLBACK_H_INCLUDED
#define MQTT_DESTINATION_CALLBACK_H_INCLUDED

#include <mosquitto.h>

void mqtt_connect_callback(struct mosquitto *mosq, void *obj, int rc);
void mqtt_disconnect_callback(struct mosquitto *mosq, void *obj, int rc);
void mqtt_publish_callback(struct mosquitto *mosq, void *obj, int mid);
void mqtt_message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message * message);
void mqtt_subscribe_callback(struct mosquitto *mosq, void *obj, int mid, int qos_count, const int* grabted_qos);
void mqtt_unsubscribe_callback(struct mosquitto *mosq, void *obj, int mid);
void mqtt_log_callback(struct mosquitto *mosq, void *obj, int level, const char *str);


#endif /* MQTT_DESTINATION_CALLBACK_H_INCLUDED */