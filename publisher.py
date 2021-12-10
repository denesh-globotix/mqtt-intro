import paho.mqtt.client as mqtt
import yaml

with open("config.yaml", "r") as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as e:
        print(e)

client = mqtt.Client()
client.connect("localhost", 1883, 60)
topic = "/home/computer"
client.publish(topic, payload="on")
