/*
 * Copyright (c) 2018 Balabit
 * Copyright (c) 2018 Kokan
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

#include "syslog-ng.h"

#include <signal.h>

#define SIGNAL_HANDLER_ARRAY_SIZE 128

static const struct sigaction *external_sigactions[SIGNAL_HANDLER_ARRAY_SIZE] = { NULL };
static gboolean internal_sigaction_registered[SIGNAL_HANDLER_ARRAY_SIZE] = { FALSE };

void
signal_handler_exec_external_handler(gint signum)
{
  g_assert(signum < SIGNAL_HANDLER_ARRAY_SIZE);

  const struct sigaction *external_sigaction = external_sigactions[signum];

  if (!external_sigaction || !external_sigaction->sa_handler)
    return;

  external_sigaction->sa_handler(signum);
}

#if SYSLOG_NG_HAVE_DLFCN_H

#include <dlfcn.h>

static int
_original_sigaction(int signum, const struct sigaction *act, struct sigaction *oldact)
{
  static int (*real_sa)(int, const struct sigaction *, struct sigaction *);

  if (real_sa == NULL)
    real_sa = dlsym(RTLD_NEXT, "sigaction");

  return real_sa(signum, act, oldact);
}

static gboolean
_need_to_save_external_sigaction_handler(gint signum)
{
  /* We need to save external sigaction handlers for signums we internally set a handler to. See lib/mainloop.c */
  switch (signum)
    {
    case SIGCHLD:
    case SIGINT:
      g_assert(signum < SIGNAL_HANDLER_ARRAY_SIZE);
      return TRUE;
    default:
      return FALSE;
    }
}

static void
_save_external_sigaction_handler(gint signum, const struct sigaction *external_sigaction)
{
  if (external_sigaction && external_sigaction->sa_handler == SIG_DFL)
    return;

  external_sigactions[signum] = external_sigaction;
}

/* This should be as defined in the <signal.h> */
int
sigaction(int signum, const struct sigaction *act, struct sigaction *oldact)
{
  if (!_need_to_save_external_sigaction_handler(signum))
    return _original_sigaction(signum, act, oldact);

  /* Internal sigactions are always the first one to arrive to this function. */
  if (!internal_sigaction_registered[signum])
    {
      gint result = _original_sigaction(signum, act, oldact);

      if (result == 0)
        internal_sigaction_registered[signum] = TRUE;

      return result;
    }

  _save_external_sigaction_handler(signum, act);
  return 0;
}

#endif
