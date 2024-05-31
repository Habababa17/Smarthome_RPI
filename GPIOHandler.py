import RPi.GPIO as GPIO

class GPIOHandler:
    def __init__(self, pin, debounce_time=10):
        self._pin = pin
        self._debounce_time = debounce_time
        self._handlers = []

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._pin, GPIO.RISING, callback=self._on_pin_change, bouncetime=self._debounce_time)

    def add_handler(self, handler):
        self._handlers.append(handler)

    def _on_pin_change(self, channel):
        for handler in self._handlers:
            handler()

    def cleanup(self):
        GPIO.remove_event_detect(self._pin)
        GPIO.cleanup()

