# import RPi.GPIO as GPIO
import time
import threading

Debounce = 0.1

class LightController:
	def __init__(self, light_array):
		self.lights = light_array

	def change(self, light_id, new_state):
		new_state = bool(new_state)
		if new_state == self.lights[light_id].isOn:
			return 201
		if new_state: 
			self.lights[light_id].turn_on()
			return 200
		self.lights[light_id].turn_off()
		return 200
    
	def getStates(self):
		json_data = [{"lightId": i, "isOn": value.isOn} for i, value in enumerate(self.lights)]
		return json_data, 200
