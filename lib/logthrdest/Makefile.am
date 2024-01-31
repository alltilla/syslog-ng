logthrdestincludedir = ${pkgincludedir}/logthrdest

EXTRA_DIST += lib/logthrdest/CMakeLists.txt

logthrdestinclude_HEADERS = \
  lib/logthrdest/logthrdestdrv.h \
  lib/logthrdest/exponential-backoff.h

logthrdest_sources = \
  lib/logthrdest/logthrdestdrv.c \
  lib/logthrdest/exponential-backoff.c

include lib/logthrdest/tests/Makefile.am
