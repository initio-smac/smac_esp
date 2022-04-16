import json
import machine
import time
import gc
gc.enable()
import uasyncio as asyncio

from DEVICE.smac_devices import SmacFan, SmacSwitch
from DEVICE.smac_device_keys import SMAC_DEVICES, SMAC_PROPERTY
from DEVICE.config import config
config.load_config_variable()

RESET_BUTTON = 26
PROPERTY = {}

try:
    #import DEVICE.config as cn
    import _thread
    import blink
    _thread.start_new_thread(blink.device_boot_blink_led, ())
except:
    pass


def set_internet_time():
    try:
        import ntptime
        ntptime.settime()
        import time
        print(time.localtime())
    except:
        pass

# on double click,
# change the mode restart in web AP mode
def on_dbl_click(*args):
    # mode = 2
    mode = config.get_config_variable(key="mode")
    mode = 2 if(mode == 0) else 0
    config.update_config_variable(key="mode", value=mode)
    machine.reset()


# on long press,
# reset the device to default code
def on_long_press(*args):
    from web_server_async import copy_folder
    print("Resetting to Default Version...")
    copy_folder(COPY_FROM="DEFAULT", COPY_TO="DEVICE")
    config.update_config_variable(key="mode", value=0)
    machine.reset()

async def my_app():
    await asyncio.sleep(1)
    while 1:
        await asyncio.sleep(1)


def init_reset_func():
    from machine import Pin
    from debounce import Pushbutton, Switch
    ip = Pin(RESET_BUTTON, Pin.IN, Pin.PULL_UP)
    ip_type = config.get_config_variable("input_type")
    print("ip type", ip_type)
    if( ip_type == "pushbutton" ):
        rs = Pushbutton(ip)
    else:
        rs = Switch(ip)
    rs.pattern_fn = on_dbl_click
    rs.pattern_args = ()
    #rs.double_func(on_dbl_click, ())
    #rs.long_func(on_long_press, ())

    with open("DEVICE/device.json", "r") as f:
        try:
            f1 = json.loads(f.read())
            PROPERTY = f1
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
            
        except Exception as e:
            print("exception while defining Pins ", e)
        gc.collect()
        f.close()

async def interval2():
    await asyncio.sleep(0)
    while 1:
        for num, prop in enumerate(PROPERTY):
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
                    PROPERTY[num]["value"] = value_temp

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
        await asyncio.sleep(0)

async def start_web_server():
    import web_server_async
    #t1 = asyncio.create_task(interval2())
    t2 = asyncio.create_task( web_server_async.start_server() )
    #await t1
    await t2

async def start_smac_client():
    from DEVICE.start import cli
    t1 = asyncio.create_task(interval2())
    t2 = asyncio.create_task( cli.start() )
    await t1
    await t2

# run functions
MODE = config.MODE
print("MODE", MODE)
init_reset_func()
#MODE = 2
if MODE == 3:
    import wifi_ap
    wifi_ap.wlan_ap.active(True)
    print("Webrepl Mode")
elif MODE == 0:
    # import wifi_ap
    # import wifi_client
    # wifi_client.init(setup_AP=False)
    # set_internet_time()
    try:
        asyncio.run( start_smac_client() )
    except Exception as e:
        print("Exception while initiating APP", e)
        asyncio.run(my_app())
elif MODE == 2:
    #import wifi_ap
    import wifi_client
    wifi_client.init(setup_AP=True)
    asyncio.run( start_web_server() )
    #web_server.start_server()
    try:
        #asyncio.run( start_web_server() )
        pass
    except Exception as e:
        print("Exception while initiating APP", e)
        #import uasyncio as asyncio
        asyncio.run(my_app())
    '''from urequests import request
    resp = request(method="GET", url="https://smacsystem.com/download/esp32/version.json")
    print("resp")
    print(resp.json())'''

'''elif MODE == 1:
    import wifi_client
    wifi_client.init()
    from smac_ota import smacOTA
    print("Checking For Updates")
    cur_version = config.get_config_variable(key="version")
    new_version = smacOTA.get_update_version(cur_version)
    if (new_version != -1):
        print("New Updates Available")
        print("Initiating Update Software")
        smacOTA.download_update(version=new_version)
    else:
        print("No Updates Available")
        config.update_config_variable(key="mode", value=0)
        #import machine
        machine.reset()'''
