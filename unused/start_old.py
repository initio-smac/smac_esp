import config
config.update_config_vars()

import wifi_client

from client import mqttTest
import urequests
import utime
import machine
from machine import Timer
import ujson as json
import gc
from machine import Pin
from debounce import DebouncedSwitch
#from pin_custom import PinCustom as Pin
import mqtt_keys
import os
import _thread



gc.enable()

utime.sleep(2)


SMAC_SERVER = "https://smacsystem.com/smacapi/"
#SMAC_SERVER = "https://reqres.in/api/products/3"
REQ_HEADERS = {'Accept': 'application/json',
               'content-type': 'application/json'
               }

IP_OP_MAP = {}
DBOUNCE = {}
D_COUNTER = 0


def get_password(username):
    try:
        print(username)
        #print(datetime.now(tz=timezone.utc))
        date_now = machine.RTC().datetime()
        dt = utime.mktime(date_now)
        du = username.replace("D_", "")
        du = int("0x{}".format(du), 0)
        password = dt - du

        print(password)
        return str(password)
    except Exception as e:
        print("get password err: {}".format(e) )


def rest_call(url, method, request, data=None, json=None, headers=REQ_HEADERS ):
    try:
        if request == "request_device_uid":
            headers['Authorization'] = 'smac:smac1'

        if config.DEVICE_ID != "":
            username = config.DEVICE_ID
            password = get_password(username)
            headers['Authorization'] = '{}:{}'.format(username, password)

        req = urequests.request(method, url, data=data, json=json, headers=headers)
        res = req.text
        
        print(res)
        print(type(res))
        import json
        print(json)
        r = json.loads(res)
        print(r)
        #r = res
        if request == "request_device_uid":
            d = r["device_id"]
            config.update_config_file(key="device_id", value=d)
            config.update_config_file(key="topics", value=d)
            config.update_config_file(key="device_name", value="smac_{}".format(d))
            config.update_config_vars()
            mqttTest.client.set_callback(mqttTest.on_receive)
            mqttTest.client.subscribe(d.encode('ascii'))
        req.close()
    except Exception as e:
        print("urequests error: {}".format(e) )

def get_device_id():
    request = "request_device_uid"
    url = SMAC_SERVER + request
    rest_call(url=url, method="GET", request=request )

def reset_counter(*args):
    global D_COUNTER
    D_COUNTER = 0

def ip_handler(*args):
    try:
        global D_COUNTER
        D_COUNTER += 1
        if D_COUNTER > 1:
           config.update_config_file(key="mode", value=1)
           utime.sleep(1)
           machine.reset()
        tim = Timer(4)                                
        tim.init(mode=Timer.ONE_SHOT, callback=reset_counter, period=1000)                    
        print(args)
        arr = args[0]
        #ip = args[0]
        #print("ip_pin: {}".format(ip) )
        #val = config.PROP_IP["{}".format(ip)]
        #prop, instance = val.split(":")
        #op_pin = config.PROP[val]
        op_pin = arr[1]
        ip_pin = arr[0]
        prop = arr[2]
        instance = arr[3]
        print("op_pin: {}".format(op_pin) )
        print("ip_pin: {}".format(ip_pin) )
        if prop == "switch_power":
            v = 1 - op_pin.value()
            op_pin.value(v)
            dat1 = {}
            dat1["property"] = prop
            dat1["value"] = v
            dat1["instance"] = instance
            config.update_config_file(key="{}:{}".format(prop, instance), value=v)
            for group in config.TOPICS:
                mqttTest.publish(frm=config.DEVICE_ID, to=group, command=mqtt_keys.CMD_STATUS, data=dat1)
    except Exception as e:
        print("ip handler err: {}".format(e))

if config.DEVICE_ID == "":
    get_device_id()

with open("device.json", "r") as f:
    try:
        f1 = json.loads(f.read())
        for p in f1:
            #print(p)
            prop = p["property"]
            instance = p["instance"]
            ip_pin = p["input_pin"]
            ip_pin = ip_pin.split(",")
            op_pin = p["pin"]
            op_pin = op_pin.split(",")
            if prop == "fan_speed":
                config.PROP["{}:{}".format(prop, instance)] = [ Pin(int(i), Pin.OUT, value=0) for i in op_pin ]
            else:
                #print("ip_pin_config: {}".format(ip_pin))
                #print("op_pin_config: {}".format(op_pin))
                #print("instance: {}".format(instance))
                pre_val = config.get_config_file("{}:{}".format(prop, instance))
                op_instance = Pin(int(op_pin[0]), Pin.OUT, value=int(pre_val)) 
                print("prevel: {}".format(pre_val))
                #if(pre_val != None) and (pre_val != ""):
                #    op_instance.value(int(pre_val))
                config.PROP["{}:{}".format(prop, instance)] = op_instance
                ip_instance = Pin(int(ip_pin[0]), Pin.IN, Pin.PULL_UP) 
                config.PROP_IP[ "{}".format(ip_instance) ] = "{}:{}".format(prop, instance)
                #IP_OP_MAP["{}".format(ip_pin[0])] = config.PROP["{}:{}".format(prop, instance)]
                #ip_instance.irq(handler=ip_handler, trigger=Pin.IRQ_FALLING)
                # args --> input_pin, input_handler, output_pin
                DebouncedSwitch(ip_instance, ip_handler, arg=( ip_pin, op_instance, prop, instance) )
    except Exception as e:
        print("error ip config: {}".format(e))


