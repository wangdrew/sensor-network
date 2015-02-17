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

MqttBrokerHost = "wangdrew.net"		# env var
MqttBrokerPort = 1883
KairosDbHost = "localhost"
KairosDbPort = 8083

class SensorServer:
	
	def __init__(self):
		self.mqttMessages = Queue()
		thread.start_new_thread(self.startMqttSubscriber, (self.mqttMessages,))

	def startMqttSubscriber(self, mqttMessages):
		print 'running'
		self.MqttSubThread = MqttSubscriber(mqttMessages)
		self.MqttSubThread.run()

	def run(self):
		while True:
			if self.mqttMessages.empty(): 
				break
			else:
				msg = self.mqttMessages.get(False)
				print 'On queue %s - %s' % (msg.topicName, str(msg.value))

class SensorMessage:
	def __init__(self, topicName, value):
		self.topicName = topicName
		self.value = value

	def toDict(self):
		return {'topic': topicName, 'value': value}

	def toJson(self):
		json.dumps(toDict())


class MqttSubscriber:
	def __init__(self, sharedqueue):
		print 'here'
		self.mqttMessages = sharedqueue

	def on_connect(client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		client.subscribe("sensor/#")

	def on_message(client, userdata, msg):
		print(msg.topic+" "+str(msg.payload))
		mqttMessages.put(SensorMessage(msg.topic, msg.payload))

	def run(self):
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message

		client.connect(MqttBrokerHost, MqttBrokerPort, 60)
		client.loop_forever()

# class DataPublisher:

# class KairosPublisher(DataPublisher):

# class RestPublisher(DataPublisher):

# class WebSocketsPublisher(DataPublisher):


# def main():
# 	birdcapture = PhotoCapture()
# 	birdcapture.run()

# def startRestServerThread(sharedqueue):
# 		rest_server = CaptureRestServer(sharedqueue)
		# rest_server.run()

# class PhotoCapture:
# 		self.sharedqueue = Queue(maxsize=1)


# 	def checkQueueMessages(self):
# 		while True:
# 			if self.sharedqueue.empty():
# 				break
# 			else:
# 				value = self.sharedqueue.get(False)
# 				if 'bird' in value:
# 					return value['bird'] # Contains confidence level


# 	def run(self):
# 		thread.start_new_thread(startRestServerThread, (self.sharedqueue,))

# 		while True:
# 			data = self.checkQueueMessages()

# 			# Use data to figure out whether to fire the shutter
# 			if data is not None and self.shouldFireShutter(data):

# 	def run_test(self):

# 		thread.start_new_thread(startRestServerThread, (self.sharedqueue,))


def main():
	server = SensorServer()
	server.run()

if __name__ == "__main__":
	main()
