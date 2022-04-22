from DEVICE.smac_device_keys import *
#from DEVICE.smac_client import client
from DEVICE.smac_keys import smac_keys
#import asyncio
import threading
import socket
import time
import json
import asyncio


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
    #--------------------------------------------------------------------------------
    # Cast bytes to bytearray     0   1   2   3   4   5   6   7   8   9   
    zGreetingSig = bytearray(b'\xFF\x00\x00\x00\x00\x00\x00\x00\x01\x7F')
    zGreetingVerMajor= bytearray(b'\x03')    
    zGreetingVerMinor= bytearray(b'\x00')    
    zGreetingMech= bytearray(b"NULL")
    zGreetingEnd = bytearray(48) 
    #                                        R   E   A   D   Y       S
    zHandshake1  = bytearray(b'\x04\x19\x05\x52\x45\x41\x44\x59\x0B\x53')
    #                            o   c   k   e   t   -   T   y   p   e     
    zHandshake2  = bytearray(b'\x6F\x63\x6B\x65\x74\x2D\x54\x79\x70\x65\x00\x00\x00')
    #                                S   U   B
    zHandshake3_sub  = bytearray(b'\x03\x53\x55\x42')
    #                                P   U   B
    zHandshake3_pub  = bytearray(b'\x03\x50\x55\x42')
    #
    zSubStart = bytearray(b'\x00\x01\x01')
    #---------------------------------------------------------------------------------

    SUB_TOPIC = []
    MSG_ID = 0
    UDP_PORT = 37020

    def __init__(self, *args):
        # create TCP/IP socket
        self.sock_sub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock_sub.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock_pub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock_pub.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock_sub = self.sock_pub
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.udp_sock.setblocking(False)
        try:
            self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except:
            pass

        try:
            self.udp_sock.bind(("", self.UDP_PORT))
        except:
            pass
        
    def subscribe(self, topic1):
        topic  = str(topic1)
        if topic not in self.SUB_TOPIC:
            t = topic 
            tt = bytes('\x00', encoding="utf-8") + bytes( [ len(t)+1 ] ) + bytes('\x01', encoding="utf-8") + bytes( t , encoding="utf-8")
            print(tt)
            self.sock_sub.send(tt)
            self.SUB_TOPIC.append(topic)
            print("subscribed to {}".format(t) )
        
        
    def unsubscribe(self, topic1):
        topic  = str(topic1)
        if topic in self.SUB_TOPIC:
            t = topic 
            tt = bytes('\x00', encoding="utf-8") + bytes( [ len(t)+1 ] )  + bytes('\x00', encoding="utf-8") + bytes( t , encoding="utf-8")
            self.sock_sub.send(tt)
            self.SUB_TOPIC.remove(topic)
            print(tt)
            print("unsubscribed to {}".format(t))
        

    def connect_sub(self, server_address, port):
        self.sock_sub.connect( (server_address, port) )

    def connect_pub(self, server_address, port):
        self.sock_pub.connect( (server_address, port) )

    id_device = ""
    type_device = ""
    name_device = ""
    PROPERTY = []
    PUB_READY = False
    SUB_READY = False

    def send_device_info(self, dest_topic="#", *args):
        #print("sending device data")
        topics = [ ("#", 'test_all_home', 'test_all_topic1'), (self.id_device, "", "") ]
        #print(topics)
        for t in topics:
            m = {}
            m[ smac_keys["TOPIC"] ] = 1
            m[ smac_keys["ID_TOPIC"] ] = t[0]
            m[ smac_keys["NAME_HOME"]] = t[1]
            m[ smac_keys["NAME_TOPIC"]] = t[2]
            m[ smac_keys["NAME_DEVICE"]] = self.name_device
            m[ smac_keys["TYPE_DEVICE"]] = self.type_device
            m[ smac_keys["ID_DEVICE"]] = self.id_device
            #print(m)
            self.send_message(frm=self.id_device, to=dest_topic, cmd=smac_keys["CMD_DEVICE_DATA"], message=m, udp=True, tcp=True)
            #print("sent {}".format(t))

        #print("send topics")
        for p in self.PROPERTY:
            #print(p)
            p1 = {}
            p1[ smac_keys["PROPERTY"] ] = 1
            p1[ smac_keys["ID_DEVICE"] ] = self.id_device
            p1[ smac_keys["ID_PROPERTY"] ] = p["id_property"]
            p1[ smac_keys["TYPE_PROPERTY"] ] = p["type_property"]
            p1[ smac_keys["NAME_PROPERTY"] ] = p["name_property"]
            p1[ smac_keys["VALUE"]] = p["value"]
            p1[ smac_keys["VALUE_MIN"]] = p["value_min"]
            p1[ smac_keys["VALUE_MAX"]] = p["value_max"]
            self.send_message(frm=self.id_device, to=dest_topic, cmd=smac_keys["CMD_DEVICE_DATA"], message=p1, udp=True, tcp=True)
        #print("send property")

    def init_publish(self):
        #await asyncio.sleep(1)
        #self.sock_pub
        self.sock_pub.connect( ("smacsystem.com", 5556) )
        #await asyncio.sleep(1)
        #time.sleep(1)
        #time.sleep(1)
        self.sock_pub.send(self.zGreetingSig)
        #sock.send(b"hello")
        print("Sending ZMQ Greeting")
        while True:
            data = self.sock_pub.recv(16)
            if (data.startswith(bytes(self.zGreetingSig))) : #Found zmqGreeting
                print("Got ZMQ Greeting! PUB")
                self.sock_pub.send(self.zGreetingVerMajor+self.zGreetingVerMinor)
                print("ZMQ Ver/Mech PUB")   
                self.sock_pub.send(self.zGreetingMech+self.zGreetingEnd)              
                self.sock_pub.send(self.zHandshake1+self.zHandshake2+self.zHandshake3_pub)
            if (b"READY" in data) : #Found READY  
                print("ReAdY PUB") 
                #ba = bytearray('\x00\x06\x30\x31\x32\x33\x34\x35', encoding="utf-8")
                #msg = 'D1 hello world : {}'.format(time.time())  
                #msg = 'D7.T1643718637 {"5": "#", "7": "g", "6": "D1"}\n'
                #ba1 = bytearray('\x00', encoding="utf-8") + bytes([len(msg)] )
                #print( ba1 + bytearray(msg, encoding="utf-8") )
                #sock.send( ba1 + bytearray(msg, encoding="utf-8")    )  
                self.PUB_READY = True
                #await asyncio.sleep(2)
                #msg1 = 'T2 hello world : {}'.format(time.time())  
                #print( ba1 + bytearray(msg1, encoding="utf-8") )
                #sock.send( ba1 + bytearray(msg1, encoding="utf-8")    )  
            if data:
                d = ''.join(chr(i) for i in data)
                print(d)
            else:
                #print ("<END Connection pub>")
                #break 
                pass
            #await asyncio.sleep(0)

    def init_subscribe(self):
        #await asyncio.sleep(1)
        self.sock_sub.connect( ("smacsystem.com", 5572) )
        while True:
            data = self.sock_sub.recv(16)          
            if (data.startswith(bytes(self.zGreetingSig))) : #Found zmq Greeting
                print("ZMQ Greeting! SUB")
                self.sock_sub.send(self.zGreetingSig+self.zGreetingVerMajor)
            if (b"NULL" in data) : #Found zmq NULL Mechnism
                print("ZMQ Ver/Mech SUB")   
                self.sock_sub.send(self.zGreetingVerMinor+self.zGreetingMech+self.zGreetingEnd)              
                self.sock_sub.send(self.zHandshake1+self.zHandshake2+self.zHandshake3_sub)
            if (b"READY" in data): #Found zmq READY, Send Subscription Start
                print("ZMQ READY Subscribe")  
                #self.sock.send(self.zSubStart)
                #self.sock_sub.send( bytearray(b'\x00\x03\x01T2 ') )
                #self.sock_sub.send( bytearray(b'\x00\x03\x01T1 ') )
                self.SUB_READY= True
                
            if data:
                d = ''.join(chr(i) for i in data)
                print(d)
            else:
                print ("<END Connection sub>")
                #break
            #time.sleep(0)
            #await asyncio.sleep(0)  

    def send_message(self, frm, to, cmd, message={}, udp=True, tcp=True, *args):
        topic = to
        msg = message
        msg[ smac_keys["FROM"] ] = frm
        msg[ smac_keys["TO"] ] = to
        msg[ smac_keys["COMMAND"] ] = cmd
        msg = json.dumps(msg)
        msg1 = "{} {}".format(topic, msg)
        
        if udp:
            try:
                addr = "255.255.255.255" 
                self.udp_sock.sendto(msg1.encode("utf-8"), (addr, self.UDP_PORT))
            except Exception as e:
                print("UDP message send err: {}".format(e))
        if tcp:
            try:
                if self.PUB_READY:
                    ba1 = bytearray('\x00', encoding="utf-8") +  bytes([len(msg)])
                    #print( ba1  )
                    self.sock_pub.send( ba1 + bytearray(msg1, encoding="utf-8")    )  
                    #await asyncio.sleep(2)
            except Exception as e:
                print("ZMQ message send err: {}".format(e))
        self.MSG_ID += 1

    def subscribe_topics(self, topics, *args):
        #await asyncio.sleep(1)
        while True:
            #await asyncio.sleep(1)
            time.sleep(1)
            print(self.SUB_READY)
            if self.SUB_READY:
                print("AA")
                #await asyncio.sleep(10)
                print("BB")
                #self.sock_sub.send( bytearray(b'\x00\x03\x01T1') )
                #time.sleep(2)
                #self.sock_sub.send( bytearray(b'\x00\x03\x01T2') )
                for t in topics:
                    self.subscribe(t)
                break
        print("ended")

    async def send_interval(self, *args):
        print("starting interval")
        await asyncio.sleep(1)
        #time.sleep(1)
        print("starting interval2")
        while True:
            print("starting interval3")
            #await asyncio.sleep(1)
            print("PUB_READY :", self.PUB_READY)
            if self.PUB_READY:
                await asyncio.sleep(0)
                print("sending device info of {}".format(self.id_device) )
                self.send_device_info()
                #threading.Timer(10, self.send_interval).start()
                #time.sleep(10)
            await asyncio.sleep(10)
            #time.sleep(10)


    def start_thread(self):
        #t1 = asyncio.create_task( client.main() )
        #await t1
        th1 = threading.Thread(target=self.init_publish, args=())
        th1.start()
        #th1.join()
        th2 = threading.Thread(target=self.init_subscribe, args=())
        th2.start()
        #th2.join()
        t = [ '#', self.id_device, "T1", "T2", "T3", "T4", "T5" ]
        th3 = threading.Thread(target=self.subscribe_topics, args=( t, ))
        th3.start()
        #th3.join()
        th4 = threading.Thread(target=self.send_interval, args=() )
        th4.start()
        #th4.join()

    async def start_tasks(self):
        #t4 = asyncio.create_task( self.send_interval() )
        #t1 = asyncio.create_task(self.init_subscribe() )
        #t2 = asyncio.create_task(self.init_publish())
        
        
        #await t1
        #await t2
        #await t4
        await asyncio.gather( self.send_interval())
        


    def main(self, *args):
        t = [ '#', self.id_device, "T1", "T2", "T3", "T4", "T5" ]
        th3 = threading.Thread(target=self.subscribe_topics, args=( t, ))
        th3.start()
        th2 = threading.Thread(target=self.init_subscribe, args=() )
        th2.start()
        th4 = threading.Thread(target=self.init_publish, args=() )
        th4.start()
        asyncio.run( self.start_tasks() )



DEVICES = {}

#def main(*args):
    #asyncio.run( client.main() )

#t1 = threading.Thread(target=main, args=())
#t1.start()
TOTAL_DEVICES =  3
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
    th = threading.Thread(target=DEVICES[dev].main, args=() )
    th.start()
    #DEVICES[dev].start1()

	

	