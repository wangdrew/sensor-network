import time
import json

class SensorMessage:

    def __init__(self, sensorId, sensorLocation, messageType, sensorData, timestamp = None):
        self.timestamp = timestamp() if timestamp is None else timestamp
        self.sensorId = sensorId
        self.sensorLocation = sensorLocation
        self.messageType = messageType
        self.sensorData = sensorData

    def timestamp(self):
        return int(time.time() * 1e3)

    def asDict(self):
        return {
            'timestamp': self.timestamp,
            'sensorId': self.sensorId,
            'sensorLocation': self.sensorLocation,
            'messageType': self.messageType,
            'sensorData': self.sensorData
        }

    def asJson(self):
        json.dumps(self.asDict())


class PowerMessage(SensorMessage):
    def __init__(self, sensorId, sensorLocation, powerW, currentA, voltageV, costCent, energykWh):

        SensorMessage.__init__(sensorId, sensorLocation, 'power', sensorData=
                               {'powerW': powerW,
                                'currentA': currentA,
                                'voltageV': voltageV,
                                'costCent': costCent,
                                'energyKwh': energykWh})



class WeatherMessage(SensorMessage):
    def __init__(self, sensorId, sensorLocation, tempDegC, tempDegF, pressurePa, relHumidityProp):

        SensorMessage.__init__(sensorId, sensorLocation, 'weather', sensorData=
                               {'tempDegC': tempDegC,
                                'tempDegF': tempDegF,
                                'pressurePa': pressurePa,
                                'relHumidityProp': relHumidityProp})