from DEVICE.smac_device_keys import SMAC_DEVICES
import json



class Config():
    PROPERTY = []  # property properties data(json)
    PROP_INSTANCE = {} # stores property objects for controlling
    PROP_TYPE = {} # stores property type of each properties
    
    DATA = {
    	"mode": 0,
    	"wifi_config_1" : {},
    	"ap_config": {},
    	"sub_topic": [],
    	"blocked_topic": [],
    	"name_device": "smac_",
    	"pin_device": "1234",
    	"input_type": "switch",
    	"interval_online": 30
    }
    TYPE_DEVICE = SMAC_DEVICES["ESP"],
    #DOWNLOAD_VERSION = None
    #INTERVAL_ONLINE = 30
    
    VERSION = "02"
    ID_DEVICE = ""
    LIMIT = {
        "limit_property": 4,
        "limit_topic": 5,
        "liit_action": 5,
        "limit_trigger": 5
    }

    def load_config_variable(self):
        try:
            with open('DEVICE/id_device.txt', "r") as d:
                self.ID_DEVICE = d.read()
                d.close()
        except Exception as e:
            print("Cant read id_device.txt : ", e)

        try:
            with open('DEVICE/version.txt', "r") as v:
                self.VERSION = v.read()
                v.close()
        except Exception as e:
            print("Cant read version.txt : ", e)

        try:
            with open('DEVICE/limits.json', "r") as l:
                self.LIMIT = json.load(l)
                #self.LIMIT["LIMIT_PROPERTY"] = limits.get("limit_property", 4)
                #self.LIMIT["LIMIT_TOPIC"] = limits.get("limit_topic", 5)
                #self.LIMIT["LIMIT_ACTION"] = limits.get("limit_action", 5)
                #self.LIMIT["LIMIT_TRIGGER"] = limits.get("limit_trigger", 5)
                l.close()
        except Exception as e:
            print("Cant read id_device.txt : ", e)

        try:
            with open('DEVICE/config.json', "r") as c1:
                self.DATA = json.load(c1)
                c1.close()

        except Exception as e:
            print("load config vars err:{}".format(e) )


    def get_config_variable(self, key):
        try:
            with open('DEVICE/config.json', "r") as c1:
                config = json.load(c1)
                c1.close()
                return config.get(key, None)
        except Exception as e:
            print("get config err:{}, key:{}".format(e, key) )
            return None

    def update_version(self, value):
        try:
            with open('DEVICE/version.txt', "w") as c1:
                c1.write(value)
                self.VERSION = value
                c1.close()
                return 
        except Exception as e:
            print("get config err:{}, key:{}".format(e, key) )
            return None

    def get_property_value(self, id_prop):
        try:
            with open('DEVICE/property_value.json', "r") as c1:
                props = json.load(c1)
                c1.close()
                return props.get(id_prop, None)
        except Exception as e:
            print("get config err:{}, key:{}".format(e, key) )
            return None

    def update_property_value(self, id_prop, value):
        try:
            props = {}
            with open('DEVICE/property_value.json', "r") as c1:
                props = json.load(c1)
                c1.close()

            props[id_prop] = value
            with open('DEVICE/property_value.json', "w") as c2:
                c2.write( json.dumps(props) )
                c2.close()
        except Exception as e:
            print(e) 

    def update_property_value_all(self):
        try:
            props = {}
            for id_prop in self.PROP_INSTANCE:
                props[id_prop] = self.PROP_INSTANCE[id_prop].value()
            with open('DEVICE/property_value.json', "w") as c2:
                c2.write( json.dumps(props) )
                c2.close()
        except Exception as e:
            print(e) 

    # arr_op = [ ADD, REM]
    def update_config_variable(self, key, value, arr_op="ADD", reload_variables=False):
        try:
            config = self.DATA
            #with open('DEVICE/config.json', "r") as c1:
            #    config = json.load(c1)
            #    c1.close()

            with open('DEVICE/config.json', "w") as c2:
                d = config.copy()
                #print(d)
                if (key == "sub_topic") and (arr_op == "ADD"):
                    if not(value[0] in  [ topic[0] for topic in d[key] ]):
                        d[key] = d[key] + [value]
                        #self.SUB_TOPIC = d[key]
                elif (key == "sub_topic") and (arr_op == "REM"):
                    for topic in d[key]:
                        if value == topic[0]:
                            d[key].remove(topic)
                    #self.SUB_TOPIC = d[key]
                elif (key == "blocked_topic") and (arr_op == "ADD"):
                    if not (value in d[key]):
                        d[key] = d[key] + [value]
                     #   self.BLOCKED_TOPIC = d[key]
                elif (key == "blocked_topic") and (arr_op == "REM"):
                    if value in d[key]:
                        d[key].remove(value)
                      #  self.BLOCKED_TOPIC = d[key]
                else:
                    d[key] = value
                #print(d)
                self.DATA[key] = d[key]
                c2.write(json.dumps(d))
                c2.close()
            #if reload_variables:
            #    self.load_config_variable()
        except Exception as e:
            print("update config err: {}".format(e))

    def delete_config_variable(self, key):
        try:
            config = {}
            with open('DEVICE/config.json', "r") as c1:
                config = json.load(c1)
                c1.close()

            with open('DEVICE/config.json', "w") as c2:
                d = config.copy()
                if key in config.keys():
                    del d[key]
                    c2.write(json.dumps(d))
                    c2.close()
        except Exception as e:
            print("delete config err: {}".format(e))

    def update_name_property(self, id_property, name_property):
        try:
            props = {}
            with open('DEVICE/device.json', "r") as c1:
                props = json.load(c1)
                c1.close()

            with open('DEVICE/device.json', "w") as c2:
                d = props.copy()
                for num, prop in enumerate(d):
                    if prop["id_property"] == id_property:
                        d[num]["name_property"] = name_property
                c2.write(json.dumps(d))
                c2.close()
        except Exception as e:
            print("update property name err: {}".format(e))

    def add_action(self, id_topic, id_context, id_device, id_property, value):
        try:
            with open('DEVICE/action.json', "r") as a1:
                actions = json.load(a1)
                a1.close()

            id_act = "{}:{}:{}:{}".format(id_topic, id_context, id_device, id_property)
            #if id_act not in actions.keys():
            with open('DEVICE/action.json', "w") as c2:
                    d = actions.copy()
                    d[id_act] = value
                    c2.write(json.dumps(d))
                    c2.close()
        except Exception as e:
            print("add action err: {}".format(e))

    def get_action(self, id_topic, id_context, id_device, id_property):
        try:
            with open('DEVICE/action.json', "r") as c1:
                actions = json.load(c1)
                id_act = "{}:{}:{}:{}".format(id_topic, id_context, id_device, id_property)
                c1.close()
                if id_act in actions.keys():
                    return actions[id_act]
                return {}
        except Exception as e:
            print("get action err:{}".format(e) )
            return None

    def remove_action(self, id_topic, id_context, id_device, id_property):
        try:
            with open('DEVICE/action.json', "r") as c1:
                actions = json.load(c1)
                id_act = "{}:{}:{}:{}".format(id_topic, id_context, id_device, id_property)
                c1.close()
                if id_act in actions.keys():
                    del actions[id_act]
            with open('DEVICE/action.json', 'w') as c2:
                c2.write(json.dumps(actions))
                c2.close()
                return 1
        except Exception as e:
            print("remove action err:{}".format(e) )
            return 0

    def get_action_all(self):
        try:
            with open('DEVICE/action.json', "r") as c1:
                actions = json.load(c1)
                c1.close()
                return actions
        except Exception as e:
            print("get action all err:{}".format(e) )
            return {}

    def add_trigger(self, id_topic, id_context, id_device, id_property, type_trigger, value):
        try:
            with open('DEVICE/trigger.json', "r") as a1:
                triggers = json.load(a1)
                a1.close()

            id_trig = "{}:{}:{}:{}:{}".format(id_topic, id_context, id_device, id_property, type_trigger)
            with open('DEVICE/trigger.json', "w") as c2:
                d = triggers.copy()
                d[id_trig] = value
                c2.write(json.dumps(d))
                c2.close()
        except Exception as e:
            print("add trigger err: {}".format(e))

    def get_trigger(self, id_topic, id_context, id_device, id_property, type_trigger):
        try:
            with open('DEVICE/trigger.json', "r") as c1:
                triggers = json.load(c1)
                id_trig = "{}:{}:{}:{}:{}".format(id_topic, id_context, id_device, id_property, type_trigger)
                c1.close()
                if id_trig in triggers.keys():
                    return triggers[id_trig]
                return {}
        except Exception as e:
            print("get trigger err:{}".format(e) )
            return {}

    def remove_trigger(self, id_topic, id_context, id_device, id_property, type_trigger):
        try:
            with open('DEVICE/trigger.json', "r") as c1:
                triggers = json.load(c1)
                id_trig = "{}:{}:{}:{}:{}".format(id_topic, id_context, id_device, id_property, type_trigger)
                c1.close()
                if id_trig in triggers.keys():
                    del triggers[id_trig]
            with open('DEVICE/trigger.json', 'w') as c2:
                c2.write(json.dumps(triggers))
                c2.close()
                return 1
        except Exception as e:
            print("remove trigger err:{}".format(e) )
            return 0

    def get_trigger_all(self):
        try:
            with open('DEVICE/trigger.json', "r") as c1:
                triggers = json.load(c1)
                c1.close()
                return triggers
        except Exception as e:
            print("get trigger all err:{}".format(e) )
            return {}

    def update_topic_msg_count(self, id_topic):
        try:
            with open('DEVICE/topic_msg_count.json', "r") as c1:
                config = json.load(c1)
                c1.close()

            with open('DEVICE/topic_msg_count.json', "w") as c2:
                d = config.copy()
                #print("d.get(id_topic), ", d.get(id_topic))
                count = 1 if( d.get(id_topic) == None ) else d.get(id_topic)+1
                d[id_topic] = count
                c2.write(json.dumps(d))
                c2.close()
        except Exception as e:
            print("update topic_msg_count err: {}".format(e))

    def delete_topic_msg_count(self, id_topic):
        try:
            with open('DEVICE/topic_msg_count.json', "r") as c1:
                config = json.load(c1)
                c1.close()

            with open('DEVICE/topic_msg_count.json', "w") as c2:
                d = config.copy()
                del d[id_topic]
                c2.write(json.dumps(d))
                c2.close()
        except Exception as e:
            print("update topic_msg_count err: {}".format(e))

    def get_topic_msg_count_all(self):
        try:
            with open('DEVICE/topic_msg_count.json', "r") as c1:
                counts = json.load(c1)
                c1.close()
                return counts
        except Exception as e:
            print("get topic_msg_count all err:{}".format(e) )
            return {}

config = Config()
