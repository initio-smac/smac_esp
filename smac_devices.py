from debounce import DebouncedSwitch
from machine import Pin


class Switch():
	op_indicator = None

	#op_indicate
	def __init__(self, input, output, op_indicator=None, value=0, *args):
		ip = Pin( int(input), Pin.IN, Pin.PULL_UP)
		self.input =  DebouncedSwitch(ip, self.handle_ip_change )
		self.output = Pin( int(output), Pin.OUT)
		print("op_indicator: {}".format( op_indicator) )
		if op_indicator != None:
			self.op_indicator = Pin( int(op_indicator), Pin.OUT)
		if value:
			self.on()
		else:
			self.off()
		#self.output.value(value)
		

	def on(self, *args):
		self.output.on()
		if self.op_indicator != None:
			self.op_indicator.on()

	def off(self, *args):
		self.output.off()
		if self.op_indicator != None:
			self.op_indicator.off()

	def value(self):
		return self.output.value()

	def handle_ip_change(self, *args):
		if self.value():
			self.off()
		else:
			self.on()


class Geyser(Switch):
	pass


class Light(Switch):
	pass

class AC(Switch):
	pass

class Fan():
	op_indicator = None
	speed = 0
	MAX_SPEED = 4
	MIN_SPEED = 0

	def __init__(self, input, output=[], op_indicator=None, value=0, *args):
		ip = Pin( int(input), Pin.IN, Pin.PULL_UP)
		self.input =  DebouncedSwitch(ip, self.handle_ip_change )
		if len(output) < 3:
			raise Exception("Three Pins are required for Fan output. Only {} pins are given.".format(len(output)) )
		self.output = [ Pin( int(i), Pin.OUT) for i in output ]
		self.change_speed(value)

	def off(self):
		self.change_speed(0)

	def change_speed(self, value):
		s1, s2, s3= self.output
		if value == 0:
			s1.off()
			s2.off()
			s3.off()
		elif value == 1:
			s1.on()
			s2.off()
			s3.off()
		elif value == 2:
			s1.off()
			s2.on()
			s3.off()
		elif value == 3:
			s1.on()
			s2.on()
			s3.off()
		elif value == 4:
			s1.off()
			s2.off()
			s3.on()
		self.speed = value

	def handle_ip_change(self, *args):
		value = 0 if (self.speed == self.MAX_SPEED) else (self.speed+1)
		self.change_speed(value)