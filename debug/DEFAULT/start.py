import json
import time

from DEVICE.smac_context import add_trigger, add_action, remove_action, remove_trigger

try:
    import machine
    import gc
    gc.enable()
    #from machine import Timer
    import uasyncio as asyncio
    from DEVICE.smac_devices import SmacFan, SmacSwitch
    import _thread
    #from smac_ota2 import smacOTA
    #import wifi_client
    ESP = True
except Exception as e:
    print(e)
    import asyncio
    ESP = False



from DEVICE.config import config
#config.load_config_variable()


from DEVICE.smac_client import client
from DEVICE.smac_requests import req_get_device_id
from DEVICE.smac_keys import smac_keys
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
            #await asyncio.sleep(1)
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
        #topics.remove( "#" )
        #topics.remove( config.ID_DEVICE )
        #topics.append( ['#', '', ''] )
        #print(topics)
        #print(dest_topic)
        #client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd= smac_keys["CMD_INIT_SEND_INFO"], message={}, udp=True, tcp=False)
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
                #print(m)
                if t[0] == "":
                    client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_SEND_INFO"], message=m, udp=True, tcp=False)
                else:
                    client.send_message(frm=config.ID_DEVICE, to=t[0], cmd=smac_keys["CMD_SEND_INFO"], message=m, udp=False, tcp=True)
                
                for p in self.PROPERTY:
                    #print(p)
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
        #client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd=smac_keys["CMD_END_SEND_INFO"], message={},
        #                    udp=True, tcp=False)


    def add_topic(self, frm, id_topic, name_home, name_topic, id_device, passkey, id_message, *args):
        print("len SUB_TOPIC", len(config.SUB_TOPIC))
        print(config.LIMIT)
        print(config.get_config_variable(key="limit_topic"))
        if config.LIMIT["LIMIT_TOPIC"] >= len(config.SUB_TOPIC) :
            if str(passkey) == str(config.PIN_DEVICE):
                #created_time = time.mktime((2000, 1, 1, 0, 0, 0, 5, 1))
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
                # sending ACK
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
                    #client.send_message(frm=config.ID_DEVICE, to=id_topic, cmd=smac_keys["CMD_INVALID_PIN"], message=d1)
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
        #print(type(passkey))
        #print(type(config.PIN_DEVICE))
        if str(passkey) == str(config.PIN_DEVICE):
            #db.add_network_entry(name_topic=id_topic, id_topic=id_topic, id_device=id_device, name_device=self.NAME_DEVICE, type_device=self.TYPE_DEVICE)
            #db.delete_network_entry_by_topic(id_topic, id_device)
            config.update_config_variable(key='sub_topic', value=id_topic, arr_op="REM", reload_variables=True)
            client.unsubscribe(id_topic)
            #self.delete_topic_widget(id_topic)
            d = {}
            d[ smac_keys["ID_TOPIC"] ] = id_topic
            d[ smac_keys["ID_DEVICE"] ] = config.ID_DEVICE
            d[ smac_keys["ID_MESSAGE"]] = id_message
            d[ smac_keys["NAME_DEVICE"]] = config.NAME_DEVICE
            d[ smac_keys["TYPE_DEVICE"]] = config.TYPE_DEVICE
            client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_STATUS_REMOVE_TOPIC"], message=d, udp=True, tcp=True)
            # sending ACK
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
            #print(args)
        client.MSG_COUNT += 1
        try:
            #print( "{}, {}, {}".format(topic, message, protocol) )
            if( topic not in  [config.ID_DEVICE, "#"]):
                config.update_topic_msg_count(topic)
            msg = json.loads(message)
            #print("1")
            frm = msg.get( smac_keys["FROM"] , None)
            to = msg.get( smac_keys["TO"], None)
            cmd = msg.get( smac_keys["COMMAND"], None )
            ack = msg.get( smac_keys["ACK"], None )
            msg_id = msg.get( smac_keys["ID_MESSAGE"], None )
            #data = msg.get( smac_keys["MESSAGE"], None )
            data = msg
            #print("2")
            #print(data)
            #print(cmd == smac_keys["CMD_SET_PROPERTY"])

            if (frm != config.ID_DEVICE):
                if cmd == smac_keys["CMD_SET_PROPERTY"]:
                    #print("3")
                    id_prop = msg.get( smac_keys["ID_PROPERTY"], None)
                    type_prop = msg.get( smac_keys["TYPE_PROPERTY"], None)
                    #instance = data.get( smac_keys["INSTANCE"], None )
                    value = msg.get( smac_keys["VALUE"], 0 )
                    #print(id_prop)
                    #print(type_prop)
                    #print(value)
                    #print("4")
                    if type_prop in [ SMAC_PROPERTY["SWITCH"], SMAC_PROPERTY["FAN"] ]:
                        #print("5")
                        value = value if(type(value) == int) else  int(value)
                        config.update_config_variable(key=id_prop, value=value)
                        config.update_config_variable(key=str(id_prop) + "_time", value=time.time())
                        '''if value:
                            #config.PROP["{}:{}".format(prop, instance) ].on()
                            config.PROP_INSTANCE[id_prop].on()
                            #print("6")
                        else:
                            #config.PROP["{}:{}".format(prop, instance) ].off()
                            config.PROP_INSTANCE[id_prop].off()
                        d = {}
                        d[smac_keys["ID_PROPERTY"]] = id_prop
                        d[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                        d[smac_keys["VALUE"]] = value
                        #topics = config.SUB_TOPIC
                        #for id_topic in topics:
                        #client.send_message(frm=config.ID_DEVICE, to="#", message=d, cmd=smac_keys["CMD_STATUS_SET_PROPERTY"], udp=True, tcp=False)
                        client.send_message(frm=config.ID_DEVICE, to="#", message=d, cmd=smac_keys["CMD_STATUS_SET_PROPERTY"], udp=True, tcp=False)'''

                if cmd == smac_keys["CMD_REQ_SEND_INFO"]:
                    print(self.SENDING_INFO)
                    #if not self.SEND_INFO:
                    print("sending device info...")
                    try:
                        #self.send_device_info( dest_topic=frm)
                        self.send_device_info( dest_topic="#")
                        pass
                    except Exception as e:
                        raise e

                if cmd == smac_keys["CMD_ADD_TOPIC"]:
                    id_topic = data.get(smac_keys["ID_TOPIC"])
                    id_device = data.get(smac_keys["ID_DEVICE"])
                    passkey = data.get(smac_keys["PASSKEY"])
                    name_home = data.get(smac_keys["NAME_HOME"])
                    name_topic = data.get(smac_keys["NAME_TOPIC"])
                    self.add_topic(frm, id_topic, name_home, name_topic, id_device, passkey, msg_id)
                    #self.ACKS.append( "{}:{}:{}".format(id_topic, id_device, smac_keys["CMD_ADD_TOPIC"]) )

                if cmd == smac_keys["CMD_REMOVE_TOPIC"]:
                    id_topic = data.get(smac_keys["ID_TOPIC"])
                    id_device = data.get(smac_keys["ID_DEVICE"])
                    passkey = data.get(smac_keys["PASSKEY"])
                    self.delete_topic(frm, id_topic, id_device, passkey, msg_id)

                if cmd == smac_keys["CMD_UPDATE_WIFI_CONFIG"]:
                    ssid = data.get(smac_keys["SSID"])
                    password = data.get(smac_keys["PASSWORD"])
                    passkey = data.get(smac_keys["PASSKEY"])
                    #id_message = data.get(smac_keys["ID_MESSAGE"])
                    if str(config.PIN_DEVICE) == str(passkey):
                        config.update_config_variable(key="wifi_config_2", value={"ssid": ssid, "password": password})
                        d1 = {}
                        d1[smac_keys["ID_MESSAGE"]] = msg_id
                        client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_UPDATE_WIFI_CONFIG"],message=d1, udp=True, tcp=True)
                    else:
                        d1 = {}
                        d1[smac_keys["MESSAGE"]] = "WIFI CONFIG not updated. Passkey Error"
                        #d1[smac_keys["ID_DEVICE"]] = frm
                        #d1[smac_keys["ID_TOPIC"]] = id_topic
                        d1[smac_keys["ID_MESSAGE"]] = msg_id
                        print("WIFI CONFIG not updated. Passkey Error")
                        client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                                message=d1, udp=True, tcp=True)

                if cmd == smac_keys["CMD_UPDATE_SOFTWARE"]:
                    config.update_config_variable(key="mode", value=1)
                    #config.update_config_variable(key="download_software", value=1)
                    #config.update_config_variable(key="download_software_requested_by", value=frm)
                    print("Restarting")
                    time.sleep(1)
                    machine.reset()



                if cmd == smac_keys["CMD_UPDATE_INTERVAL_ONLINE"]:
                    interval = data.get(smac_keys["INTERVAL"], 20)
                    passkey = data.get(smac_keys["PASSKEY"])
                    id_device = data.get(smac_keys["ID_DEVICE"])
                    #id_message = data.get(smac_keys["ID_MESSAGE"])
                    if id_device == config.ID_DEVICE:
                        if str(config.PIN_DEVICE) == str(passkey):
                            config.update_config_variable(key="interval_online", value=interval)
                            d1 = {}
                            d1[smac_keys["INTERVAL"]] = interval
                            d1[smac_keys["ID_DEVICE"]] = id_device
                            d1[smac_keys["ID_MESSAGE"]] = msg_id
                            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_UPDATE_INTERVAL_ONLINE"],message=d1, udp=True, tcp=True)
                        else:
                            d1 = {}
                            d1[smac_keys["MESSAGE"]] = "Online Interval not updated. Passkey Error"
                            #d1[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                            #d1[smac_keys["ID_TOPIC"]] = id_topic
                            d1[smac_keys["ID_MESSAGE"]] = msg_id
                            print(d1[smac_keys["MESSAGE"]])
                            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                                    message=d1, udp=True, tcp=True)

                if cmd == smac_keys["CMD_UPDATE_NAME_DEVICE"]:
                    name_device = data.get(smac_keys["NAME_DEVICE"])
                    id_device = data.get(smac_keys["ID_DEVICE"])
                    #id_message = data.get(smac_keys["ID_MESSAGE"])
                    if id_device == config.ID_DEVICE:
                        passkey = data.get(smac_keys["PASSKEY"])
                        if str(config.PIN_DEVICE) == str(passkey):
                            config.update_config_variable(key="NAME_DEVICE", value=name_device)
                            config.NAME_DEVICE = name_device
                            d1 = {}
                            d1[smac_keys["NAME_DEVICE"]] = name_device
                            d1[smac_keys["ID_DEVICE"]] = id_device
                            d1[smac_keys["ID_MESSAGE"]] = msg_id
                            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_UPDATE_NAME_DEVICE"],message=d1, udp=True, tcp=True)
                        else:
                            d1 = {}
                            d1[smac_keys["MESSAGE"]] = "Device Name not updated. Passkey Error"
                            d1[smac_keys["ID_MESSAGE"]] = msg_id
                            #d1[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                            #d1[smac_keys["ID_TOPIC"]] = id_topic
                            print(d1[smac_keys["MESSAGE"]])
                            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                                    message=d1, udp=True, tcp=True)

                if cmd == smac_keys["CMD_UPDATE_NAME_PROPERTY"]:
                    name_property = data.get(smac_keys["NAME_PROPERTY"])
                    id_property = data.get(smac_keys["ID_PROPERTY"])
                    id_device = data.get(smac_keys["ID_DEVICE"])
                    #id_message = data.get(smac_keys["ID_MESSAGE"])
                    if id_device == config.ID_DEVICE:
                        passkey = data.get(smac_keys["PASSKEY"])
                        d1 = {}
                        d1[smac_keys["NAME_PROPERTY"]] = name_property
                        d1[smac_keys["ID_PROPERTY"]] = id_property
                        d1[smac_keys["ID_DEVICE"]] = id_device
                        d1[smac_keys["ID_MESSAGE"]] = msg_id
                        if str(config.PIN_DEVICE) == str(passkey):
                            config.update_name_property(id_property, name_property)
                            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_UPDATE_NAME_PROPERTY"],message=d1, udp=True, tcp=True)
                        else:
                            d1[smac_keys["MESSAGE"]] = "Property Name not updated. Passkey Error"
                            #d1[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                            #d1[smac_keys["ID_TOPIC"]] = id_topic
                            print(d1[smac_keys["MESSAGE"]])
                            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                                    message=d1, udp=True, tcp=True)

                if cmd == smac_keys["CMD_ADD_ACTION"]:
                    add_action(data, frm)

                if cmd == smac_keys["CMD_ADD_TRIGGER"]:
                    add_trigger(data, frm)

                if cmd == smac_keys["CMD_REMOVE_ACTION"]:
                    remove_action(data, frm)

                if cmd == smac_keys["CMD_REMOVE_TRIGGER"]:
                    remove_trigger(data, frm)

                if cmd == smac_keys["CMD_TRIGGER_CONTEXT"]:
                    id_context = data.get( smac_keys["ID_CONTEXT"] )
                    self.trigger_context(id_context)

        except Exception as e:
            print("Exception while decoding message: {}, msg: {}".format(e, message) )
        #    raise e

    def trigger_context(self, id_context):
        print("Triggering Context ", id_context)
        actions = config.get_action_all()
        for act in actions.keys():
            a = act.split(":")
            id_context_act = a[1]
            if id_context == id_context_act:
                id_prop = a[3]
                type_prop = config.PROP_TYPE[id_prop]
                value = actions[act]
                self.set_property(id_prop, type_prop, value)

    async def interval_2(self):
        await asyncio.sleep(0)
        while 1:
            for num, prop in enumerate(self.PROPERTY):
                #print("\n\n\n")
                value = prop["value"]
                if type(value) == str:
                    value = int(value)
                id_prop = prop["id_property"]
                type_prop = prop["type_property"]
                value_temp = config.get_config_variable(key=id_prop)
                if value_temp == None:
                    value_temp = 0
                #print(prop)
                #print("num", num)
                #print(prop)
                #print(value)
                #print(value_temp)
                if value_temp != value:
                    print("\n\n\n")
                    #lastUpdated_time = config.get_config_variable(key=str(id_prop) + "_time")
                    #if lastUpdated_time == None:
                    #    lastUpdated_time = time.time()
                    #t_diff = time.time() - lastUpdated_time
                    #print(id_prop)
                    #print(type_prop)
                    #print(type(type_prop))
                    print("value_temp", value_temp)
                    print("value", value)
                    #print("t_diff", t_diff)
                    #if t_diff > .2:
                    changed = self.set_property(id_prop, type_prop, value_temp)
                    print("ch", changed)
                    if changed:
                        self.PROPERTY[num]["value"] = value_temp

                        #print("before")
                        #print(self.PROPERTY)

                        #print("after")
                        #print(self.PROPERTY)
                    #else:
                    #    print("Device is Busy")
                    #    d = {}
                    #    d[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                    #    d[smac_keys["VALUE"]] = 5
                        #client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_DEVICE_BUSY"], message=d, udp=True, tcp=False)
            await asyncio.sleep(.1)


    async def interval(self):
        await asyncio.sleep(0)
        COUNTER = 0
        print("INTERVAL", config.INTERVAL_ONLINE)
        print(type(config.INTERVAL_ONLINE))
        print(self.PROPERTY)
        while 1:
            #print(self.PROPERTY)

            '''for num, prop in enumerate(self.PROPERTY):
                #print("\n\n\n")
                value = prop["value"]
                if type(value) == str:
                    value = int(value)
                id_prop = prop["id_property"]
                type_prop = prop["type_property"]
                value_temp = config.get_config_variable(key=id_prop)
                if value_temp == None:
                    value_temp = 0
                #print(prop)
                #print("num", num)
                #print(prop)
                #print(value)
                #print(value_temp)
                if value_temp != value:
                    print("\n\n\n")
                    lastUpdated_time = config.get_config_variable(key=str(id_prop) + "_time")
                    if lastUpdated_time == None:
                        lastUpdated_time = time.time()
                    t_diff = time.time() - lastUpdated_time
                    print(id_prop)
                    #print(type_prop)
                    #print(type(type_prop))
                    print("value_temp", value_temp)
                    print("value", value)
                    print("t_diff", t_diff)
                    if t_diff > .2:
                        changed = self.set_property(id_prop, type_prop, value_temp)
                        print("ch", changed)
                        if changed:
                            self.PROPERTY[num]["value"] = value_temp

                        #print("before")
                        #print(self.PROPERTY)

                        #print("after")
                        #print(self.PROPERTY)
                    else:
                        print("Device is Busy")
                        d = {}
                        d[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                        d[smac_keys["VALUE"]] = 5
                        #client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_DEVICE_BUSY"], message=d, udp=True, tcp=False)'''

            #print(COUNTER)
            #print(COUNTER % (2*config.INTERVAL_ONLINE) )
            if(COUNTER % (config.INTERVAL_ONLINE)) == 0:
                client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_ONLINE"], message={})

            if(COUNTER %(config.INTERVAL_ONLINE*3)) == 0:
                self.send_device_info(dest_topic="#")

            if( COUNTER % 5 ) == 0:
                #print("checking RAM availability")
                #avail = gc.mem_free() / 1024
                #print("{}KB".format(avail) )
                print("MSG_COUNT_PREV", self.MSG_COUNT_PREV)
                print("MSG_COUNT", client.MSG_COUNT)
                diff = client.MSG_COUNT - self.MSG_COUNT_PREV
                self.MSG_COUNT_PREV = client.MSG_COUNT
                if diff > 30:
                    client.DEVICE_BUSY = True
                    client.UDP_REQ = []
                    client.ZMQ_REQ = []
                #if client.DEVICE_BUSY:
                    print("Device is Busy Due to Network Load")
                    d = {}
                    d[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                    d[smac_keys["VALUE"]] = 5
                    client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_DEVICE_BUSY"], message=d, udp=True, tcp=False)
                else:
                    if client.DEVICE_BUSY:
                        client.DEVICE_BUSY = False

            if(COUNTER % 10) == 0:
                print("checking topic message counts", time.localtime())
                msg_counts = config.get_topic_msg_count_all()
                with open('DEVICE/topic_msg_count.json', "w") as c2:
                    print(msg_counts)
                    for id_topic in msg_counts.keys():
                        if msg_counts[id_topic] >= 50:
                            client.block_topic(id_topic)
                            config.update_config_variable(key="blocked_topic", value=id_topic, arr_op="ADD")
                            pass
                        del msg_counts[id_topic]
                    c2.write(json.dumps(msg_counts))
                    c2.close()

                    if len(client.BLOCKED_LIST) >= 10:
                        # print block list reached
                        pass



            if(COUNTER % 60) == 0:
                print("checking triggers on time:", time.localtime())
                triggers = config.get_trigger_all()
                for trig in triggers.keys():
                    print(trig)
                    value = triggers[trig]
                    id_topic, id_context, id_device, id_property, type_trigger = trig.split(":")
                    print( smac_keys[type_trigger] )
                    if type_trigger == smac_keys["TYPE_TRIGGER_TIME"]:
                        tim = value.split(":")
                        hour = tim[0]
                        minute = tim[1]
                        #DOWLIST = tim[2].split(",")
                        DOWLIST = list(tim[2])
                        cur_time = time.localtime()
                        cur_hour = cur_time[3]
                        cur_min = cur_time[4]
                        cur_DOW = cur_time[6]
                        print("hour, min, local_hour, local_min", hour, minute, cur_hour, cur_min)
                        print("DOWLIST", DOWLIST)
                        print("CUR_DOW", cur_DOW)
                        print( DOWLIST[cur_DOW] )
                        print(hour == str(cur_hour))
                        print(minute == str(cur_min))
                        print(self.TIME_SYNC)
                        if self.TIME_SYNC and (int(hour) == cur_hour ) and (int(minute) == cur_min) and int(DOWLIST[cur_DOW]):
                            print("triggering context", id_context)
                            self.trigger_context(id_context)
                        else:
                            print("not triggered")

                    elif type_trigger == smac_keys["TYPE_TRIGGER_PROP"]:
                        print("val, local_val", value, config.PROP_INSTANCE[id_property].value())
                        if str(config.PROP_INSTANCE[id_property].value()) == str(value):
                            self.trigger_context(id_context)


            COUNTER += 1
            await asyncio.sleep(1)

    def set_property(self, id_prop, type_prop, value):
            print("TYPE_PROP", type_prop)
            print(type_prop == SMAC_PROPERTY["FAN"])
            if config.PROP_INSTANCE.get(id_prop, None) != None:
        #try:
                if type_prop == SMAC_PROPERTY["SWITCH"]:
                    #config.update_config_variable(key=id_prop, value=value)
                    if value:
                        config.PROP_INSTANCE[id_prop].on()
                    else:
                        config.PROP_INSTANCE[id_prop].off()
                    d = {}
                    d[smac_keys["ID_PROPERTY"]] = id_prop
                    d[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                    d[smac_keys["VALUE"]] = value
                    client.send_message(frm=config.ID_DEVICE, to="#", message=d, cmd=smac_keys["CMD_STATUS_SET_PROPERTY"],
                                        udp=True, tcp=True)
                    return True
                if type_prop == SMAC_PROPERTY["FAN"]:
                    print("VAL:", value)
                    config.PROP_INSTANCE[id_prop].change_speed(value)
                    d = {}
                    d[smac_keys["ID_PROPERTY"]] = id_prop
                    d[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                    d[smac_keys["VALUE"]] = value
                    client.send_message(frm=config.ID_DEVICE, to="#", message=d, cmd=smac_keys["CMD_STATUS_SET_PROPERTY"],
                                        udp=True, tcp=True)
                    return True
        #except Exception as e:
        #    print("Exception during set_property: {}".format(e) )

    def on_start(self, *args):
        print("started", args)

    def setlocaltime(self):
        from ntptime import time as tim
        t = tim()
        #import machine
        #import time

        offset = int(5.5*3600)
        #t_offset = t+offset
        tm = time.localtime(t + offset)
        print("t, tm", t, tm)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


    async def test_pins(self):
        from machine import Pin
        pins = [Pin(j, Pin.OUT) for j in [2, 4, 5, 12, 13, 14] ]
        await asyncio.sleep(1)
        while 1:
            for i in pins:
                i.on()
            await asyncio.sleep(5)
            for i in pins:
                i.off()
            await asyncio.sleep(5)


    async def subscribe_topics(self):
        await asyncio.sleep(1)
        #topics = [ t[0] for t in config.SUB_TOPIC ]
        #topics =  ["#", config.ID_DEVICE ]+ top
        while True:
            print("SUB CONNECTED: {}".format(client.ZMQ_SUB_CONNECTED) )
            if client.ZMQ_SUB_CONNECTED:
                #asyncio.run( client._subscribe('topic') )
                #await client._subscribe('topic1')
                #await client._subscribe(config.ID_DEVICE)
                client.subscribe('#')
                client.subscribe(config.ID_DEVICE)
                for t in config.SUB_TOPIC:
                   if t[0] not in ['']:
                       #await client._subscribe(t[0])
                       client.subscribe(t[0])
                       print(t[0]) 
                break
            await asyncio.sleep(1)


    async def start(self):
        import wifi_client
        if config.ID_DEVICE== "":
            #await asyncio.sleep(10)
            wifi_client.init(setup_AP=False)
            req_get_device_id()
            #wifi_ap.wlan_ap.active(True)
        else:
            import wifi_ap
            wifi_client.init(setup_AP=True)

            def handleInterrupt(timer):
                wifi_ap.wlan_ap.active(False)

            timer = machine.Timer(0)
            timer.init(period=60000, mode=machine.Timer.ONE_SHOT, callback=handleInterrupt)

        if not wifi_client.wlan.isconnected():
            mode = 2
            config.update_config_variable(key="mode", value=mode)
            machine.reset()

        #await asyncio.sleep(2)


        #topics = [ t[0] for t in config.SUB_TOPIC ]
        #client.subscribe( ["#", config.ID_DEVICE ]+topics )
        #import threading
        #th = threading.Thread(target=self.subscribe_topics, args=())
        #th.start()
        #import _thread
        #_thread.start_new_thread( self.subscribe_topics, () )
        blocked_list = config.get_config_variable(key="blocked_topic")
        if blocked_list != None:
            client.BLOCKED_LIST = blocked_list
        print(client.SUB_TOPIC)
        #client.subscribe( "D1" )
        #client.subscribe( "D2" )
        client.process_message = self.on_message
        client.on_start = self.on_start

        download_software_status = config.get_config_variable(key="download_software_status")
        if download_software_status != None:
            config.delete_config_variable(key="download_software_status")
            dest_topic = config.get_config_variable(key="download_software_requested_by")
            d = {}
            if download_software_status == "0":
                d[smac_keys["MESSAGE"]] = "No updates available"
                client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd=smac_keys["CMD_STATUS_UPDATE_SOFTWARE"], message=d, udp=True, tcp=True)
            elif download_software_status == "1":
                d[smac_keys["MESSAGE"]] = "New Updates Downloaded and Installed."
                client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd=smac_keys["CMD_STATUS_UPDATE_SOFTWARE"], message=d, udp=True, tcp=True)




        if ESP:
            try:
                #from ntptime import settime
                print("before internet time", time.localtime())
                self.setlocaltime()
                print("after internet time", time.localtime())
                self.TIME_SYNC = True
                #print("TIME SET", time.localtime())
            except Exception as e:
                print("Internet Time not Set", e)
                self.TIME_SYNC = False
            with open("DEVICE/device.json", "r") as f:
                try:
                    f1 = json.loads(f.read())
                    self.PROPERTY = f1
                    for p in f1:
                        #print(p)
                        id_prop = p["id_property"]
                        type_prop = p["type_property"]
                        #instance = p["instance"]
                        ip_pin = p["pin_input"]
                        if(ip_pin != None) and (ip_pin != ""):
                            ip_pin = ip_pin.split(",")
                        op_pin = p["pin_output"]
                        op_pin = op_pin.split(",")
                        pre_val = config.get_config_variable("{}".format(id_prop))
                        pre_val = 0 if(pre_val == None) else pre_val
                        config.update_config_variable(key=id_prop+"_time", value=time.time())
                        config.PROP_TYPE[id_prop] = type_prop
                        print("prevel: {}".format(pre_val))
                        if type_prop == SMAC_PROPERTY["FAN"]:
                            #config.PROP["{}:{}".format(prop, instance)] = Fan( input=ip_pin[0], output=op_pin, value=pre_val )
                            config.PROP_INSTANCE[id_prop] = SmacFan( input_pin=ip_pin[0], output=op_pin, value=pre_val, id_property=id_prop )
                        elif type_prop == SMAC_PROPERTY["SWITCH"]:
                            #config.PROP["{}:{}".format(prop, instance)] = Switch( input=ip_pin[0], output=op_pin[0], value=pre_val )
                            config.PROP_INSTANCE[id_prop] = SmacSwitch( input_pin=ip_pin[0], output=op_pin[0], value=pre_val, id_property=id_prop )
                        #time.sleep(.1)
                        #await  asyncio.sleep(.1)
                    print(config.PROP_INSTANCE)

                    '''from machine import Pin
                    from debounce import Pushbutton
                    reset_pin = Pin(self.RESET_BUTTON, Pin.IN, Pin.PULL_UP)
                    p1 = Pushbutton(reset_pin)
                    p1.double_func(self.on_dbl_click, ())
                    p1.long_func(self.on_long_press, ())'''

                except Exception as e:
                    print("error ip config: {}".format(e))


        #t1 = asyncio.ensure_future( self.send_test() )
        #t2 = asyncio.ensure_future( client.main() )


        if ESP:
            self.send_device_info(dest_topic="#")
            t3 = asyncio.create_task(self.subscribe_topics())
            t1 = asyncio.create_task(client.main())
            t2 = asyncio.create_task(self.interval())
            t4 = asyncio.create_task(self.interval2())
            #t3 = asyncio.create_task(self.test_pins())
            await t4
            await t3
            await t2
            await t1
            #asyncio.gather( self.interval(), client.main())
        else:
            #import threading
            #t1 = threading.Thread( self.send_test() )
            #t1.start()
            asyncio.gather( client.main(), self.send_test())

cli = smacInit()

asyncio.run( cli.start() )
#cli.start()

#asyncio.gather( cli.start(), cli.send_test() )
