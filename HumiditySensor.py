from gpiozero import MCP3008

class HumiditySensor:
	def __init__(self, sensor_id):
		self.id = sensor_id
		
	def get_reading(self):
		return "%.2f" % MCP3008(channel = self.id).value
