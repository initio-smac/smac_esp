import json
from smac_device_keys import SMAC_DEVICES


#WIFI_CONFIG_DEFAULT = {"ssid": "admin", "password": "password"}
#WIFI_CONFIG_1 = {}
#WIFI_CONFIG_2 = {}
#MQTT_SERVER = "smacsystem.com"
SUB_TOPIC = []
ID_DEVICE = ""
NAME_DEVICE = "smac_esp32"
TYPE_DEVICE = SMAC_DEVICES["ESP"]
VERSION = "01"
MODE = 0

PROP = {}

def load_config_variable():
    try:
        with open('config.json', "r") as c:
            config = json.load(c)
            c.close()

    except Exception as e:
        print("update config vars err:{}".format(e) )

'''def load_config_variable():
    try:
        with open('config.json', "r") as c:
            config = json.load(c)
            global WIFI_CONFIG_1
            WIFI_CONFIG_1 = config['wifi_config_1']
            global WIFI_CONFIG_2
            WIFI_CONFIG_2 = config['wifi_config_2']
            global AP_CONFIG
            AP_CONFIG = config['ap_config']
            #global MQTT_SERVER
            #MQTT_SERVER = config["mqtt_server"]
            global TOPICS
            TOPICS = config["topics"]
            global DEVICE_ID
            DEVICE_ID = config["id_device"]
            global DEVICE_NAME
            DEVICE_NAME = config["name_device"]
            global VERSION
            VERSION = config.get("version", "01")
            global MODE
            print(config.get("mode"))
            MODE = config.get("mode", 0)
            c.close()

    except Exception as e:
        print("update config vars err:{}".format(e) )'''

def get_config_variable(key):
    try:
        with open('config.json', "r") as c1:
            config = json.load(c1)
            c1.close()
            return config.get(key, 0)
    except Exception as e:
        print("get config file err:{}".format(e) )

# arr_op = [ ADD, REM]
def update_config_variable(key, value, arr_op="ADD"):
    try:
        config = {}
        with open('config.json', "r") as c1:
            config = json.load(c1)
            c1.close()

        with open('config.json', "w") as c2:
            d = config.copy()
            print(d)
            if (key == "SUB_TOPIC") and (arr_op == "ADD"):
                if not(value in d[key]):
                    d[key] = d[key] + [value]
            elif (key == "SUB_TOPIC") and (arr_op == "REM"):
                if value in d[key]:
                    d[key].remove(value)
            else:
                d[key] = value
            print(d)
            c2.write(json.dumps(d))
            c2.close()
    except Exception as e:
        print("update config file err: {}".format(e))

def delete_config_variable(key):
    try:
        config = {}
        with open('config.json', "r") as c1:
            config = json.load(c1)
            c1.close()

        with open('config.json', "w") as c2:
            d = config.copy()
            del d[key]
            c2.write(json.dumps(d))
            c2.close()
    except Exception as e:
        print("delete config file err: {}".format(e))
