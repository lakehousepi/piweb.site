import RPi.GPIO as GPIO
import time

class MorseFlasher(object):
	def __init__(self, led_pin, dash_len=0.3, dot_len=0.1, blip_wait=0.1, 
			letter_wait=0.3, punct_wait=0.3, debug=False):
		self.led_pin = led_pin
		self.dash_len = dash_len
		self.dot_len = dot_len
		self.blip_wait = blip_wait
		self.letter_wait = letter_wait
		self.punct_wait = punct_wait
		self.debug = debug
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.led_pin, GPIO.OUT)
		
		self.alphabet = {
			'e': '.',
			't': '-',
			'a': '.-',
			'i': '..',
			'n': '-.',
			'm': '--',
			's': '...',
			'u': '..-',
			'r': '.-.',
			'w': '.--',
			'd': '-..',
			'k': '-.-',
			'g': '--.',
			'o': '---',
			'h': '....',
			'v': '...-',
			'f': '..-.',
			'l': '.-..',
			'p': '.--.',
			'j': '.---',
			'b': '-...',
			'x': '-..-',
			'c': '-.-.',
			'y': '-.--',
			'z': '--..',
			'q': '--.-',
			' ': ' ',
			',': '  ',
			';': '  ',
			':': '   ',
			'.': '   '
		}
		
		self.action_map = {
			'.': self.dot,
			'-': self.dash,
			' ': self.p_wait
		}
		
	def dot(self):
		GPIO.output(self.led_pin, True)
		time.sleep(self.dot_len)
		GPIO.output(self.led_pin, False)
		time.sleep(self.blip_wait)
		
	def dash(self):
		GPIO.output(self.led_pin, True)
		time.sleep(self.dash_len)
		GPIO.output(self.led_pin, False)
		time.sleep(self.blip_wait)
	
	def p_wait(self):
		time.sleep(self.punct_wait)

	def flash_char(self, char):
		char = char.lower()
		if self.debug:
			print '  trying to flash character "%s"' % char
			
		if char not in self.alphabet:
			print '    unknown character: "%s"' % char
		else:
			for e in self.alphabet[char]:
				if self.debug:
					print '    trying to flash element "%s"' % e
				if e not in self.action_map:
					print '      unknown element: "%s"' % e
				else:
					self.action_map[e]()
					time.sleep(self.letter_wait)
		
	def flash_string(self, string):
		if self.debug:
			print 'trying to flash string "%s"' % string
		for char in string:
			self.flash_char(char)