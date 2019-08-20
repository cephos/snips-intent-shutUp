#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
import dbus

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def intent_received(hermes, intent_message):
    if intent_message.intent.intent_name == 'shutUp':
        sysbus = dbus.SystemBus()
        systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        manager.RestartUnit('snips-tts.service', 'fail')
    else:
        return

    hermes.publish_end_session(intent_message.session_id, "OK")


with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()
