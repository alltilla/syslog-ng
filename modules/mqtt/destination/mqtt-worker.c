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

static int
_mqtt_send(MQTTDestinationWorker *self, char *msg)
{
  int publish_result; // gint, nem kell kulon definialni
  int loop_result;    //            -||-
  publish_result = mosquitto_publish(self->mosq, NULL, self->topic->str, strlen(msg), msg, 1, 0);
  loop_result = mosquitto_loop(self->mosq, 1000, 1);
  msg_error("send", evt_tag_int("loop_result", loop_result));
  
  return publish_result;
}

static LogThreadedResult
_dw_insert(LogThreadedDestWorker *s, LogMessage *msg)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;

  GString *string_to_write = g_string_new(""); // koltseges muvelet, erdmes inkabb 1 GStringet tarolni a workerben, es azt ujrahasznalni minden insert-ben
  g_string_printf(string_to_write, "thread_id=%lu message=%s\n",
                  self->thread_id, log_msg_get_value(msg, LM_V_MESSAGE, NULL)); // configban template() opcio + log_template_format(), de errol inkabb szemelyesen beszeljunk

  int retval = _mqtt_send(self, string_to_write->str);
  msg_error("insert", evt_tag_int("retval", retval));
  if (retval != MOSQ_ERR_SUCCESS)
    {
      switch(retval) // a mapolast alaposabban at kellene nezni, allitsuk be jol a threaded dest-et!
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

static void
_set_mosquitto_callback(struct mosquitto *mosq) // megnezzuk, hogy ezek kellenek-e
{
  mosquitto_connect_callback_set(mosq, mqtt_connect_callback);
  mosquitto_disconnect_callback_set(mosq, mqtt_disconnect_callback);
  mosquitto_message_callback_set(mosq, mqtt_message_callback);
  mosquitto_subscribe_callback_set(mosq, mqtt_subscribe_callback);
  mosquitto_unsubscribe_callback_set(mosq, mqtt_unsubscribe_callback);
  mosquitto_log_callback_set(mosq, mqtt_log_callback);
}

static gboolean
_connect(LogThreadedDestWorker *s)
{
  int loop; // felesleges valtozo
  int isConnected; // nyugodtan lehet lejjebb definialni, hasznalj gint-et, hasznalj snake_case-t

  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;
  MQTTDestinationDriver *owner = (MQTTDestinationDriver *) s->owner;


  isConnected = mosquitto_connect(self->mosq, owner->host->str, owner->port, owner->keepalive);

  if (isConnected)
    {
      msg_error("Could not connect mosquitto", evt_tag_error("error")); // + evt_tag_str("driver", owner->super.super.super.id)
      // csak akkor hasznalunk evt_tag_error-t, ha az errno be van setelve, nem az isConnected erteket kellene kiiratni?
      return FALSE;
    }

  // loop = mosquitto_loop_start(self->mosq);
  // if (loop != MOSQ_ERR_SUCCESS)
  //   {
  //     msg_error("Unable to start loop", evt_tag_error("error"), evt_tag_int("loop ", loop));
  //     return FALSE;
  //   }
  msg_error("connect");
  return TRUE;
}

static void
_disconnect(LogThreadedDestWorker *s)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;
  mosquitto_disconnect(self->mosq);
  msg_error("disconnect");
}

static gboolean
_thread_init(LogThreadedDestWorker *s)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;
  MQTTDestinationDriver *owner = (MQTTDestinationDriver *) s->owner;

  msg_error("thread init");
  /*
    You can create thread specific resources here. In this example, we
    store the thread id.
  */
  self->thread_id = get_thread_id(); // erre nincs szukseg


  g_string_assign(self->topic, owner->topic->str);

  self->mosq = mosquitto_new(NULL, owner->clean_session, NULL);

  if(self->mosq == NULL)
    {
      msg_error("Could not create mosquitto", evt_tag_error("error"));
      return FALSE;
    }

  _set_mosquitto_callback(self->mosq);

  mosquitto_threaded_set(self->mosq, true); // ezt megnézzni


  return log_threaded_dest_worker_init_method(s);
}

static void
_thread_deinit(LogThreadedDestWorker *s)
{
  MQTTDestinationWorker *self = (MQTTDestinationWorker *)s;
  /*
    If you created resources during _thread_init,
    you need to free them here
  */

  mosquitto_destroy(self->mosq);
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

  log_threaded_dest_worker_free_method(s);
}

static void
mqtt_global_init(void)
{
  mosquitto_lib_init();
  msg_error("init lefut");
}

static void
mqtt_global_deinit(void)
{
  mosquitto_lib_cleanup();
}

static void
mqtt_global_initializers(void) 
{
  static gboolean initialized = FALSE;

  if (!initialized)
    {
      register_application_hook(AH_STARTUP, (ApplicationHookFunc) mqtt_global_init, NULL, AHM_RUN_ONCE);
      register_application_hook(AH_SHUTDOWN, (ApplicationHookFunc) mqtt_global_deinit, NULL, AHM_RUN_ONCE);
      initialized = TRUE;
    }
}


LogThreadedDestWorker *
mqtt_destination_dw_new(LogThreadedDestDriver *o, gint worker_index)
{
  MQTTDestinationWorker *self = g_new0(MQTTDestinationWorker, 1);
  self->topic = g_string_new(""); // hasznalhato az owner-e
  msg_error("new");
  mqtt_global_initializers();

  log_threaded_dest_worker_init_instance(&self->super, o, worker_index);
  self->super.thread_init = _thread_init;
  self->super.thread_deinit = _thread_deinit;
  self->super.insert = _dw_insert;
  self->super.free_fn = _dw_free;
  self->super.connect = _connect;
  self->super.disconnect = _disconnect;

  return &self->super;
}
