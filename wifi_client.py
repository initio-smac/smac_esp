import json
import time

import network
from DEVICE.config import config
#from machine import Pin
import utime
#import wifi_ap

'''try:
	wlan_ap = network.WLAN(network.AP_IF)
	wlan_ap.active(True)
	wlan_ap.config(essid="ESP32_D2")
	#wlan.active(True)
except Exception as e:
	print("wifi ap err: {}".format(e))'''

#led = Pin(2, Pin.OUT, value=0)

def wifi_connect(ssid, password):
    try:
        COUNT = 0
        #global wlan
        wlan.connect(ssid, password)
        #if (wlan.isconnected()) or (COUNT >= 10):
        #    return wlan.isconnected()
        while  ( not(wlan.isconnected()) and (COUNT < 10) ):
            COUNT += 1
            utime.sleep(1)
        return wlan.isconnected()
    except Exception as e:
        print("wifi connect  err: {}".format(e) )
        return False
        
#f = open("wifi.json", "r").read()
#config = json.loads(f)
wlan = network.WLAN( network.STA_IF )
wlan.active( True )
def init(setup_AP=False):
    try:
        #arr = wlan.scan()
        #print(arr)
        w_config = config.DATA["wifi_config_1"]
        print("Connecting to WIFI_CONIG_1:{}".format(w_config["ssid"]))
        conn1 = wifi_connect(w_config["ssid"], w_config["password"])
        print("conn1", conn1)

        #WIFI_NAME = ""
        #if not conn1:
            #print("Connecting to WIFI_CONIG_2:{}".format(config.WIFI_CONFIG_2["ssid"]))
            #time.sleep(5)
            
            #conn2 = wifi_connect(config.WIFI_CONFIG_2["ssid"], config.WIFI_CONFIG_2["password"])
            #if conn2:
            #    WIFI_NAME = config.WIFI_CONFIG_2["ssid"]
        #else:
        #    WIFI_NAME = w_config["ssid"]

        id_device = config.ID_DEVICE
        #AP_TEXT = ""
        #wlan_ap = network.WLAN(network.AP_IF)
        if wlan.isconnected():
            print("connected")
            print( wlan.ifconfig() )
            AP_TEXT = "SMAC_{}_{}".format(id_device, w_config["ssid"])
        else:
            AP_TEXT = "SMAC_{}_NO_CONNECTION".format(id_device)
            #wlan_ap.config(essid=)
        print(AP_TEXT)
        print(setup_AP)
        if(setup_AP):
            import wifi_ap
            wifi_ap.setup_ap(ssid=AP_TEXT, password=None)
            #config.update_config_variable(key="ap_config", value={"ssid": AP_TEXT, "password": ""})
    except Exception as e:
        print("wlan station connect error: {}".format(e))