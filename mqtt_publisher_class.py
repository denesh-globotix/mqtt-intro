#!/usr/bin/env python3
import paho.mqtt.client as paho
from paho import mqtt
import yaml

import sys
from signal import signal, SIGINT


class MQTTPubClient(paho.Client):
    def __init__(self):
        # using MQTT version 5 here
        # userdata is user defined data of any type, updated by user_data_set()
        # client_id is the given name of the client
        self.client = paho.Client(
            client_id="", userdata=None, protocol=paho.MQTTv5)
        with open("config.yaml", "r") as f:
            try:
                config_params = (yaml.safe_load(f))
                self.cloud_port = config_params['cloud_port']
                self.username = config_params['username']
                self.password = config_params['password']
                self.cluster_name = config_params['cluster_name']
                self.cloud_message = config_params['cloud_message']
            except yaml.YAMLError as e:
                print(e)

        self.client.on_connect = self.on_connect

        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        # set username and password
        self.client.username_pw_set(self.username, self.password)

        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect(self.cluster_name, self.cloud_port)

        # setting callbacks, use separate functions like above for better visibility
        self.client.on_publish = self.on_publish

        # a single publish, this can also be done in loops, etc.
        connect = True

        if (connect):
            print("publish to connect")
            self.client.publish("robots/information/7",
                                payload=self.cloud_message, qos=1)
        else:
            print("publish to disconnect")
            self.client.publish("robots/information/1",
                                payload="Offline", qos=2)

        self.client.loop_forever()


    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))


if __name__ == "__main__":
    mqqq_client = MQTTPubClient()
