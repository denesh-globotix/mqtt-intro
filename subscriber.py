import paho.mqtt.client as mqtt
import yaml

# The callback for when the client receives a response from the server


def on_connect(client, userdata, flags, rc):
    print(f"Connected with client code {client}")
    print(f"Connected with User Data {userdata}")
    print(f"Connected with flags {flags}")
    print(f"Connected with result code {str(rc)}")


def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message


    with open("config.yaml", "r") as f:
        try:
            config_params = (yaml.safe_load(f))
            topic = config_params['topic']
            host = config_params['host']
        except yaml.YAMLError as e:
            print(e)

    client.connect(host, port=1883, keepalive=60)
    client.subscribe(topic)

    client.loop_forever()
