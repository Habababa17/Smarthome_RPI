from TemperatureSensor import TemperatureSensor
from HumiditySensor import HumiditySensor
from LightSensor import LightSensor
from flask import jsonify
from datetime import datetime

class SensorController:
	def __init__(self, sensor_array):
		self.temperatureSensors = []
		self.humiditySensors = []
		self.lightSensors = []
		
		for sensor in sensor_array[0]:
			self.temperatureSensors.append(TemperatureSensor(sensor))
			
		for sensor in sensor_array[1]:
			self.humiditySensors.append(HumiditySensor(sensor))
			
		for sensor in sensor_array[2]:
			self.lightSensors.append(LightSensor(sensor))			
			
	def read_data(self, name, sensor_array):
		return_data = []
		
		for sensor in sensor_array:
			value = sensor.get_reading()
			timestamp = datetime.utcnow().isoformat() + "Z"
			data = {
			f"{name}": value,
			"dateTime": timestamp,
			"sensorId": sensor.id
		}
		return_data.append(data)
		return jsonify(return_data), 200

	def read_temperature(self):
		return self.read_data("temperature", self.temperatureSensors)
		
	def read_humidity(self):
		return self.read_data("humidity", self.humiditySensors)

	def read_light(self):
		return self.read_data("light", self.lightSensors)
