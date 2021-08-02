/*
 * Copyright (c) 2002-2016 Balabit
 * Copyright (c) 2016 Viktor Juhasz <viktor.juhasz@balabit.com>
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

#include "logqueue-disk-non-reliable.h"
#include "logpipe.h"
#include "messages.h"
#include "syslog-ng.h"
#include "scratch-buffers.h"

#define ITEM_NUMBER_PER_MESSAGE 2

typedef struct
{
  guint index_in_queue;
  guint item_number_per_message;
  LogQueue *queue;
} DiskqMemusageLoaderState;

static gboolean
_object_is_message_in_position(guint index_in_queue, guint item_number_per_message)
{
  return !(index_in_queue % item_number_per_message);
}

static void
_update_memory_usage_during_load(gpointer data, gpointer s)
{
  DiskqMemusageLoaderState *state = (DiskqMemusageLoaderState *)s;

  if (_object_is_message_in_position(state->index_in_queue, state->item_number_per_message))
    {
      LogMessage *msg = (LogMessage *)data;
      log_queue_memory_usage_add(state->queue, log_msg_get_size(msg));
    }
  state->index_in_queue++;
}

static gboolean
_start(LogQueueDisk *s, const gchar *filename)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;

  gboolean retval = qdisk_start(s->qdisk, filename, self->qout, self->qbacklog, self->qoverflow);

  DiskqMemusageLoaderState qout_sum = { .index_in_queue = 0,
                                        .item_number_per_message = ITEM_NUMBER_PER_MESSAGE,
                                        .queue = &self->super.super
                                      };

  DiskqMemusageLoaderState overflow_sum = { .index_in_queue = 0,
                                            .item_number_per_message = ITEM_NUMBER_PER_MESSAGE,
                                            .queue = &self->super.super
                                          };

  g_queue_foreach(self->qout, _update_memory_usage_during_load, &qout_sum);
  g_queue_foreach(self->qoverflow, _update_memory_usage_during_load, &overflow_sum);

  return retval;
}

static inline guint
_get_message_number_in_queue(GQueue *queue)
{
  return queue->length / ITEM_NUMBER_PER_MESSAGE;
}

#define HAS_SPACE_IN_QUEUE(queue) (_get_message_number_in_queue(queue) < queue ## _size)

static inline gboolean
_has_messages_on_disk(LogQueueDiskNonReliable *self)
{
  return qdisk_get_length(self->super.qdisk) > 0;
}

static inline gboolean
_has_messages_in_queue(GQueue *queue)
{
  return queue->length > 0;
}

static gint64
_get_length (LogQueueDisk *s)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;
  return _get_message_number_in_queue(self->qout)
         + qdisk_get_length (s->qdisk)
         + _get_message_number_in_queue(self->qoverflow);
}

static inline gboolean
_pop_from_memory_queue_head(LogQueueDiskNonReliable *self, GQueue *queue, LogMessage **msg,
                            LogPathOptions *path_options)
{
  if (queue->length == 0)
    return FALSE;

  *msg = g_queue_pop_head(queue);
  POINTER_TO_LOG_PATH_OPTIONS(g_queue_pop_head(queue), path_options);
  log_queue_memory_usage_sub(&self->super.super, log_msg_get_size(*msg));

  return TRUE;
}

static LogMessage *
_get_next_message(LogQueueDiskNonReliable *self, LogPathOptions *path_options)
{
  LogMessage *result = NULL;
  path_options->ack_needed = TRUE;
  if (_has_messages_on_disk(self))
    {
      result = log_queue_disk_read_message(&self->super, path_options);
      if(result)
        {
          log_queue_memory_usage_add(&self->super.super, log_msg_get_size(result));
          path_options->ack_needed = FALSE;
        }
    }
  else if (_has_messages_in_queue(self->qoverflow))
    {
      result = g_queue_pop_head (self->qoverflow);
      POINTER_TO_LOG_PATH_OPTIONS (g_queue_pop_head (self->qoverflow), path_options);
    }
  return result;
}

static inline gboolean
_could_move_into_qout(LogQueueDiskNonReliable *self)
{
  /* NOTE: we only load half the qout queue at a time */
  return (_get_message_number_in_queue(self->qout) < (self->qout_size / 2));
}

