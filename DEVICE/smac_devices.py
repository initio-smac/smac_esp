#import uasyncio as asyncio
import time

from DEVICE.config import config
from debounce import Switch, Pushbutton
from machine import Pin
import machine

IP_PINS_SENSITIVE = ["32", "33", "34", "35"]
RESET_BUTTON = 33


# on double click,
# change the mode restart in web AP mode
def on_dbl_click(*args):
	mode = 2
	config.update_config_variable(key="mode", value=mode)
	machine.reset()


# on long press,
# reset the device to default code
def on_long_press( *args):
	from web_server import copy_folder
	print("Resetting to Default Version...")
	copy_folder(COPY_FROM="DEFAULT", COPY_TO="DEVICE")
	config.update_config_variable(key="mode", value=0)
	machine.reset()


class SmacSwitch:
	op_indicator = None
	input_pin = None
	ID_PROP = None


	#op_indicate
	def __init__(self, input_pin, output, op_indicator=None, value=0, id_property=None, *args):
		if id_property != None:
			self.ID_PROP = id_property
		if(input_pin != "") and (input_pin != None):
			ip = Pin(int(input_pin), Pin.IN, Pin.PULL_UP)
			#ip.irq(handler=self.handle_ip_change)
			#self.input_pin = ip
			ip_type = config.get_config_variable("input_type")
			print("ip type", ip_type)
			if( ip_type == "pushbutton" ):
				self.input_pin = Pushbutton(ip)
				self.input_pin.release_func(self.handle_ip_change, ())
			else:
				self.input_pin = Switch(ip)
				self.input_pin.open_func(self.handle_ip_change, ())
				self.input_pin.close_func(self.handle_ip_change, ())

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
		print(args)
		print(self.ID_PROP)
		if self.ID_PROP != None:
			#val = 1 - self.value()
			val = config.get_config_variable(key=self.ID_PROP)
			if val == None:
				val = 0
			val = 1 - val
			print(val)
			config.update_config_variable(key=self.ID_PROP, value=val)
			config.update_config_variable(key=str(self.ID_PROP) + "_time", value=time.time())
			if val:
				config.PROP_INSTANCE[self.ID_PROP].on()
			else:
				config.PROP_INSTANCE[self.ID_PROP].off()


class Geyser(SmacSwitch):
	pass


class Light(SmacSwitch):
	pass

class AC(SmacSwitch):
	pass

class SmacFan:
	op_indicator = None
	speed = 0
	MAX_SPEED = 4
	MIN_SPEED = 0
	ID_PROP = None
	input_pin = None

	def __init__(self, input_pin, output=[], op_indicator=None, value=0, id_property=None, *args):
		#self.speed = value
		if id_property != None:
			self.ID_PROP = id_property
		if(input_pin != "") and (input_pin != None):
			ip = Pin(int(input_pin), Pin.IN, Pin.PULL_UP)
			#ip.irq(handler=self.handle_ip_change_fan)
			#self.input_pin = ip
			#self.input_pin =  DebouncedSwitch(ip, self.handle_ip_change_fan )
			ip_type = config.get_config_variable("input_type")
			print(input_pin)
			print(ip_type)
			if (ip_type == "pushbutton"):
				self.input_pin = Pushbutton(ip)
				self.input_pin.release_func(self.handle_ip_change_fan, ())
			if input_pin == str(RESET_BUTTON):
			#	self.input_pin = Pushbutton(ip)
			#	self.input_pin.double_func(on_dbl_click, ())
			#	self.input_pin.long_func(on_long_press, ())
				pass
			else:
				self.input_pin = Switch(ip)
				self.input_pin.open_func(self.handle_ip_change_fan, ())
				self.input_pin.close_func(self.handle_ip_change_fan, ())

		if len(output) < 3:
			raise Exception("Three Pins are required for Fan output. Only {} pins are given.".format(len(output)) )
		self.output = [ Pin( int(i), Pin.OUT) for i in output ]
		self.change_speed(value)

	def off(self):
		self.change_speed(0)

	def change_speed(self, value):
		try:
			print("fan speed value", value)
			print(self.output)
			s1, s2, s3= self.output
			if value == 0:
				s1.off()
				time.sleep(.5)
				s2.off()
				time.sleep(.5)
				s3.off()
			elif value == 1:
				s1.on()
				time.sleep(.5)
				s2.off()
				time.sleep(.5)
				s3.off()
			elif value == 2:
				s1.off()
				time.sleep(.5)
				s2.on()
				time.sleep(.5)
				s3.off()
			elif value == 3:
				s1.on()
				time.sleep(.5)
				s2.on()
				time.sleep(.5)
				s3.off()
			elif value == 4:
				s1.off()
				time.sleep(.5)
				s2.off()
				time.sleep(.5)
				s3.on()
				#time.sleep(.5)
				#s2.off()
			print(s1.value())
			print(s2.value())
			print(s3.value())
			self.speed = value
			print(self.speed)
		except Exception as e:
			print("change speed err: {}".format(e))

	def value(self):
		return self.speed

	def handle_ip_change_fan(self, *args):
		#value = 0 if (self.speed == self.MAX_SPEED) else (self.speed+1)
		#self.change_speed(value)
		print("changed Fan", self.speed, self.ID_PROP)
		#print(self.ID_PROP)
		if self.ID_PROP != None:
			val = 0 if (self.speed == self.MAX_SPEED) else (self.speed+1)
			config.update_config_variable(key=self.ID_PROP, value=val)
			config.update_config_variable(key=str(self.ID_PROP) + "_time", value=time.time())
