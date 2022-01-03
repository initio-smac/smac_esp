from config import config
config.load_config_variable()

# wifi AP
import network
'''try:
	wlan_ap = network.WLAN(network.AP_IF)
	wlan_ap.active(True)
	wlan_ap.config(essid="ESP32_D2")
	#wlan.active(True)
except Exception as e:
	print("wifi ap err: {}".format(e))'''

import wifi_client


# run functions
MODE = config.MODE
print("MODE", MODE)
MODE = 2
if MODE == 2:
    import web_server
    '''from urequests import request
    resp = request(method="GET", url="https://smacsystem.com/download/esp32/version.json")
    print("resp")
    print(resp.json())'''
elif MODE == 1:
    #import web_server
    #import wifi_client
    #import _thread
    from smac_ota import smacOTA
    print("Initiating Update Software")
    smacOTA.download_update(version="02")
elif MODE == 0:
    import start

#MODE = 0

'''from debounce import DebouncedSwitch
from machine import Pin, Timer

IP_PIN = 34
IP_COUNTER = 0

def ip_handler(*args):
    global IP_COUNTER
    IP_COUNTER += 1

def import_file(*args):
    print("IP_COUNTER: {}".format(IP_COUNTER) )
    if IP_COUNTER > 1:
        import web_server
    else:
        import start
    

IP = Pin(IP_PIN, Pin.IN, Pin.PULL_UP)
DebouncedSwitch(IP, ip_handler, arg=() )

tim = Timer(3)                                   # create a timer object using timer 3
tim.init(mode=Timer.ONE_SHOT, callback=import_file, period=5000)   '''   


