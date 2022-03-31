from DEVICE.smac_device_keys import *
from DEVICE.smac_client import client
from DEVICE.smac_keys import smac_keys
import asyncio
import threading

TOTAL_DEVICES =  5
PROPERTY = [
    {
      "id_property": "P0",
      "type_property": "0",
      "name_property": "SWITCH1",
      "value": "0",
      "value_min": "0",
      "value_max": "1",
      "pin_output": "2",
      "pin_input": "26"
    },
   {
      "id_property": "P1",
      "type_property": "0",
      "name_property": "SWITCH2",
      "value": "0",
      "value_min": "0",
      "value_max": "1",
      "pin_output": "4",
      "pin_input": "27"
    },
   {
      "id_property": "P2",
      "type_property": "0",
      "name_property": "SWITCH3",
      "value": "0",
      "value_min": "0",
      "value_max": "1",
      "pin_output": "5",
      "pin_input": "32"
   },
   {
      "id_property": "P3",
      "type_property": "1",
      "name_property": "FAN",
      "value": "0",
      "value_min": "0",
      "value_max": "4",
      "pin_output": "12,13,14",
      "pin_input": "33"
  }
]

class TestDevice():
    id_device = ""
    type_device = ""
    name_device = ""
    PROPERTY = []

    def send_device_info(self, dest_topic="#", *args):
        print("sending device data")
        topics = [ ("#", 'test_all_home', 'test_all_topic1'), (self.id_device, "", "") ]
        print(topics)
        for t in topics:
            m = {}
            m[ smac_keys["TOPIC"] ] = 1
            m[ smac_keys["ID_TOPIC"] ] = t[0]
            m[ smac_keys["NAME_HOME"]] = t[1]
            m[ smac_keys["NAME_TOPIC"]] = t[2]
            m[ smac_keys["NAME_DEVICE"]] = self.name_device
            m[ smac_keys["TYPE_DEVICE"]] = self.type_device
            m[ smac_keys["ID_DEVICE"]] = self.id_device
            print(m)
            client.send_message(frm=self.id_device, to=dest_topic, cmd=smac_keys["CMD_DEVICE_DATA"], message=m, udp=True, tcp=True)
            print("sent {}".format(t))

        print("send topics")
        for p in self.PROPERTY:
            print(p)
            p1 = {}
            p1[ smac_keys["PROPERTY"] ] = 1
            p1[ smac_keys["ID_DEVICE"] ] = self.id_device
            p1[ smac_keys["ID_PROPERTY"] ] = p["id_property"]
            p1[ smac_keys["TYPE_PROPERTY"] ] = p["type_property"]
            p1[ smac_keys["NAME_PROPERTY"] ] = p["name_property"]
            p1[ smac_keys["VALUE"]] = p["value"]
            p1[ smac_keys["VALUE_MIN"]] = p["value_min"]
            p1[ smac_keys["VALUE_MAX"]] = p["value_max"]
            client.send_message(frm=self.id_device, to=dest_topic, cmd=smac_keys["CMD_DEVICE_DATA"], message=p1, udp=True, tcp=True)
        print("send property")

    def subscribe(self, topic):
    	client.subscribe(topic)

    def unsubscribe(self):
    	client.unsubscribe(topic)

    async def start(self):
    	t1 = asyncio.create_task( client.main() )
    	await t1



DEVICES = {}

def main(*args):
    asyncio.run( client.main() )

t1 = threading.Thread(target=main, args=())
t1.start()

for dev in range(2, TOTAL_DEVICES):
    DEVICES[dev] = TestDevice()
    id_device = "D{}".format(dev)
    print("starting instance: {}".format(id_device) )
    name_device = id_device
    type_device = SMAC_DEVICES["ESP"]
    DEVICES[dev].id_device = id_device
    DEVICES[dev].name_device = name_device
    DEVICES[dev].type_device = type_device
    DEVICES[dev].PROPERTY = PROPERTY
    DEVICES[dev].send_device_info()

	

	