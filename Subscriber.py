from paho.mqtt import client as mqtt

__author__ = 'andrewwang'


class MqttSubscriber:
    def __init__(self, mqttHost, mqttPort, messageQueue, topicName):
        self.mqttHost = mqttHost
        self.mqttPort = mqttPort
        self.mqttMessages = messageQueue
        self.topicName = topicName

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker "+str(rc))
        client.subscribe(self.topicName + "/#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        self.mqttMessages.put(SensorMessage(msg.topic, msg.payload))

    def run(self):
        try:
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.on_message = self.on_message

            client.connect(self.mqttHost, self.mqttPort, 60)
            client.loop_forever()
        except Exception:
            import traceback
            print traceback.format_exc()