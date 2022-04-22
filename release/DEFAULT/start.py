import json
import time
from DEVICE.smac_context import add_trigger, add_action, remove_action, remove_trigger
try:
    import machine
    import gc
    gc.enable()
    import uasyncio as asyncio
    from DEVICE.smac_devices import SmacFan, SmacSwitch
    import _thread
    ESP = True
except Exception as e:
    print(e)
    import asyncio
    ESP = False
from DEVICE.config import config
from DEVICE.smac_client import client
from DEVICE.smac_requests import req_get_device_id
from DEVICE.smac_platform import SMAC_PLATFORM
from DEVICE.smac_device_keys import SMAC_DEVICES, SMAC_PROPERTY
class smacInit():
    SENDING_INFO = 0
    TIME_SYNC = False
    RESET_BUTTON = 35
    MSG_COUNT_PREV = 0
    DEVICE_DATA_SEND_INTERVAL = 60
    def send_test(self, *args):
        d = {}
        d[ smac_keys["PROPERTY"] ] = SMAC_DEVICES["SWITCH"]
        d[ smac_keys["INSTANCE"] ] = 0
        msg = {}
        msg[ smac_keys["FROM"] ] = "D1"
        msg[ smac_keys["TO"] ] = "D2"
        msg[ smac_keys["COMMAND"] ] = smac_keys["CMD_SET_PROPERTY"]
        i = 0
        while 1:
            d[ smac_keys["VALUE"] ] = 1 if( i%2 == 0 ) else 0
            msg[ smac_keys["MESSAGE"] ] = d
            print("sending")
            print(msg)
            client.send_message( "D2", json.dumps(msg) )
            time.sleep(1)
            i += 1
    def send_device_info(self, dest_topic, *args):
        self.SENDING_INFO = 1
        topics = config.SUB_TOPIC
        print(topics)
        print("11")
        default_topic = ['', '', '']
        if( default_topic not in topics ):
            topics += [ default_topic ]
        for t in topics:
            if t[0] not in (config.ID_DEVICE,):
                m = {}
                m[ smac_keys["TOPIC"] ] = 1
                m[ smac_keys["ID_TOPIC"] ] = t[0]
                m[ smac_keys["NAME_HOME"]] = t[1]
                m[ smac_keys["NAME_TOPIC"]] = t[2]
                m[ smac_keys["NAME_DEVICE"]] = config.NAME_DEVICE
                m[ smac_keys["TYPE_DEVICE"]] = config.TYPE_DEVICE
                m[ smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                if t[0] == "":
                    client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_SEND_INFO"], message=m, udp=True, tcp=False)
                else:
                    client.send_message(frm=config.ID_DEVICE, to=t[0], cmd=smac_keys["CMD_SEND_INFO"], message=m, udp=False, tcp=True)
                for p in self.PROPERTY:
                    p1 = {}
                    p1[ smac_keys["PROPERTY"] ] = 1
                    p1[ smac_keys["ID_DEVICE"] ] = config.ID_DEVICE
                    p1[ smac_keys["ID_PROPERTY"] ] = p["id_property"]
                    p1[ smac_keys["TYPE_PROPERTY"] ] = p["type_property"]
                    p1[ smac_keys["NAME_PROPERTY"] ] = p["name_property"]
                    p1[ smac_keys["VALUE"]] = p["value"]
                    p1[ smac_keys["VALUE_MIN"]] = p["value_min"]
                    p1[ smac_keys["VALUE_MAX"]] = p["value_max"]
                    if t[0] == "":
                        client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_SEND_INFO"], message=p1, udp=True, tcp=False)
                    else:
                        client.send_message(frm=config.ID_DEVICE, to=t[0], cmd=smac_keys["CMD_SEND_INFO"], message=p1, udp=False, tcp=True)
                print("send property to topic: {}".format(t[0]))
            print("sent topic ", t[0])
        self.SENDING_INFO = 0
    def add_topic(self, frm, id_topic, name_home, name_topic, id_device, passkey, id_message, *args):
        print("len SUB_TOPIC", len(config.SUB_TOPIC))
        print(config.LIMIT)
        print(config.get_config_variable(key="limit_topic"))
        if config.LIMIT["LIMIT_TOPIC"] >= len(config.SUB_TOPIC) :
            if str(passkey) == str(config.PIN_DEVICE):
                config.update_config_variable(key='sub_topic', value=[id_topic, name_home, name_topic], arr_op="ADD", reload_variables=True)
                client.subscribe(id_topic)
                d = {}
                d[ smac_keys["ID_TOPIC"] ] = id_topic
                d[ smac_keys["ID_DEVICE"] ] = config.ID_DEVICE
                d[ smac_keys["NAME_DEVICE"]] = config.NAME_DEVICE
                d[ smac_keys["TYPE_DEVICE"]] = config.TYPE_DEVICE
                d[ smac_keys["NAME_HOME"]] = name_home
                d[ smac_keys["NAME_TOPIC"]] = name_topic
                d[ smac_keys["ID_MESSAGE"]] = id_message
                client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_STATUS_ADD_TOPIC"], message=d, udp=True, tcp=True)
                d1 = {}
                d1[ smac_keys["MESSAGE"] ] = "Topic subscribed successfylly"
                print("subscribed topic: {}".format(id_topic))
            else:
                d1 = {}
                d1[smac_keys["MESSAGE"]] = "Topic '{}' not subscribed".format(id_topic)
                d1[smac_keys["ID_DEVICE"]] = id_device
                d1[smac_keys["ID_MESSAGE"]] = id_message
                d1[smac_keys["ID_TOPIC"]] = id_topic
                print("Cannot subscribe to {}. Passkey error.".format(id_topic))
                if config.ID_DEVICE == frm:
                    print("same device")
                else:
                    client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"], message=d1, udp=True, tcp=True)
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Topic '{}/{}' not subscribed. Topic Limit Reached.".format(name_home, name_topic)
            d1[smac_keys["ID_DEVICE"]] = id_device
            d1[smac_keys["ID_TOPIC"]] = id_topic
            d1[smac_keys["ID_MESSAGE"]] = id_message
            print("Cannot subscribe to {}. Topic Limit Reached.".format(id_topic))
            if config.ID_DEVICE == frm:
                print("same device")
            else:
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_TOPIC_LIMIT_EXCEEDED"], message=d1)
    def delete_topic(self, frm, id_topic, id_device, passkey, id_message, *args):
        print(passkey)
        print(config.PIN_DEVICE)
        print(passkey == config.PIN_DEVICE)
        if str(passkey) == str(config.PIN_DEVICE):
            config.update_config_variable(key='sub_topic', value=id_topic, arr_op="REM", reload_variables=True)
            client.unsubscribe(id_topic)
            d = {}
            d[ smac_keys["ID_TOPIC"] ] = id_topic
            d[ smac_keys["ID_DEVICE"] ] = config.ID_DEVICE
            d[ smac_keys["ID_MESSAGE"]] = id_message
            d[ smac_keys["NAME_DEVICE"]] = config.NAME_DEVICE
            d[ smac_keys["TYPE_DEVICE"]] = config.TYPE_DEVICE
            client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_STATUS_REMOVE_TOPIC"], message=d, udp=True, tcp=True)
            d1 = {}
            d1[ smac_keys["MESSAGE"] ] = "Topic unsubscribed successfylly"
            print("unsubscribed topic: {}".format(id_topic))
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Topic '{}' not unsubscribed".format(id_topic)
            d1[smac_keys["ID_DEVICE"]] = id_device
            d1[smac_keys["ID_TOPIC"]] = id_topic
            d1[smac_keys["ID_MESSAGE"]] = id_message
            print("Cannot unsubscribe to {}. Passkey error.".format(id_topic))
            if config.ID_DEVICE == frm:
                print("same device")
            else:
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"], message=d1, udp=True, tcp=True)
    def on_message(self, topic, message, protocol, *args):
        client.MSG_COUNT += 1
        try:
            if( topic not in  [config.ID_DEVICE, "#"]):
                config.update_topic_msg_count(topic)
            msg = json.loads(message)
            frm = msg.get( smac_keys["FROM"] , None)
            to = msg.get( smac_keys["TO"], None)
            cmd = msg.get( smac_keys["COMMAND"], None )
            ack = msg.get( smac_keys["ACK"], None )
            msg_id = msg.get( smac_keys["ID_MESSAGE"], None )
            data = msg
            if (frm != config.ID_DEVICE):
                if cmd == smac_keys["CMD_SET_PROPERTY"]:
                    id_prop = msg.get( smac_keys["ID_PROPERTY"], None)
                    type_prop = msg.get( smac_keys["TYPE_PROPERTY"], None)
                    value = msg.get( smac_keys["VALUE"], 0 )
                    if type_prop in [ SMAC_PROPERTY["SWITCH"], SMAC_PROPERTY["FAN"] ]:
                        value = value if(type(value) == int) else  int(value)
                        config.update_config_variable(key=id_prop, value=value)
                        config.update_config_variable(key=str(id_prop) + "_time", value=time.time())
                except Exception as e:
                    print("error ip config: {}".format(e))
        if ESP:
            self.send_device_info(dest_topic="#")
            t3 = asyncio.create_task(self.subscribe_topics())
            t1 = asyncio.create_task(client.main())
            t2 = asyncio.create_task(self.interval())
            t4 = asyncio.create_task(self.interval2())
            await t4
            await t3
            await t2
            await t1
        else:
            asyncio.gather( client.main(), self.send_test())
cli = smacInit()
asyncio.run( cli.start() )