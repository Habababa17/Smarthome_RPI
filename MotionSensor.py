from GPIOHandler import GPIOHandler
from Light import Light
import time
import RPi.GPIO as GPIO
from datetime import datetime
import requests
import json

class MotionSensor:
	def __init__(self, sensor_id, sensor_pin, light_id, light_pin, is_on=False):
		self.id = sensor_id
		self.pin = sensor_pin
		self.isOn = is_on
		self.handler = GPIOHandler(sensor_pin)
		self.handler.add_handler(self.alarm)
		self.light = Light(light_id, light_pin, is_on)
		
	def switch_state(self):
		if(self.isOn):
			return self.turn_off()
		else:
			return self.turn_on()
	
	def turn_on(self):
		self.isOn = True
		return self.light.turn_on()

	def turn_off(self):
		self.isOn = False
		return self.light.turn_off()

	def alarm(self):
		if(self.isOn):

			api = "http://ec2-51-21-98-162.eu-north-1.compute.amazonaws.com/api/"
			ap = "https://crappie-caring-gecko.ngrok-free.app/api/"
			api2 = "system/1/board/1/devices/alarm/sensorsRPi"
			params =  {
				'alarmId': "1",
				'alarmSensorId': f"{self.id}",
				'date': f"{datetime.now()}"}
			#from json import dump
			#pretty_json = json.dumps(params, indent=4)
			#print(pretty_json)
			#with open("test.json", "w") as handle:
			#	dump(params, handle, indent=4)
			self.send_alarm(ap+api2,params)
			pass
			
	def send_alarm(self, api, parameters):
		response = requests.put(f"{api}", json=parameters)
		if response.status_code == 200:
			print("sucessfully posted the data with parameters provided")
		else:
			print(
				f"Hello, there's a {response.status_code} error with your request")
