import time

from DEVICE.config import config
config.load_config_variable()

def set_internet_time():
    try:
        import ntptime
        ntptime.settime()
        print(time.localtime())
    except:
        pass

# run functions
MODE = config.MODE
print("MODE", MODE)
MODE = 0
if MODE == 2:
    import wifi_ap
    import wifi_client
    wifi_client.init(setup_AP=True)
    import web_server
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
    if( new_version != -1):
        print("New Updates Available")
        print("Initiating Update Software")
        smacOTA.download_update(version=new_version)
    else:
        print("No Updates Available")
        config.update_config_variable(key="mode", value=0)
        #import machine
        #machine.reset()
elif MODE == 0:
    import wifi_ap
    import wifi_client
    wifi_client.init(setup_AP=True)
    #set_internet_time()
    import DEVICE.start