group_id = "D_1bc.G_1604037091"
def send_group_request():
    device_name = os.uname()[1]
    data = {}
    data["data"] = {'device_name': device_name}
    mqttTest.publish(frm=config.DEVICE_ID, to=group_id, command=mqtt_keys.CMD_REQ_ADD_TO_GROUP, data=data)

def dir_exists(path, dir):
    arr = os.listdir(path)
    return (dir in arr)

def check_connection(*args):
    url = "https://smacsystem.com/download/esp32/version.json"
    req = urequests.get(url)
    req.close()
    if req.status_code == 200:
        return True
    else:
        return False

#print(utime.time())
#while not check_connection():
#    pass
#print(utime.time())
gc.collect()

try:
    DOWNLOAD_VERSION = config.get_config_file("download_version")
    config_old = {}
    invalid_version = [ "", None, "0", 0 ]
    with open('config.json', "r") as c1:
        config_old = json.load(c1)
        c1.close()
    
    if (DOWNLOAD_VERSION not in invalid_version):
        print("checking internet connection...")
        while not check_connection():
            pass
        print("downloading version: {}".format(DOWNLOAD_VERSION))
        url = "https://smacsystem.com/download/esp32/{}/files.json".format(DOWNLOAD_VERSION)
        print(url)
        req = urequests.get(url)
        res = req.json()
        req.close()
        print(res)
        for f in res.keys():
            print("downloading file: {}, path: {}".format(f, res[f]))
            path = res[f]
            d_paths = path.split("/")
            
            if d_paths[0] != "":
                print(d_paths)
                try:
                    print("creating dir : {}".format(d_paths[0]) )
                    os.mkdir(d_paths[0])
                except Exception as e:
                    print(e)
                if len(d_paths) > 1:
                    for num, i in enumerate(d_paths):
                        #print(num)
                        #print(len(d_paths)-1)
                        if num < len(d_paths)-1:
                            try:
                                print("creating dir : {}/{}".format(i, d_paths[num+1]) )
                                os.mkdir("/{}/{}".format(i, d_paths[num+1]))
                            except Exception as e:
                                print(e)
                print(path)
                u = "https://smacsystem.com/download/esp32/{}/{}/{}".format(DOWNLOAD_VERSION, path, f)
            else:
                u = "https://smacsystem.com/download/esp32/{}/{}".format(DOWNLOAD_VERSION, f)
            #url_path = "{}/{}".format(path,f)
            
            print(u)
            req1 = urequests.get(u)
            res1 = req1.text
            if req1.status_code == 200:
                with open("{}/{}".format(path, f), "w" ) as f:
                    f.write(res1)
            req1.close()
            
            #print(res1)
            
        # update the variables
        try:
            print("updating new config file")
            con = {}
            with open('config.json', "r") as c1:
                con = json.load(c1)
                c1.close()

            with open('config.json', "w") as c2:
                d = con.copy()
                if d.get("download_version", None) != None:
                    del d["download_version"]
                d["version"] = DOWNLOAD_VERSION
                d["topics"] = config_old["topics"]
                d["device_id"] = config_old["device_id"]
                d["device_name"] = config_old["device_name"]
                d["device_id"] = config_old["device_id"]
                d["mqtt_server"] = config_old["mqtt_server"]
                d["ap_config"] = config_old["ap_config"]
                d["wifi_config_1"] = config_old["wifi_config_1"]
                d["wifi_config_2"] = config_old["wifi_config_2"]
                d["mode"] = 0
                print(d)
                c2.write(json.dumps(d))
                c2.close()
        except Exception as e:
            print("update config file err: {}".format(e))
        gc.collect()
        print("\nSuccessfully downloaded version: {}\nRebooting...".format(DOWNLOAD_VERSION))
        machine.reset()
                
    else:
        url = "https://smacsystem.com/download/esp32/version.json"
        req = urequests.get(url)
        res = req.json()
        req.close()
        #print(res)
        ver = res.get("versions", [])
        if len(ver) > 0:
            config.update_config_file("versions", value=ver)
except Exception as e:
    print(e)

_thread.start_new_thread(mqttTest.connect, ())

#mqttTest.connect()
utime.sleep(5)
#send_group_request()