static void
_add_message_to_qout(LogQueueDiskNonReliable *self, LogMessage *msg, LogPathOptions *path_options)
{
  /* NOTE: we always generate flow-control disabled entries into
   * qout, they only get there via backlog rewind */

  g_queue_push_tail (self->qout, msg);
  g_queue_push_tail (self->qout, LOG_PATH_OPTIONS_FOR_BACKLOG);
  log_msg_ack (msg, path_options, AT_PROCESSED);
}

static inline gboolean
_has_movable_message(LogQueueDiskNonReliable *self)
{
  return _has_messages_in_queue(self->qoverflow)
         && ((HAS_SPACE_IN_QUEUE(self->qout) && !_has_messages_on_disk(self))
             || qdisk_is_space_avail (self->super.qdisk, 4096));
}

static void
_move_messages_from_overflow(LogQueueDiskNonReliable *self)
{
  LogMessage *msg;
  LogPathOptions path_options;
  /* move away as much entries from the overflow area as possible */
  while (_has_movable_message(self))
    {
      msg = g_queue_pop_head (self->qoverflow);
      POINTER_TO_LOG_PATH_OPTIONS (g_queue_pop_head (self->qoverflow), &path_options);

      if (!_has_messages_on_disk(self) && HAS_SPACE_IN_QUEUE(self->qout))
        {
          /* we can skip qdisk, go straight to qout */
          g_queue_push_tail (self->qout, msg);
          g_queue_push_tail (self->qout, LOG_PATH_OPTIONS_FOR_BACKLOG);
          log_msg_ref (msg);
        }
      else
        {
          ScratchBuffersMarker marker;
          GString *serialized = scratch_buffers_alloc_and_mark(&marker);

          /*
           * We are running in the destination thread, and doing multiple expensive
           * serializations while holding the lock.
           *
           * Releasing the lock would make the source threads be able to push more
           * messages to the disk-buffer, but we would still be occupied with serializing
           * instead of processing messages in the disk-buffer, so it would not
           * give us any performance gain.
           *
           * We should not do such expensive operations in the destination thread.
           * We better fix this.
           */
          if (!qdisk_serialize_msg(self->super.qdisk, msg, serialized))
            {
              scratch_buffers_reclaim_marked(marker);
              break;
            }

          if (log_queue_disk_write_message(&self->super, serialized))
            {
              log_queue_memory_usage_sub(&self->super.super, log_msg_get_size(msg));
            }
          else
            {
              /* oops, although there seemed to be some free space available,
               * we failed saving this message, (it might have needed more
               * than 4096 bytes than we ensured), push back and break
               */
              g_queue_push_head (self->qoverflow, LOG_PATH_OPTIONS_TO_POINTER (&path_options));
              g_queue_push_head (self->qoverflow, msg);
              log_msg_ref (msg);
              break;
            }
          scratch_buffers_reclaim_marked(marker);
        }
      log_msg_ack (msg, &path_options, AT_PROCESSED);
      log_msg_unref (msg);
    }
}

static void
_move_disk (LogQueueDiskNonReliable *self)
{
  LogMessage *msg;
  LogPathOptions path_options = LOG_PATH_OPTIONS_INIT;

  if (qdisk_is_read_only (self->super.qdisk))
    return;

  /* stupid message mover between queues */

  if (!_has_messages_in_queue(self->qout) && self->qout_size > 0)
    {
      do
        {
          msg = _get_next_message(self, &path_options);

          if (msg)
            {
              _add_message_to_qout(self, msg, &path_options);
            }
        }
      while (msg && _could_move_into_qout(self));
    }
  // _move_messages_from_overflow(self);
}

