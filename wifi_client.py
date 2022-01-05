import network
from config import config
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
        global wlan
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
        
        

try:
    wlan = network.WLAN( network.STA_IF )
    wlan.active( True )

    #arr = wlan.scan()
    #print(arr)

    print("Connecting to WIFI_CONIG_1:{}".format(config.WIFI_CONFIG_1["ssid"]))  
    conn1 = wifi_connect(config.WIFI_CONFIG_1["ssid"], config.WIFI_CONFIG_1["password"])
    print("conn1", conn1)

    #while conn1!=None:
    #    pass

    WIFI_NAME = ""
    if not conn1:
        print("Connecting to WIFI_CONIG_2:{}".format(config.WIFI_CONFIG_2["ssid"]))
        conn2 = wifi_connect(config.WIFI_CONFIG_2["ssid"], config.WIFI_CONFIG_2["password"])
        if conn2:
            WIFI_NAME = config.WIFI_CONFIG_2["ssid"]
    else:
        WIFI_NAME = config.WIFI_CONFIG_1["ssid"]

    #while conn2!=None:
    #    pass
        
        #if not conn2:
        #    print("Connecting to WIFI_CONIG_DEFAULT:{}".format(config.WIFI_CONFIG_DEFAULT["ssid"]))
        #    conn3 = wifi_connect(config.WIFI_CONFIG_DEFAULT["ssid"], config.WIFI_CONFIG_DEFAULT["password"])
            
    id_device = config.get_config_variable(key="id_device")
    if wlan.isconnected():
        print("connected")
        print( wlan.ifconfig() )
        wlan_ap.config(essid="SMAC_{}_{}".format(id_device, WIFI_NAME))
        #led.value(1)
        #utime.sleep(1)
        #led.value(0)
        #utime.sleep(5)
    else:
        wlan_ap.config(essid="SMAC_{}_NO_CONNECTION".format(id_device))
except Exception as e:
    print("wlan station connect error: {}".format(e))


#while not wlan.isconnected():
#	pass

#print( wlan.ifconfig() )
#import blink
#blink.blink_led2()
