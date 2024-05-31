from pad4pi import rpi_gpio
from datetime import datetime, timedelta

class KeypadFunctions:
	def __init__(self, alarm_controller, light):
		self.alarm_controller = alarm_controller
		self.mode = True
		self.timeout = 5
		self.lastcall = ""
		self.mintime = 0.2
		#self.tries = 0
		#self.maxtries = 3
		self.code = "1234"
		self.inserted_code = ""
		self.alarmactivation = "****"
		self.current_sensor = 0
		self.light = light
		self.reset_attempt()
	def printKey(self, key):
		print(key)
	
	def loop(self, key):
		now = datetime.now()
		#print(key)
		#print(now - self.lastcall)
		delta = (now - self.lastcall).total_seconds()
		self.lastcall = now
		if(delta < self.mintime):
			return
		if(delta<self.timeout):
			print(key)
			self.readPassword(key)
		else:
			self.changeCurrentSensor(key)
			print(f"curr sensor: {key}")
		
	def readPassword(self, key):
		self.inserted_code = self.inserted_code + key
		if(len(self.inserted_code) < len(self.code)):
			# TODO FLASH char inserted to passord
			self.light.flash_short()
			pass
		else:
			self.chceckPassword()
		pass
	def reset_attempt(self):
		self.lastcall = datetime.now() - timedelta(seconds=self.timeout)
		
	def chceckPassword(self):
		if(self.inserted_code == self.code):
			self.alarm_controller.turn_off(self.current_sensor)
			self.light.flash_long()
			print("succes")
			self.reset_attempt()
		else:
			print("fail")
			self.light.flash_error()
			self.reset_attempt()
			pass
		self.inserted_code = ""
			
	def changeCurrentSensor(self, key):
		if(self.alarm_controller.containsSensor(int(key))):
			self.current_sensor = int(key)
			self.inserted_code = ""
			if(not self.alarm_controller.motion_sensors[int(key)].isOn):
				self.alarm_controller.turn_on(int(key))
			self.light.flash_short()

	