static void
_ack_backlog (LogQueueDisk *s, guint num_msg_to_ack)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;
  LogMessage *msg;
  LogPathOptions path_options = LOG_PATH_OPTIONS_INIT;
  guint i;

  for (i = 0; i < num_msg_to_ack; i++)
    {
      if (!_has_messages_in_queue(self->qbacklog))
        return;
      msg = g_queue_pop_head (self->qbacklog);
      POINTER_TO_LOG_PATH_OPTIONS (g_queue_pop_head (self->qbacklog), &path_options);
      log_msg_unref (msg);
      log_msg_ack (msg, &path_options, AT_PROCESSED);
    }
}

static void
_rewind_backlog (LogQueueDisk *s, guint rewind_count)
{
  guint i;
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;
  rewind_count = MIN(rewind_count, _get_message_number_in_queue(self->qbacklog));

  for (i = 0; i < rewind_count; i++)
    {
      gpointer ptr_opt = g_queue_pop_tail (self->qbacklog);
      gpointer ptr_msg = g_queue_pop_tail (self->qbacklog);

      g_queue_push_head (self->qout, ptr_opt);
      g_queue_push_head (self->qout, ptr_msg);

      log_queue_queued_messages_inc(&self->super.super);
      log_queue_memory_usage_add(&self->super.super, log_msg_get_size((LogMessage *)ptr_msg));
    }
}

static inline void
_push_to_qbacklog_if_needed(LogQueueDiskNonReliable *self, LogMessage *msg, LogPathOptions *path_options)
{
  if (!self->super.super.use_backlog)
    return;

  log_msg_ref(msg);
  g_queue_push_tail(self->qbacklog, msg);
  g_queue_push_tail(self->qbacklog, LOG_PATH_OPTIONS_TO_POINTER(path_options));
}

static LogMessage *
_pop_head (LogQueueDisk *s, LogPathOptions *path_options)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;
  LogMessage *msg = NULL;

  if (_pop_from_memory_queue_head(self, self->qout, &msg, path_options))
    goto success;

  msg = log_queue_disk_read_message(s, path_options);
  if (msg)
    {
      path_options->ack_needed = FALSE;
      goto success;
    }

  if (_pop_from_memory_queue_head(self, self->qoverflow, &msg, path_options))
    goto success;

  return NULL;

success:
  _push_to_qbacklog_if_needed(self, msg, path_options);
  _move_disk(self);
  return msg;
}

static void
_push_head (LogQueueDisk *s, LogMessage *msg, const LogPathOptions *path_options)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;

  g_queue_push_head (self->qout, LOG_PATH_OPTIONS_TO_POINTER (path_options));
  g_queue_push_head (self->qout, msg);
  log_queue_queued_messages_inc(&self->super.super);
  log_queue_memory_usage_add(&self->super.super, log_msg_get_size(msg));
}

static inline void
_report_message_drop(LogQueueDiskNonReliable *self)
{
  msg_debug("Destination queue full, dropping message",
            evt_tag_str  ("filename", qdisk_get_filename (self->super.qdisk)),
            evt_tag_long ("queue_len", _get_length(&self->super)),
            evt_tag_int  ("mem_buf_length", self->qoverflow_size),
            evt_tag_long ("disk_buf_size", qdisk_get_maximum_size (self->super.qdisk)),
            evt_tag_str  ("persist_name", self->super.super.persist_name));
}

static inline void
_push_to_memory_queue_tail(LogQueueDiskNonReliable *self, GQueue *queue, LogMessage *msg,
                           const LogPathOptions *path_options)
{
  g_queue_push_tail(queue, msg);
  g_queue_push_tail(queue, LOG_PATH_OPTIONS_TO_POINTER(path_options));

  log_msg_ref(msg);

  log_queue_memory_usage_add(&self->super.super, log_msg_get_size(msg));
}

static inline gboolean
_push_to_qout_tail(LogQueueDiskNonReliable *self, LogMessage *msg)
{
  if (!HAS_SPACE_IN_QUEUE(self->qout))
    return FALSE;

  LogPathOptions path_options = LOG_PATH_OPTIONS_INIT_NOACK;
  _push_to_memory_queue_tail(self, self->qout, msg, &path_options);

  return TRUE;
}

