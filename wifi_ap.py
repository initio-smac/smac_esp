import network

try:
	wlan = network.WLAN(network.AP_IF)
	wlan.active(True)
	wlan.config(essid="ESP32_D2")
	#wlan.active(True)
except Exception as e:
	print("wifi ap err: {}".format(e))