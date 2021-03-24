from smac_device_keys import SMAC_DEVICES, SMAC_PROPERTY
import json

class Config():
    PROPERTY = []
    PROP_INSTANCE = {}
    WIFI_CONFIG = {}
    AP_CONFIG = {}
    SUB_TOPIC = []
    ID_DEVICE = ""
    NAME_DEVICE = "smac_esp"
    TYPE_DEVICE = SMAC_DEVICES["ESP"]
    PIN_DEVICE = "1234"
    VERSION = "DEFAULT"

    def load_config_variable(self):
        try:
            with open('config.json', "r") as c:
                config = json.load(c)
                self.WIFI_CONFIG = config['WIFI_CONFIG']
                self.AP_CONFIG = config['AP_CONFIG']
                self.SUB_TOPIC = config["SUB_TOPIC"]
                self.ID_DEVICE = config["ID_DEVICE"]
                self.NAME_DEVICE = config["NAME_DEVICE"]
                self.TYPE_DEVICE = SMAC_DEVICES["ESP"]
                self.VERSION = config.get("VERSION", "01")
                self.PIN_DEVICE = config.get("PIN_DEVICE", "1234")
                #global MODE
                #print(config.get("mode"))
                #MODE = config.get("mode", 0)
                c.close()

        except Exception as e:
            print("update config vars err:{}".format(e) )

    def get_config_variable(self, key):
        try:
            with open('config.json', "r") as c1:
                config = json.load(c1)
                c1.close()
                return config.get(key, 0)
        except Exception as e:
            print("get config file err:{}".format(e) )

    # arr_op = [ ADD, REM]
    def update_config_variable(self, key, value, arr_op="ADD"):
        try:
            config = {}
            with open('config.json', "r") as c1:
                config = json.load(c1)
                c1.close()

            with open('config.json', "w") as c2:
                d = config.copy()
                #print(d)
                if (key == "SUB_TOPIC") and (arr_op == "ADD"):
                    if not(value in d[key]):
                        d[key] = d[key] + [value]
                elif (key == "SUB_TOPIC") and (arr_op == "REM"):
                    if value in d[key]:
                        d[key].remove(value)
                else:
                    d[key] = value
                #print(d)
                c2.write(json.dumps(d))
                c2.close()
        except Exception as e:
            print("update config file err: {}".format(e))

    def delete_config_variable(self, key):
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

config = Config()