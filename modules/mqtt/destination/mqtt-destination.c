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
mqtt_destination_dd_set_host (LogDriver *d, const gchar host)
{
    // TODO    
}

void
mqtt_destination_dd_set_port (LogDriver *d, const gint port)
{
    // TODO    
}

void
mqtt_destination_dd_set_topic(LogDriver *d, const gchar topic)
{
    // TODO    
}

void
mqtt_destination_dd_set_clean_session (LogDriver *d, const gboolean clean_session)
{
    // TODO    
}

void
mqtt_destination_dd_set_keepalive (LogDriver *d, const gint keepalive)
{
    // TODO    
}

/*
 * Utilities
 */

static const gchar *
_format_stats_instance(LogThreadedDestDriver *d)
{
    // TODO
}

static const gchar *
_format_persist_name(const LogPipe *d)
{
    // TODO
}

static gboolean
_dd_init(LogPipe *d)
{
    // TODO
}

gboolean
_dd_deinit(LogPipe *s)
{
    // TODO
}

static void
_dd_free(LogPipe *d)
{
    // TODO
}

LogDriver *
mqtt_destination_dd_new(GlobalConfig *cfg)
{
    // TODO
}
