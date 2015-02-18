from Queue import Queue
import thread
import sys,os,subprocess,time
from flask import Flask
from flask import request
import __builtin__
import json
import mimerender
import paho.mqtt.client as mqtt

'''
mqtt subscriber
subscribe to mqtt
publish the data to all extensions

Extensions
# websockets server
# db publisher
# rest endpoint caches

Rest endpoints
'''

MqttBrokerHost = "wangdrew.net"     # env var
MqttBrokerPort = 1883
KairosDbHost = "localhost"
KairosDbPort = 8083

class SensorServer:
    
    def __init__(self):
        self.mqttMessages = Queue()

    def startMqttSubscriber(self, mqttMessages):
        self.MqttSubThread = MqttSubscriber(mqttMessages)
        self.MqttSubThread.run()

    def run(self):
        # start mqtt subscriber
        thread.start_new_thread(self.startMqttSubscriber, (self.mqttMessages,))

        while True:
            if not self.mqttMessages.empty(): 
                msg = self.mqttMessages.get(False)
                print 'On queue %s - %s' % (msg.topicName, str(msg.value))

                # Give to exporters

class SensorMessage:
    def getTimestamp(self):
        return int(time.time() * 1e3)

    def __init__(self, topicName, value, ts = getTimestamp()):
        self.topicName = topicName
        self.value = value
        self.timestamp = ts

    def toDict(self):
        return {'topic': topicName, 'value': value}

    def toJson(self):
        json.dumps(toDict())


class MqttSubscriber:
    def __init__(self, sharedqueue):
        self.mqttMessages = sharedqueue

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker "+str(rc))
        client.subscribe("sensor/#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        self.mqttMessages.put(SensorMessage(msg.topic, msg.payload))

    def run(self):
        try:
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.on_message = self.on_message

            client.connect(MqttBrokerHost, MqttBrokerPort, 60)
            client.loop_forever()
        except Exception:
            import traceback
            print traceback.format_exc()

class DataPublisher:
    
    def publish(self, msg):
        pass


class KairosPublisher(DataPublisher):

    def __init__():
        self.kariosHost = KairosDbHost
        self.kairosPort = KairosDbPort  #TODO: Make these env vars
        self.kairosEndpoint = "http://" + str(self.KairosHost) + \
            ":" + str(self.KairosPort) + "/api/v1/datapoints"

    kairosMetric = {
        "name": "",
        "timestamp": "",
        "value" : "",
        "tags" : {"channel":"0"},
        "type" : "double"
    }

    def publish(self, msg):
        metricsToDB = []

        for metric in dataToWrite:
            metricBody = copy.deepcopy(kairosMetric)
            metricBody["name"] = msg.topic
            metricBody["timestamp"] = msg.timestamp
            metricBody["value"] = msg.value
            metricsToDB.append(metricBody)

        try:
            resp = requests.post(KairosUrl, data = json.dumps(metricsToDB))
            if resp.status_code != 204: # kairosDB success response code
                print resp.text
        except Exception as e:
            print(str(e))


# class RestPublisher(DataPublisher):

# class WebSocketsPublisher(DataPublisher):


# def main():
#   birdcapture = PhotoCapture()
#   birdcapture.run()

# def startRestServerThread(sharedqueue):
#       rest_server = CaptureRestServer(sharedqueue)
        # rest_server.run()

# class PhotoCapture:
#       self.sharedqueue = Queue(maxsize=1)


#   def checkQueueMessages(self):
#       while True:
#           if self.sharedqueue.empty():
#               break
#           else:
#               value = self.sharedqueue.get(False)
#               if 'bird' in value:
#                   return value['bird'] # Contains confidence level


#   def run(self):
#       thread.start_new_thread(startRestServerThread, (self.sharedqueue,))

#       while True:
#           data = self.checkQueueMessages()

#           # Use data to figure out whether to fire the shutter
#           if data is not None and self.shouldFireShutter(data):

#   def run_test(self):

#       thread.start_new_thread(startRestServerThread, (self.sharedqueue,))

def main():
    server = SensorServer()
    server.run()

if __name__ == "__main__":
    main()
