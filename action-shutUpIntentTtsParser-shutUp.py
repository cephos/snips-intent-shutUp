#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from http.client import HTTPSConnection
from base64 import b64encode
import json
import dbus

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


def intent_received(self, hermes, intent_message):
    if intent_message.intent.intent_name == 'shutUp':

        config = read_configuration_file("config.ini")
        if config.get("secret").get("pegasus_user") is None:
            print "No pegasus_user in config.ini, you must setup an user for this skill to work"
        elif len(config.get("secret").get("pegasus_user")) == 0:
            print "No pegasus_user in config.ini, you must setup an user for this skill to work"
        skill_locale = config.get("secret", {"locale":"en_US"}).get("locale", u"en_US")

        #This sets up the https connection
        c = HTTPSConnection("localhost:8443")
        json_string = {'action': 'RESTART'}
        json_action = json.dumps(json_string)
        #we need to base 64 encode it 
        #and then decode it to acsii as python 3 stores it as a byte string
        userAndPassString = config.get("secret").get("pegasus_user")+":"+config.get("secret").get("pegasus_pass")
        userAndPass = b64encode(str.encode(userAndPassString)).decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-type': 'application/json' }
        #then connect
        c.request('GET', '/pegasus/platform/snips-audio-server', json_action, headers=headers)
        #get the response back
        res = c.getresponse()
        # at this point you could check the status etc
        # this gets the page text
        data = res.read()  
        print(data.decode())

        #sysbus = dbus.SystemBus()
        #systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        #manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        #manager.RestartUnit('snips-tts.service', 'fail')
    else:
        return

    hermes.publish_end_session(intent_message.session_id, "OK")


with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()
