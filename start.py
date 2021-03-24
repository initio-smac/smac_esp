import json
import time

try:
    from machine import Timer
    import uasyncio as asyncio
    import wifi_client2
    from smac_devices import Fan, Switch
    ESP = True
except:
    import asyncio
    ESP = False



from config import config
config.load_config_variable()


from smac_client import client
from smac_requests import req_get_device_id
from smac_keys import smac_keys
from smac_platform import SMAC_PLATFORM
from smac_device_keys import SMAC_DEVICES, SMAC_PROPERTY

class smacInit():
    SENDING_INFO = 0


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
        topics.remove( "#" )
        topics.remove( config.ID_DEVICE )
        topics.append( '')
        print(topics)
        print(dest_topic)
        client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd= smac_keys["CMD_INIT_SEND_INFO"], message={}, udp=True, tcp=False)
        for t in topics:
            m = {}
            m[ smac_keys["ID_TOPIC"] ] = t
            m[ smac_keys["NAME_TOPIC"]] = ""
            m[ smac_keys["NAME_DEVICE"]] = config.NAME_DEVICE
            m[ smac_keys["TYPE_DEVICE"]] = config.TYPE_DEVICE
            m[ smac_keys["ID_DEVICE"]] = config.ID_DEVICE
            print(m)
            client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd=smac_keys["CMD_SEND_INFO"], message=m, udp=True, tcp=False)
            print("sent {}".format(t))
        print("send topics")

        for p in self.PROPERTY:
            print(p)
            p1 = {}
            p1[ smac_keys["ID_DEVICE"] ] = config.ID_DEVICE
            p1[ smac_keys["ID_PROPERTY"] ] = p["id_property"]
            p1[ smac_keys["TYPE_PROPERTY"] ] = p["type_property"]
            p1[ smac_keys["NAME_PROPERTY"] ] = p["name_property"]
            p1[ smac_keys["VALUE"]] = p["value"]
            p1[ smac_keys["VALUE_MIN"]] = p["value_min"]
            p1[ smac_keys["VALUE_MAX"]] = p["value_max"]
            client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd=smac_keys["CMD_SEND_INFO"], message=p1, udp=True, tcp=False)
        print("send property")

        self.SENDING_INFO = 0
        client.send_message(frm=config.ID_DEVICE, to=dest_topic, cmd=smac_keys["CMD_END_SEND_INFO"], message={},
                            udp=True, tcp=False)

    def add_topic(self, frm, id_topic, name_home, name_topic, id_device, passkey, *args):
        if str(passkey) == str(config.PIN_DEVICE):
            config.update_config_variable(key='SUB_TOPIC', value=id_topic, arr_op="ADD")
            client.subscribe(id_topic)
            d = {}
            d[ smac_keys["ID_TOPIC"] ] = id_topic
            d[ smac_keys["NAME_DEVICE"]] = config.NAME_DEVICE
            d[ smac_keys["TYPE_DEVICE"]] = config.TYPE_DEVICE
            d[ smac_keys["NAME_HOME"]] = name_home
            d[ smac_keys["NAME_TOPIC"]] = name_topic
            client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_STATUS_ADD_TOPIC"], message=d, udp=True, tcp=False)
            # sending ACK
            d1 = {}
            d1[ smac_keys["MESSAGE"] ] = "Topic subscribed successfylly"
            print("subscribed topic: {}".format(id_topic))
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Topic '{}' not subscribed".format(id_topic)
            d1[smac_keys["ID_DEVICE"]] = id_device
            d1[smac_keys["ID_TOPIC"]] = id_topic
            print("Cannot subscribe to {}. Passkey error.".format(id_topic))
            if config.ID_DEVICE == frm:
                print("same device")
            else:
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"], message=d1, udp=True, tcp=False)
                #client.send_message(frm=config.ID_DEVICE, to=id_topic, cmd=smac_keys["CMD_INVALID_PIN"], message=d1)

    def delete_topic(self, frm, id_topic, id_device, passkey, *args):
        print(passkey)
        print(config.PIN_DEVICE)
        print(passkey == config.PIN_DEVICE)
        #print(type(passkey))
        #print(type(config.PIN_DEVICE))
        if str(passkey) == str(config.PIN_DEVICE):
            #db.add_network_entry(name_topic=id_topic, id_topic=id_topic, id_device=id_device, name_device=self.NAME_DEVICE, type_device=self.TYPE_DEVICE)
            #db.delete_network_entry_by_topic(id_topic, id_device)
            config.update_config_variable(key='SUB_TOPIC', value=id_topic, arr_op="REM")
            client.unsubscribe(id_topic)
            #self.delete_topic_widget(id_topic)
            d = {}
            d[ smac_keys["ID_TOPIC"] ] = id_topic
            d[ smac_keys["NAME_DEVICE"]] = config.NAME_DEVICE
            d[ smac_keys["TYPE_DEVICE"]] = config.TYPE_DEVICE
            client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_STATUS_REMOVE_TOPIC"], message=d, udp=True, tcp=False)
            # sending ACK
            d1 = {}
            d1[ smac_keys["MESSAGE"] ] = "Topic unsubscribed successfylly"
            print("unsubscribed topic: {}".format(id_topic))
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Topic '{}' not unsubscribed".format(id_topic)
            d1[smac_keys["ID_DEVICE"]] = id_device
            d1[smac_keys["ID_TOPIC"]] = id_topic
            print("Cannot unsubscribe to {}. Passkey error.".format(id_topic))
            if config.ID_DEVICE == frm:
                print("same device")
            else:
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"], message=d1, udp=True, tcp=False)


    def on_message(self, topic, message, protocol, *args):
        print(args)
        try:
            print( "{}, {}, {}".format(topic, message, protocol) )
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

            if frm != config.ID_DEVICE:
                if cmd == smac_keys["CMD_SET_PROPERTY"]:
                    #print("3")
                    id_prop = msg.get( smac_keys["ID_PROPERTY"], None)
                    type_prop = msg.get( smac_keys["TYPE_PROPERTY"], None)
                    #instance = data.get( smac_keys["INSTANCE"], None )
                    value = msg.get( smac_keys["VALUE"], 0 )
                    #print("4")
                    if type_prop == SMAC_PROPERTY["SWITCH"]:
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





        except Exception as e:
            print("Exception while decoding message: {}".format(e) )
            raise e


    async def interval(self):
        await asyncio.sleep(0)
        while 1:
            #print(self.PROPERTY)
            for num, prop in enumerate(self.PROPERTY):
                value = prop["value"]
                id_prop = prop["id_property"]
                type_prop = prop["type_property"]
                value_temp = config.get_config_variable(key=id_prop)
                #print(prop)
                #print(value)
                #print(value_temp)
                if value_temp != value:
                    lastUpdated_time = config.get_config_variable(key=str(id_prop) + "_time")
                    t_diff = time.time() - lastUpdated_time
                    print("t_diff", t_diff)
                    if t_diff > .5:
                        self.set_property(id_prop, type_prop, value_temp)

                        #print("before")
                        #print(self.PROPERTY)
                        self.PROPERTY[num]["value"] = value_temp
                        #print("after")
                        #print(self.PROPERTY)
                    else:
                        print("Device is Busy")
                        d = {}
                        d[smac_keys["ID_DEVICE"]] = config.ID_DEVICE
                        d[smac_keys["VALUE"]] = 5
                        #client.send_message(frm=config.ID_DEVICE, to="#", cmd=smac_keys["CMD_DEVICE_BUSY"], message=d, udp=True, tcp=False)

                
            await asyncio.sleep(.1)

    def set_property(self, id_prop, type_prop, value):
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
                                udp=True, tcp=False)

    async def start(self):
        if config.ID_DEVICE== "":
            req_get_device_id()

        time.sleep(2)
        client.subscribe( ["#", "D1"] )
        print(client.SUB_TOPIC)
        #client.subscribe( "D1" )
        #client.subscribe( "D2" )
        client.process_message = self.on_message


        if ESP:
            with open("device.json", "r") as f:
                try:
                    f1 = json.loads(f.read())
                    self.PROPERTY = f1
                    for p in f1:
                        #print(p)
                        id_prop = p["id_property"]
                        type_prop = p["type_property"]
                        #instance = p["instance"]
                        ip_pin = p["pin_input"]
                        ip_pin = ip_pin.split(",")
                        op_pin = p["pin_output"]
                        op_pin = op_pin.split(",")
                        pre_val = config.get_config_variable("{}".format(id_prop))
                        config.update_config_variable(key=id_prop+"_time", value=time.time())
                        print("prevel: {}".format(pre_val))
                        if type_prop == SMAC_PROPERTY["FAN"]:
                            #config.PROP["{}:{}".format(prop, instance)] = Fan( input=ip_pin[0], output=op_pin, value=pre_val )
                            config.PROP_INSTANCE[id_prop] = Fan( input=ip_pin[0], output=op_pin, value=pre_val )
                        elif type_prop == SMAC_PROPERTY["SWITCH"]:
                            #config.PROP["{}:{}".format(prop, instance)] = Switch( input=ip_pin[0], output=op_pin[0], value=pre_val )
                            config.PROP_INSTANCE[id_prop] = Switch( input=ip_pin[0], output=op_pin[0], value=pre_val )
                except Exception as e:
                    print("error ip config: {}".format(e))


        #t1 = asyncio.ensure_future( self.send_test() )
        #t2 = asyncio.ensure_future( client.main() )


        if ESP:

            t1 = asyncio.create_task(client.main())
            t2 = asyncio.create_task(self.interval())
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
