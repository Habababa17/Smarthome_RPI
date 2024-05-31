from GPIOHandler import GPIOHandler
import RPi.GPIO as GPIO
import threading
import time

class Light:
	def __init__(self, light_id, pin, is_on = False):
		self.id = light_id
		self.pin = pin
		self.isOn = is_on
		self._led_thread = None
		self._led_stop_event = threading.Event()
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(self.pin, self.isOn)
	
	def switch_state(self):
		if(self.isOn):
			return self.turn_off()
		else:
			return self.turn_on()
	
	def turn_on(self):
		self.isOn = True
		GPIO.output(self.pin, self.isOn)
		return 200

	def turn_off(self):
		self.isOn = False
		GPIO.output(self.pin, self.isOn)
		return 200

	def _flash_led(self, duration):
		GPIO.output(self.pin, GPIO.HIGH)
		time.sleep(duration)
		GPIO.output(self.pin, GPIO.LOW)

	def flash_short(self):
		self._led_stop_event.clear()
		self._led_thread = threading.Thread(target=self._flash_led, args=(0.1,))
		self._led_thread.start()

	def flash_long(self):
		self._led_stop_event.clear()
		self._led_thread = threading.Thread(target=self._flash_led, args=(1.0,))
		self._led_thread.start()

	def flash_error(self):
		#Your custom LED flashing pattern here
		self._led_stop_event.clear()
		self._led_thread = threading.Thread(target=self._custom_flash)
		self._led_thread.start()

	def _custom_flash(self):
		#Implement your custom LED flashing pattern here
		pattern = [(0.5, 0.5)] *3  # Example pattern: on for 0.1s, off for 0.2s, etc.
		for duration, interval in pattern:
			GPIO.output(self.pin, GPIO.HIGH)
			time.sleep(duration)
			GPIO.output(self.pin, GPIO.LOW)
			time.sleep(interval)

	def stop_led_flash(self):
		self._led_stop_event.set()
		if self._led_thread:
			self._led_thread.join()  # Wait for the thread to finish
		GPIO.output(self.pin, GPIO.LOW)

	def cleanup(self):
		GPIO.remove_event_detect(self.pin)
		self.stop_led_flash()
		GPIO.cleanup()


			
