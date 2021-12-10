import paho.mqtt.client as mqtt
import yaml

with open("config.yaml", "r") as f:
    try:
        config_params = (yaml.safe_load(f))
        topic = config_params['topic']
    except yaml.YAMLError as e:
        print(e)

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.publish(topic, payload="on")