#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import paho.mqtt.client as paho
from paho import mqtt
import yaml

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

with open("config.yaml", "r") as f:
    try:
        config_params = (yaml.safe_load(f))
        cloud_port = config_params['cloud_port']
        username = config_params['username']
        password = config_params['password']
        cluster_name = config_params['cluster_name']
        cloud_message = config_params['cloud_message']
    except yaml.YAMLError as e:
        print(e)

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(username, password)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(cluster_name, cloud_port)

# setting callbacks, use separate functions like above for better visibility
client.on_publish = on_publish

# a single publish, this can also be done in loops, etc.
client.publish("robots/information/1", payload= cloud_message, qos=1)
# client.publish("robots/information/1", payload= "Offline", qos=1)

client.will_set("robots/information", payload="Offline", qos=0, retain=True)
# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_stop()