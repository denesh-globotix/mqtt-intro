import paho.mqtt.client as mqtt
import yaml

with open("config.yaml", "r") as f:
    try:
        config_params = (yaml.safe_load(f))
        topic = config_params['topic']
        host = config_params['host']
        message = config_params['message']
    except yaml.YAMLError as e:
        print(e)

client = mqtt.Client()
client.connect(host, 1883, 60)
client.publish(topic, payload=message, retain=True)