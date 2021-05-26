set(MQTT_SOURCES
    mqtt-destination.c
    mqtt-destination.h
    mqtt-parser.c
    mqtt-parser.h
    mqtt-plugin.c
    mqtt-worker.c
    mqtt-worker.h
)

find_package(systemd)
find_package(mosquitto)

add_module(
  TARGET mqtt
  GRAMMAR mqtt-grammar
  INCLUDES ${ZLIB_INCLUDE_DIRS}
           ${WRAP_INCLUDE_DIRS}
           ${Libsystemd_INCLUDE_DIRS}
  DEPENDS ${WRAP_LIBRARIES}
          ${ZLIB_LIBRARIES}
          OpenSSL::SSL
          OpenSSL::Crypto
          libnet
          mosquitto
          ${Libsystemd_LIBRARIES}
  SOURCES ${MQTT_SOURCES}
)

