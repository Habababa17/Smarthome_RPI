import time
import RPi.GPIO as GPIO
from datetime import datetime
import json


class Lock:
    def __init__(self, lock_id, lock_pin, is_open=1):
        self.lock_id = lock_id

        GPIO.setup(lock_pin, GPIO.OUT)
        self.servo = GPIO.PWM(lock_pin, 50)
        self.servo.start(0)

        self.isOpen = is_open
        if self.isOpen == 1:
            self.servo.ChangeDutyCycle(2 + (0 / 18))
        else:
            self.servo.ChangeDutyCycle(2 + (90 / 18))

    def open(self):
        self.isOpen = 1
        self.servo.ChangeDutyCycle(2 + (0 / 18))

    def close(self):
        self.isOpen = 0
        self.servo.ChangeDutyCycle(2 + (90 / 18))
