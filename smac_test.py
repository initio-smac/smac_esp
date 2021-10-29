import json
import time

# from debounce import DebouncedSwitch
from machine import Pin

from smac_device_keys import SMAC_PROPERTY
TIM = .5
ONLY_INPUT_PINS = ["34", "35", "36", "37", "38", "39"]

class SmacSwitch:
    op_indicator = None
    input_pin = None
    ID_PROP = None

    # op_indicate
    def __init__(self, input_pin, output, op_indicator=None, value=0, id_property=None, *args):
        if id_property != None:
            self.ID_PROP = id_property
        if (input_pin != "") and (input_pin != None):
            print("IP", input_pin)
            print("IP in ", (input_pin in ONLY_INPUT_PINS) )
            #if input_pin not in ONLY_INPUT_PINS:
            ip = Pin( int(input_pin), Pin.IN, Pin.PULL_UP)
            ip.irq(handler=self.handle_ip_change, trigger=Pin.IRQ_FALLING)
            #else:
            #    ip = Pin(int(input_pin), Pin.IN, Pin.PULL_DOWN )
            #    ip.irq(handler=self.handle_ip_change, trigger=Pin.IRQ_RISING)
            # self.input_pin =  DebouncedSwitch(ip, self.handle_ip_change )
            self.input_pin = ip
        self.output = Pin(int(output), Pin.OUT)
        print("op_indicator: {}".format(op_indicator))
        if op_indicator != None:
            self.op_indicator = Pin(int(op_indicator), Pin.OUT)
        if value:
            self.on()
        else:
            self.off()

    def on(self, *args):
        self.output.on()
        if self.op_indicator != None:
            self.op_indicator.on()

    def off(self, *args):
        self.output.off()
        if self.op_indicator != None:
            self.op_indicator.off()

    def set_value(self, value):
        print("value", value)
        print("IP value", self.input_pin.value())
        #print("\n")
        self.output.value(value)

    def value(self):
        return self.output.value()

    def handle_ip_change(self, *args):
        print("changed", self.input_pin.value())
        print(args)
        print(self.ID_PROP)


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
        if id_property != None:
            self.ID_PROP = id_property
        if (input_pin != "") and (input_pin != None):
            print("IP", input_pin)
            print("IP in ", (input_pin in ONLY_INPUT_PINS))
            #if input_pin not in ONLY_INPUT_PINS:
            ip = Pin(int(input_pin), Pin.IN, Pin.PULL_UP)
            ip.irq(handler=self.handle_ip_change_fan, trigger=Pin.IRQ_FALLING)
            #else:
            #    ip = Pin(int(input_pin), Pin.IN, Pin.PULL_DOWN)
            #    ip.irq(handler=self.handle_ip_change_fan, trigger=Pin.IRQ_RISING)
            # self.input_pin =  DebouncedSwitch(ip, self.handle_ip_change_fan )
            self.input_pin = ip
        if len(output) < 3:
            raise Exception("Three Pins are required for Fan output. Only {} pins are given.".format(len(output)))
        self.output = [Pin(int(i), Pin.OUT) for i in output]
        self.change_speed(value)

    def off(self):
        self.change_speed(0)

    def value(self):
        return self.speed

    def set_value(self, value, *args):
        self.change_speed(value)

    def change_speed(self, value):
        try:
            print("value", value)
            print("IP value", self.input_pin.value())
            # print(self.output)
            s1, s2, s3 = self.output
            print(self.output)
            #print("\n")
            if value:
                s1.on()
                #time.sleep(.1)
                s2.on()
                #time.sleep(.1)
                s3.on()
            else:
                s1.off()
                #time.sleep(.1)
                s2.off()
                #time.sleep(.1)
                s3.off()
            print("s1 val", s1.value())
            print("s2 val", s2.value())
            print("s3 val", s3.value())
            self.speed = value
            return s3.value()
            if value == 0:
                s1.off()
                #time.sleep(TIM)
                s2.off()
                #time.sleep(TIM)
                s3.off()
            elif value == 1:
                s1.on()
                #time.sleep(TIM)
                #s2.off()
                #time.sleep(TIM)
                #s3.off()
            elif value == 2:
                #s1.off()
                #time.sleep(TIM)
                s2.on()
                #time.sleep(TIM)
                #s3.off()
            elif value == 3:
                #s1.on()
                #time.sleep(TIM)
                #s2.on()
                #time.sleep(TIM)
                s3.off()
            elif value == 4:
                #s1.off()
                #time.sleep(TIM)
                #s2.off()
                #time.sleep(TIM)
                s3.on()
            # time.sleep(.5)
            # s2.off()
            self.speed = value
        # print(self.speed)
        except Exception as e:
            print("change speed err: {}".format(e))


    def handle_ip_change_fan(self, *args):
        print("changed Fan", self.speed, self.ID_PROP)

PROP_INSTANCE = {}
with open("device.json", "r") as f:
    try:
        f1 = json.loads(f.read())
        for p in f1:
            # print(p)
            id_prop = p["id_property"]
            type_prop = p["type_property"]
            # instance = p["instance"]
            ip_pin = p["pin_input"]
            if (ip_pin != None) and (ip_pin != ""):
                ip_pin = ip_pin.split(",")
            op_pin = p["pin_output"]
            op_pin = op_pin.split(",")
            if type_prop == SMAC_PROPERTY["FAN"]:
                # config.PROP["{}:{}".format(prop, instance)] = Fan( input=ip_pin[0], output=op_pin, value=pre_val )
                PROP_INSTANCE[id_prop] = SmacFan(input_pin=ip_pin[0], output=op_pin, value=0,
                                                        id_property=id_prop)
            elif type_prop == SMAC_PROPERTY["SWITCH"]:
                # config.PROP["{}:{}".format(prop, instance)] = Switch( input=ip_pin[0], output=op_pin[0], value=pre_val )
                PROP_INSTANCE[id_prop] = SmacSwitch(input_pin=ip_pin[0], output=op_pin[0], value=0,
                                                           id_property=id_prop)
            # time.sleep(.1)
            # await  asyncio.sleep(.1)
        print(PROP_INSTANCE)
    except Exception as e:
        print("error ip config: {}".format(e))

import random
_vals = ["P0", "P1", "P2", "P3"]
p = input("Enter Input: P")
#p = "P3"
val = 0
while 1:
    #p = random.choice(_vals)
    #p = "P3"
    #val = 1 - PROP_INSTANCE[p].value()
    val = 1 - val
    print("####")
    print("PID", p)
    print(PROP_INSTANCE[p].value())
    res = PROP_INSTANCE[p].set_value(val)
    print("TIME: ", time.time())
    print("****")
    print("\n")
    #print( [ PROP_INSTANCE[i].input_pin.value()  for i in _vals ] )
    time.sleep(1)

    '''text = input("Enter to control device")
    try:
        PID = text
        v = 1 - PROP_INSTANCE[PID].value()
        PROP_INSTANCE[PID].set_value(v)
        #for i in PROP_INSTANCE.keys():
        #    print("IP val", PROP_INSTANCE[i].input_pin.value())
        #time.sleep(1)
    except:
        pass'''

