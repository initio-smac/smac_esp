from config import config
#import time
config.load_config_variable()
#time.sleep(1)
import wifi_client


MODE = config.MODE
print("MODE", MODE)
MODE = 2
if MODE == 2:
    import web_server
elif MODE == 1:
    #import web_server
    #import wifi_client
    #import _thread
    from smac_ota2 import smacOTA
    print("Initiating Update Software")
    smacOTA.download_update()
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


