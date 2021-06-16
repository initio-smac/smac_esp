import time

from config import config
from debounce import DebouncedSwitch
from machine import Pin



class Switch():
	op_indicator = None
	ID_PROP = None

	#op_indicate
	def __init__(self, input, output, op_indicator=None, value=0, id_property=None, *args):
		if id_property != None:
			self.ID_PROP = id_property
		ip = Pin( int(input), Pin.IN, Pin.PULL_DOWN)
		#self.input =  DebouncedSwitch(ip, self.handle_ip_change )
		self.input = ip
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
		#if self.value():
		#	self.off()
		#else:
		#	self.on()
		print("changed", self.value())
		print(self.ID_PROP)
		if self.ID_PROP != None:
			val = 1 - self.value()
			config.update_config_variable(key=self.ID_PROP, value=val)
			config.update_config_variable(key=str(self.ID_PROP) + "_time", value=time.time())


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
	ID_PROP = None

	def __init__(self, input, output=[], op_indicator=None, value=0, id_property=None, *args):
		if id_property != None:
			self.ID_PROP = id_property
		ip = Pin( int(input), Pin.IN, Pin.PULL_DOWN)
		#self.input =  DebouncedSwitch(ip, self.handle_ip_change_fan )
		self.input = ip
		if len(output) < 3:
			raise Exception("Three Pins are required for Fan output. Only {} pins are given.".format(len(output)) )
		self.output = [ Pin( int(i), Pin.OUT) for i in output ]
		self.change_speed(value)

	def off(self):
		self.change_speed(0)

	def change_speed(self, value):
		try:
			print("value", value)
			#print(self.output)
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
				time.sleep(.5)
				s2.on()
				s3.off()
			elif value == 4:
				s1.off()
				s2.on()
				time.sleep(.5)
				s3.on()
				time.sleep(.5)
				s2.off()
			self.speed = value
			#print(self.speed)
		except Exception as e:
			print("change speed err: {}".format(e))

	def handle_ip_change_fan(self, *args):
		#value = 0 if (self.speed == self.MAX_SPEED) else (self.speed+1)
		#self.change_speed(value)
		print("changed Fan", self.speed, self.ID_PROP)
		#print(self.ID_PROP)
		if self.ID_PROP != None:
			val = 0 if (self.speed == self.MAX_SPEED) else (self.speed+1)
			config.update_config_variable(key=self.ID_PROP, value=val)
			config.update_config_variable(key=str(self.ID_PROP) + "_time", value=time.time())