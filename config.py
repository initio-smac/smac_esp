from smac_device_keys import SMAC_DEVICES
import json

class Config():
    PROPERTY = []
    PROP_INSTANCE = {}
    WIFI_CONFIG_1 = {}
    WIFI_CONFIG_2 = {}
    AP_CONFIG = {}
    SUB_TOPIC = []
    ID_DEVICE = ""
    NAME_DEVICE = "smac_esp"
    TYPE_DEVICE = SMAC_DEVICES["ESP"]
    PIN_DEVICE = "1234"
    VERSION = "02"
    MODE = 0
    DOWNLOAD_VERSION = None
    INTERVAL_ONLINE = 30
    LIMIT = {
        "LIMIT_DEVICE": 10,
        "LIMIT_TOPIC": 10
    }

    def load_config_variable(self):
        try:
            with open('config.json', "r") as c:
                config = json.load(c)
                self.WIFI_CONFIG_1 = config['wifi_config_1']
                self.WIFI_CONFIG_2 = config['wifi_config_2']
                self.AP_CONFIG = config['ap_config']
                self.SUB_TOPIC = config["sub_topic"]
                self.ID_DEVICE = config["id_device"]
                self.NAME_DEVICE = config["name_device"]
                self.TYPE_DEVICE = SMAC_DEVICES["ESP"]
                self.VERSION = config.get("version", "01")
                self.PIN_DEVICE = config.get("pin_device", "1234")
                self.MODE = config.get("mode", 0)
                self.DOWNLOAD_VERSION = config.get("download_version")
                self.INTERVAL_ONLINE = config.get("interval_online")
                self.LIMIT["LIMIT_DEVICE"] = config.get("limit_device", 10)
                self.LIMIT["LIMIT_TOPIC"] = config.get("limit_topic", 10)

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
                return config.get(key, None)
        except Exception as e:
            print("get config file err:{}, key:{}".format(e, key) )
            return None

    # arr_op = [ ADD, REM]
    def update_config_variable(self, key, value, arr_op="ADD", reload_variables=False):
        try:
            config = {}
            with open('config.json', "r") as c1:
                config = json.load(c1)
                c1.close()

            with open('config.json', "w") as c2:
                d = config.copy()
                #print(d)
                if (key == "sub_topic") and (arr_op == "ADD"):
                    if not(value[0] in  [ topic[0] for topic in d[key] ]):
                        d[key] = d[key] + [value]
                elif (key == "sub_topic") and (arr_op == "REM"):
                    for topic in d[key]:
                        if value == topic[0]:
                            d[key].remove(topic)
                else:
                    d[key] = value
                #print(d)
                c2.write(json.dumps(d))
                c2.close()
            if reload_variables:
                self.load_config_variable()
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
                if key in config.keys():
                    del d[key]
                    c2.write(json.dumps(d))
                    c2.close()
        except Exception as e:
            print("delete config file err: {}".format(e))

    def update_name_property(self, id_property, name_property):
        try:
            props = {}
            with open('device.json', "r") as c1:
                props = json.load(c1)
                c1.close()

            with open('device.json', "w") as c2:
                d = props.copy()
                for num, prop in enumerate(d):
                    if prop["id_property"] == id_property:
                        d[num]["name_property"] = name_property
                c2.write(json.dumps(d))
                c2.close()
        except Exception as e:
            print("update config file err: {}".format(e))

config = Config()
