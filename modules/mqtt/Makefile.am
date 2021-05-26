include modules/mqtt/destination/Makefile.am


MQTT_PLUGINS = \
  $(top_builddir)/modules/mqtt/destination/libmqtt_destination.la


module_LTLIBRARIES += modules/mqtt/libmqtt.la

modules_mqtt_libmqtt_la_SOURCES = \
  modules/mqtt/mqtt-plugins.c

modules_mqtt_libmqtt_la_LIBADD = $(MODULE_DEPS_LIBS) $(MQTT_PLUGINS)
modules_mqtt_libmqtt_la_DEPENDENCIES = $(MODULE_DEPS_LIBS) $(MQTT_PLUGINS)
modules_mqtt_libmqtt_la_LDFLAGS = $(MODULE_LDFLAGS)

EXTRA_DIST += modules/mqtt/CMakeLists.txt

modules/mqtt modules/mqtt/ mod-mqtt: modules/mqtt/libmqtt.la

.PHONY: modules/mqtt/ mod-mqtt
