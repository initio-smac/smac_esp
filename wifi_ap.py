import network

try:
	wlan = network.WLAN(network.AP_IF)
	wlan.active(True)
	wlan.config(essid="esp32_man")
	#wlan.active(True)
except Exception as e:
	print("wifi ap err: {}".format(e))