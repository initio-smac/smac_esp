import network

try:
	wlan_ap = network.WLAN(network.AP_IF)
	wlan_ap.active(True)
	wlan_ap.config(essid="ESP32_D2")
	#wlan.active(True)
except Exception as e:
	print("wifi ap err: {}".format(e))