from config import config
from smac_client import client
from smac_keys import smac_keys


def add_action(data, frm):
    id_device = data.get(smac_keys["ID_DEVICE"])
    if id_device == config.ID_DEVICE:
        actions = config.get_action_all()
        #print("acts",actions)
        #print("acts",actions.keys())
        print( config.get_config_variable(key="limit_action") )
        if len(actions) < config.get_config_variable(key="limit_action"):
            passkey = data.get(smac_keys["PASSKEY"])
            if str(config.PIN_DEVICE) == str(passkey):
                id_topic = data.get(smac_keys["ID_TOPIC"])
                id_context = data.get(smac_keys["ID_CONTEXT"])
                id_property = data.get(smac_keys["ID_PROPERTY"])
                value = data.get(smac_keys["VALUE"])
                config.add_action(id_topic, id_context, id_device, id_property, value)
                d1 = {}
                d1[smac_keys["ID_TOPIC"]] = id_topic
                d1[smac_keys["ID_CONTEXT"]] = id_context
                d1[smac_keys["ID_DEVICE"]] = id_device
                d1[smac_keys["ID_PROPERTY"]] = id_property
                d1[smac_keys["VALUE"]] = value
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_ADD_ACTION"], message=d1)
            else:
                d1 = {}
                d1[smac_keys["MESSAGE"]] = "Action Not Added. Passkey Error"
                print(d1[smac_keys["MESSAGE"]])
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                    message=d1)
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Action Not Added. Limit Error"
            print(d1[smac_keys["MESSAGE"]])
            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_ACTION_LIMIT_EXCEEDED"],
                                message=d1)

def add_trigger(data, frm):
    id_device = data.get(smac_keys["ID_DEVICE"])
    if id_device == config.ID_DEVICE:
        triggers = config.get_trigger_all()
        if len(triggers) < config.get_config_variable(key="limit_trigger"):
            passkey = data.get(smac_keys["PASSKEY"])
            if str(config.PIN_DEVICE) == str(passkey):
                id_topic = data.get(smac_keys["ID_TOPIC"])
                id_context = data.get(smac_keys["ID_CONTEXT"])
                id_property = data.get(smac_keys["ID_PROPERTY"])
                type_trigger = data.get(smac_keys["TYPE_TRIGGER"])
                value = data.get(smac_keys["VALUE"])
                config.add_trigger(id_topic, id_context, id_device, id_property, type_trigger, value)
                d1 = {}
                d1[smac_keys["ID_TOPIC"]] = id_topic
                d1[smac_keys["ID_CONTEXT"]] = id_context
                d1[smac_keys["ID_DEVICE"]] = id_device
                d1[smac_keys["ID_PROPERTY"]] = id_property
                d1[smac_keys["TYPE_TRIGGER"]] = type_trigger
                d1[smac_keys["VALUE"]] = value
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_ADD_TRIGGER"], message=d1)
            else:
                d1 = {}
                d1[smac_keys["MESSAGE"]] = "Trigger Not Added. Passkey Error"
                print(d1[smac_keys["MESSAGE"]])
                client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                    message=d1)
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Trigger Not Added. Limit Error"
            print(d1[smac_keys["MESSAGE"]])
            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_TRIGGER_LIMIT_EXCEEDED"],
                                message=d1)

def remove_action(data, frm):
    id_device = data.get(smac_keys["ID_DEVICE"])
    if id_device == config.ID_DEVICE:
        passkey = data.get(smac_keys["PASSKEY"])
        if str(config.PIN_DEVICE) == str(passkey):
            id_topic = data.get(smac_keys["ID_TOPIC"])
            id_context = data.get(smac_keys["ID_CONTEXT"])
            id_property = data.get(smac_keys["ID_PROPERTY"])
            #value = data.get(smac_keys["VALUE"])
            config.remove_action(id_topic, id_context, id_device, id_property)
            d1 = {}
            d1[smac_keys["ID_TOPIC"]] = id_topic
            d1[smac_keys["ID_CONTEXT"]] = id_context
            d1[smac_keys["ID_DEVICE"]] = id_device
            d1[smac_keys["ID_PROPERTY"]] = id_property
            #d1[smac_keys["VALUE"]] = value
            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_REMOVE_ACTION"], message=d1)
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Action Not Removed. Passkey Error"
            print(d1[smac_keys["MESSAGE"]])
            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                message=d1)

def remove_trigger(data, frm):
    id_device = data.get(smac_keys["ID_DEVICE"])
    if id_device == config.ID_DEVICE:
        passkey = data.get(smac_keys["PASSKEY"])
        if str(config.PIN_DEVICE) == str(passkey):
            id_topic = data.get(smac_keys["ID_TOPIC"])
            id_context = data.get(smac_keys["ID_CONTEXT"])
            id_property = data.get(smac_keys["ID_PROPERTY"])
            type_trigger = data.get(smac_keys["TYPE_TRIGGER"])
            #value = data.get(smac_keys["VALUE"])
            config.remove_trigger(id_topic, id_context, id_device, id_property, type_trigger)
            d1 = {}
            d1[smac_keys["ID_TOPIC"]] = id_topic
            d1[smac_keys["ID_CONTEXT"]] = id_context
            d1[smac_keys["ID_DEVICE"]] = id_device
            d1[smac_keys["ID_PROPERTY"]] = id_property
            d1[smac_keys["TYPE_TRIGGER"]] = type_trigger
            #d1[smac_keys["VALUE"]] = value
            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_STATUS_REMOVE_TRIGGER"], message=d1)
        else:
            d1 = {}
            d1[smac_keys["MESSAGE"]] = "Trigger Not Added. Passkey Error"
            print(d1[smac_keys["MESSAGE"]])
            client.send_message(frm=config.ID_DEVICE, to=frm, cmd=smac_keys["CMD_INVALID_PIN"],
                                message=d1)