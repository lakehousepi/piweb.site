import RPi.GPIO as GPIO

class LEDController(object):
    def __init__(self, led_pin):
        self.led_pin = led_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        
    def on(self):
        GPIO.output(self.led_pin, True)
    
    def off(self):
        GPIO.output(self.led_pin, False)