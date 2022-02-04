
import machine


from DEVICE.config import config
config.load_config_variable()


def set_internet_time():
    try:
        import ntptime
        ntptime.settime()
        import time
        print(time.localtime())
    except:
        pass

RESET_BUTTON = 33


try:
    #import DEVICE.config as cn
    import _thread
    import blink
    _thread.start_new_thread(blink.device_boot_blink_led, ())
except:
    pass




# on double click,
# change the mode restart in web AP mode
def on_dbl_click(*args):
    # mode = 2
    mode = config.get_config_variable(key="mode")
    mode = 2 if(mode == 0) else 0
    config.update_config_variable(key="mode", value=mode)
    machine.reset()


# on long press,
# reset the device to default code
def on_long_press(*args):
    from web_server import copy_folder
    print("Resetting to Default Version...")
    copy_folder(COPY_FROM="DEFAULT", COPY_TO="DEVICE")
    config.update_config_variable(key="mode", value=0)
    machine.reset()

async def my_app():
    await asyncio.sleep(1)
    while 1:
        await asyncio.sleep(1)


def init_reset_func():
    from machine import Pin
    from debounce import Pushbutton
    ip = Pin(RESET_BUTTON, Pin.IN, Pin.PULL_UP)
    rs = Pushbutton(ip)
    rs.double_func(on_dbl_click, ())
    rs.long_func(on_long_press, ())

# run functions
MODE = config.MODE
print("MODE", MODE)
#MODE = 2
if MODE == 3:
    import wifi_ap
    wifi_ap.wlan_ap.active(True)
    print("Webrepl Mode")
elif MODE == 2:
    import wifi_ap
    import wifi_client
    wifi_client.init(setup_AP=True)
    import web_server
    web_server.start_server()
    '''from urequests import request
    resp = request(method="GET", url="https://smacsystem.com/download/esp32/version.json")
    print("resp")
    print(resp.json())'''
elif MODE == 1:
    import wifi_client
    wifi_client.init()
    from smac_ota import smacOTA
    print("Checking For Updates")
    cur_version = config.get_config_variable(key="version")
    new_version = smacOTA.get_update_version(cur_version)
    if (new_version != -1):
        print("New Updates Available")
        print("Initiating Update Software")
        smacOTA.download_update(version=new_version)
    else:
        print("No Updates Available")
        config.update_config_variable(key="mode", value=0)
        #import machine
        machine.reset()
elif MODE == 0:
    # import wifi_ap
    # import wifi_client
    # wifi_client.init(setup_AP=False)
    # set_internet_time()
    init_reset_func()
    try:
        import DEVICE.start
    except Exception as e:
        print("Exception while initiating APP", e)
        import uasyncio as asyncio
        asyncio.run(my_app())
