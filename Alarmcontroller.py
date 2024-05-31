from MotionSensor import MotionSensor


class AlarmController:
	def __init__(self, motion_sensors):
		self.motion_sensors = motion_sensors
	
	def get_state(self):
		sensor_states = {}
		json_states = []
		for motion_sensor in self.motion_sensors:
			json_data = {"alarmSensorId": f"{motion_sensor.id}", "alarmId": "1", "isOn": 1 if motion_sensor.isOn else 0, "movementDetected": 1}
			json_states.append(json_data)
		return json_states 
		
	def set_state(self, sensor_id, new_state):
		new_state = bool(new_state)
		if(new_state):
			return self.motion_sensors[int(sensor_id)].turn_on()
		else:
			return self.motion_sensors[int(sensor_id)].turn_off()
			
	def switch_state(self, sensor_id):
		return self.motion_sensors[int(sensor_id)].switch_state()
	
	def turn_on(self, sensor_id):
		return self.motion_sensors[int(sensor_id)].turn_on()

	def turn_off(self, sensor_id):
		return self.motion_sensors[int(sensor_id)].turn_off()
	
	def containsSensor(self, sensor_id):
		for sensor in self.motion_sensors:
			if(sensor.id == sensor_id):
				return True
		return False
		
