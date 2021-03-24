import network
import config
from machine import Pin
import utime

#led = Pin(2, Pin.OUT, value=0)

def wifi_connect(ssid, password):
    try:
        global wlan
        wlan.connect(ssid, password)
        utime.sleep(5)
        print(wlan.isconnected())
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
    
    if not conn1:
        print("Connecting to WIFI_CONIG_2:{}".format(config.WIFI_CONFIG_2["ssid"]))  
        conn2 = wifi_connect(config.WIFI_CONFIG_2["ssid"], config.WIFI_CONFIG_2["password"])
        
        if not conn2:
            print("Connecting to WIFI_CONIG_DEFAULT:{}".format(config.WIFI_CONFIG_DEFAULT["ssid"]))  
            conn3 = wifi_connect(config.WIFI_CONFIG_DEFAULT["ssid"], config.WIFI_CONFIG_DEFAULT["password"])
            

    if wlan.isconnected():
        print("connected")
        print( wlan.ifconfig() )
        #led.value(1)
        #utime.sleep(1)
        #led.value(0)
        #utime.sleep(5)
except Exception as e:
	print("wlan station connect error: {}".format(e))


#while not wlan.isconnected():
#	pass

#print( wlan.ifconfig() )
#import blink
#blink.blink_led2()
