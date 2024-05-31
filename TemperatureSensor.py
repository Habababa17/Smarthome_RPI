from gpiozero import MCP3008
import math

class TemperatureSensor:
	def __init__(self, sensor_id):
		self.id = sensor_id
		
	def get_reading(self):
		offset = 400
		reading = int(1024 * (1 - MCP3008(channel = self.id).value)) - offset
		temp_c = math.log((10240000 / reading) - 10000)
		temp_c = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * temp_c ** 2)) * temp_c)
		temp_c = temp_c - 273.15
		return "%.2f" % temp_c
