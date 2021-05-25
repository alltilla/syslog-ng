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

#include <stdio.h>

static int
_mqtt_send(MQTTDestinationWorker *self, char *msg)
{ 
  return mosquitto_publish(self->mosq, NULL, self->topic->str, strlen(msg), msg, 1, 0);
}

static LogThreadedResult
_dw_insert(LogThreadedDestWorker *s, LogMessage *msg)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;

  GString *string_to_write = g_string_new("");
  g_string_printf(string_to_write, "thread_id=%lu message=%s\n",
                  self->thread_id, log_msg_get_value(msg, LM_V_MESSAGE, NULL));

  int retval = _mqtt_send(self, string_to_write->str);

  if (retval != MOSQ_ERR_SUCCESS)
    {
      switch(retval)
        {
          case MOSQ_ERR_INVAL:
          case MOSQ_ERR_NOMEM:
          case MOSQ_ERR_NO_CONN:
          case MOSQ_ERR_PROTOCOL:
          case MOSQ_ERR_PAYLOAD_SIZE:
          case MOSQ_ERR_MALFORMED_UTF8:
          case MOSQ_ERR_QOS_NOT_SUPPORTED:
          case MOSQ_ERR_OVERSIZE_PACKET:
            {
              msg_error("Error while sending message");
              return LTR_ERROR;
              break;
            }
          
        }
    }

  g_string_free(string_to_write, TRUE);

  return LTR_SUCCESS;
  /*
   * LTR_DROP,
   * LTR_ERROR,
   * LTR_SUCCESS,
   * LTR_QUEUED,
   * LTR_NOT_CONNECTED,
   * LTR_RETRY,
  */
}

static gboolean
_connect(LogThreadedDestWorker *s)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;
  MQTTDestinationDriver *owner = (MQTTDestinationDriver *) s->owner;

  g_string_assign(self->topic, owner->topic->str);

  self->mosq = mosquitto_new(NULL, owner->clean_session, NULL);
  mosquitto_connect(self->mosq, owner->host->str, owner->port, owner->keepalive);
  mosquitto_subscribe(self->mosq, NULL, owner->topic->str, 1);
}

static void
_disconnect(LogThreadedDestWorker *s)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;

  mosquitto_destroy(self->mosq);
}

static gboolean
_thread_init(LogThreadedDestWorker *s)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;

  /*
    You can create thread specific resources here. In this example, we
    store the thread id.
  */
  self->thread_id = get_thread_id();

  return log_threaded_dest_worker_init_method(s);
}

static void
_thread_deinit(LogThreadedDestWorker *s)
{
  /*
    If you created resources during _thread_init,
    you need to free them here
  */

  log_threaded_dest_worker_deinit_method(s);
}

static void
_dw_free(LogThreadedDestWorker *s)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;
  /*
    If you created resources during new,
    you need to free them here.
  */
 g_string_free(self->topic, TRUE);

  mosquitto_lib_cleanup();
  log_threaded_dest_worker_free_method(s);
}


LogThreadedDestWorker *
mqtt_destination_dw_new(LogThreadedDestDriver *o, gint worker_index)
{
  MQTTDestinationWorker *self = g_new0(MQTTDestinationWorker, 1);
  self->topic = g_string_new("");

  mosquitto_lib_init();
  log_threaded_dest_worker_init_instance(&self->super, o, worker_index);
  self->super.thread_init = _thread_init;
  self->super.thread_deinit = _thread_deinit;
  self->super.insert = _dw_insert;
  self->super.free_fn = _dw_free;
  self->super.connect = _connect;
  self->super.disconnect = _disconnect;

  return &self->super;
}
