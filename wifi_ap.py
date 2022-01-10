import network
from DEVICE.config import config

try:
	wlan_ap = network.WLAN(network.AP_IF)
	wlan_ap.active(True)
	print(config.AP_CONFIG)
	wlan_ap.config(essid=config.AP_CONFIG["ssid"], password=config.AP_CONFIG["password"])
	#wlan.active(True)
except Exception as e:
	print("wifi ap err: {}".format(e))