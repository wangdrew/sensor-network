import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("testtopic")

# client = mqtt.Client()
# client.connect("wangdrew.net", 1883, 60)
# client.on_connect = on_connect

publish.single("testtopic", payload="lalalalala huh", hostname="wangdrew.net", port=1883)