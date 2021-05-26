noinst_LTLIBRARIES      += modules/mqtt/destination/libmqtt_destination.la
modules_mqtt_destination_libmqtt_destination_la_SOURCES = \
  modules/mqtt/destination/mqtt-grammar.y       \
  modules/mqtt/destination/mqtt-parser.c        \
  modules/mqtt/destination/mqtt-parser.h        \
  modules/mqtt/destination/mqtt-callback.c      \
  modules/mqtt/destination/mqtt-callback.h      \
  modules/mqtt/destination/mqtt-plugin.c        \
  modules/mqtt/destination/mqtt-worker.h        \
  modules/mqtt/destination/mqtt-worker.c        \
  modules/mqtt/destination/mqtt-destination.h   \
  modules/mqtt/destination/mqtt-destination.c

BUILT_SOURCES       +=      \
  modules/mqtt/destination/mqtt-grammar.y       \
  modules/mqtt/destination/mqtt-grammar.c       \
  modules/mqtt/destination/mqtt-grammar.h

EXTRA_DIST        +=      \
  modules/mqtt/destination/mqtt-grammar.ym \
  modules/mqtt/destination/CMakeLists.txt

modules_mqtt_destination_libmqtt_destination_la_CPPFLAGS  =     \
  $(AM_CPPFLAGS)                              \
  -I$(top_srcdir)/modules/mqtt/destination/  \
  -I$(top_builddir)/modules/mqtt/destination/

modules_mqtt_destination_libmqtt_destination_la_LIBADD  = $(MODULE_DEPS_LIBS)
modules_mqtt_destination_libmqtt_destination_la_LDFLAGS = $(MODULE_LDFLAGS)
modules_mqtt_destination_libmqtt_destination_la_DEPENDENCIES= $(MODULE_DEPS_LIBS)