static inline gboolean
_push_to_qoverflow_tail(LogQueueDiskNonReliable *self, LogMessage *msg, const LogPathOptions *path_options)
{
  if (!HAS_SPACE_IN_QUEUE(self->qoverflow))
    return FALSE;

  _push_to_memory_queue_tail(self, self->qoverflow, msg, path_options);

  return TRUE;
}

static gboolean
_push_tail(LogQueueDisk *s, LogMessage *msg, GString *serialized, LogPathOptions *local_options,
           const LogPathOptions *path_options)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;

  if (!_has_messages_on_disk(self))
    {
      if (_push_to_qout_tail(self, msg))
        return TRUE;
    }

  if (!_has_messages_in_queue(self->qoverflow))
    {
      if (log_queue_disk_write_message(s, serialized))
        return TRUE;
    }

  if (_push_to_qoverflow_tail(self, msg, path_options))
    {
      local_options->ack_needed = FALSE;
      return TRUE;
    }

  _report_message_drop(self);

  return FALSE;
}

static void
_free_queue (GQueue *q)
{
  while (!g_queue_is_empty (q))
    {
      LogMessage *lm;
      LogPathOptions path_options = LOG_PATH_OPTIONS_INIT;

      lm = g_queue_pop_head (q);
      POINTER_TO_LOG_PATH_OPTIONS (g_queue_pop_head (q), &path_options);
      log_msg_ack (lm, &path_options, AT_PROCESSED);
      log_msg_unref (lm);
    }
  g_queue_free (q);
}

static void
_freefn (LogQueueDisk *s)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;
  _free_queue (self->qoverflow);
  self->qoverflow = NULL;
  _free_queue (self->qout);
  self->qout = NULL;
  _free_queue (self->qbacklog);
  self->qbacklog = NULL;
}

static gboolean
_load_queue (LogQueueDisk *s, const gchar *filename)
{
  /* qdisk portion is not yet started when this happens */
  g_assert(!qdisk_started (s->qdisk));

  return _start(s, filename);
}

static gboolean
_save_queue (LogQueueDisk *s, gboolean *persistent)
{
  gboolean success = FALSE;
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;
  if (qdisk_save_state (s->qdisk, self->qout, self->qbacklog, self->qoverflow))
    {
      *persistent = TRUE;
      success = TRUE;
    }
  qdisk_stop (s->qdisk);
  return success;
}

static void
_restart(LogQueueDisk *s, DiskQueueOptions *options)
{
  LogQueueDiskNonReliable *self = (LogQueueDiskNonReliable *) s;
  qdisk_init_instance(self->super.qdisk, options, "SLQF");
}

static void
_set_virtual_functions (LogQueueDisk *self)
{
  self->get_length = _get_length;
  self->ack_backlog = _ack_backlog;
  self->rewind_backlog = _rewind_backlog;
  self->pop_head = _pop_head;
  self->push_head = _push_head;
  self->push_tail = _push_tail;
  self->start = _start;
  self->free_fn = _freefn;
  self->load_queue = _load_queue;
  self->save_queue = _save_queue;
  self->restart = _restart;
}

LogQueue *
log_queue_disk_non_reliable_new(DiskQueueOptions *options, const gchar *persist_name)
{
  g_assert(options->reliable == FALSE);
  LogQueueDiskNonReliable *self = g_new0(LogQueueDiskNonReliable, 1);
  log_queue_disk_init_instance(&self->super, persist_name);
  qdisk_init_instance(self->super.qdisk, options, "SLQF");
  self->qbacklog = g_queue_new ();
  self->qout = g_queue_new ();
  self->qoverflow = g_queue_new ();
  self->qout_size = options->qout_size;
  self->qoverflow_size = options->mem_buf_length;
  _set_virtual_functions (&self->super);
  return &self->super.super;
}
