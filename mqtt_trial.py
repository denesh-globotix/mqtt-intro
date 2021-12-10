import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)
topic = "my_topic"
client.publish(topic, payload="on")
