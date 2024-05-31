from flask import Flask, render_template, jsonify
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime
from Lightcontroller import LightController
from SensorController import SensorController
from KeypadFunctions import KeypadFunctions
from GPIOHandler import GPIOHandler
from MotionSensor import MotionSensor
from Alarmcontroller import AlarmController
from Light import Light
from Lock import Lock
from LockController import LockController
# Importing only one config
from config import *

#to modify used devices modify config.py file

def main():
	GPIO.setmode(GPIO.BCM)
	app = Flask(__name__)
        
    #inicialize light controller
	light_id = 0
	lights = []
	for pin in light_pins:
		lights.append(Light(light_id, pin))
		light_id = light_id + 1
	light_controller = LightController(lights)
    
    #inicialize sensor controller
	sensor_controller = SensorController(sensor_array)
    
    #inicialize alarm controller
	motion_id = 0
	motion_sensors = []
	for mpin, lpin in zip(motion_pins, motion_light_pins):
		motion_sensors.append(MotionSensor(motion_id, mpin, light_id, lpin, False))
		light_id = light_id + 1
		motion_id = motion_id + 1
	alarm_controller = AlarmController(motion_sensors)

	#inicialize KEYPAD
	factory = rpi_gpio.KeypadFactory()
	keypad = factory.create_keypad(keypad=KEYPAD, row_pins = ROW_PINS, col_pins = COL_PINS)
	keypadFunctions = KeypadFunctions(alarm_controller, Light(light_id, keypad_light_pin))
	light_id = light_id + 1
	keypad.registerKeyPressHandler(keypadFunctions.loop)
	
	#inicialize lock controller
	lock_id = 0
	locks = []
	for lock_pin in lock_pins:
		locks.append(Lock(lock_id, lock_pin))
		lock_id = lock_id + 1
	lock_controller = LockController(locks)
	
	@app.route('/lights/states')
	def getStates():
		return light_controller.getStates()

	@app.route('/lights/set/<int:lightId>/<int:newState>')
	def change(lightId, newState):
		code = light_controller.change(lightId, newState)
		if(code == 200):
			return [{"Message": "Changed correctly"}], code
		elif(code == 201):
			return [{"Message": f"Light {lightId} was already {'ON' if newState else 'OFF'}"}], code

	@app.route('/sensors/temperature')
	def getTemperatures():
		return sensor_controller.read_temperature()

	@app.route('/sensors/humidity')
	def get_humidity():
		return sensor_controller.read_humidity()
		
	@app.route('/sensors/light')
	def get_light():
		return sensor_controller.read_light()
    
	@app.route('/alarm/set/<int:sensorId>/<int:newState>')
	def setAlarmState(sensorId, newState):
		code = alarm_controller.set_state(sensorId, newState)
		return {},code
		
	@app.route('/alarm/get')
	def getAlarmState():
		return alarm_controller.get_state(), 200

	@app.route('/door-locks/states')
	def getLocksStates():
		return lock_controller.getStates()

	@app.route('/door-locks/states/<int:lockId>')
	def getLockState(lockId):
		return lock_controller.getState(lockId)

	@app.route('/door-locks/set/<int:newState>')
	def setLocksStates(newState):
		if (newState == 1):
			return lock_controller.closeAll()
		return lock_controller.openAll()

	@app.route('/door-locks/set/<int:lockId>/<int:newState>')
	def setLockState(lockId, newState):
		if (newState == 1):
			return lock_controller.close(lockId)
		return lock_controller.open(lockId)
		   
	app.run(debug = True, port = 5000, host = '0.0.0.0')
	
if __name__ == '__main__':
	main()
