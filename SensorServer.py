from Queue import Queue
import thread

from Subscriber import MqttSubscriber
from Publisher import InfluxPublisher
from Messages import PowerMessage, WeatherMessage

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
