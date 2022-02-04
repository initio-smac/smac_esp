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
        print("Connecting to WIFI_CONIG_1:{}".format(config.WIFI_CONFIG_1["ssid"]))
        conn1 = wifi_connect(config.WIFI_CONFIG_1["ssid"], config.WIFI_CONFIG_1["password"])
        print("conn1", conn1)

        WIFI_NAME = ""
        if not conn1:
            print("Connecting to WIFI_CONIG_2:{}".format(config.WIFI_CONFIG_2["ssid"]))
            #time.sleep(5)
            conn2 = wifi_connect(config.WIFI_CONFIG_2["ssid"], config.WIFI_CONFIG_2["password"])
            if conn2:
                WIFI_NAME = config.WIFI_CONFIG_2["ssid"]
        else:
            WIFI_NAME = config.WIFI_CONFIG_1["ssid"]

        id_device = config.get_config_variable(key="id_device")
        #AP_TEXT = ""
        #wlan_ap = network.WLAN(network.AP_IF)
        if wlan.isconnected():
            print("connected")
            print( wlan.ifconfig() )
            AP_TEXT = "SMAC_{}_{}".format(id_device, WIFI_NAME)
        else:
            AP_TEXT = "SMAC_{}_NO_CONNECTION".format(id_device)
            #wlan_ap.config(essid=)
        if(setup_AP):
            from wifi_ap import wlan_ap
            wlan_ap.config(essid=AP_TEXT)
    except Exception as e:
        print("wlan station connect error: {}".format(e))