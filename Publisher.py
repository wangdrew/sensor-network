from abc import ABCMeta, abstractmethod
import json
from SensorServer import KairosDbHost, KairosDbPort

__author__ = 'andrewwang'


class DataPublisher(metaclass=ABCMeta):

    @abstractmethod
    def publish(self, msg):
        pass


class InfluxPublisher(DataPublisher):
    def __init__(self, host, port, username, password, dbName):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbName = dbName

    def publish(self, msg):
        msg.timstamp


class KairosPublisher(DataPublisher):

    def __init__(self):
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

