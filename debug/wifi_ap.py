import network
#from DEVICE.config import config



def setup_ap(ssid, password):
	try:
		wlan_ap = network.WLAN(network.AP_IF)
		wlan_ap.active(True)
		#w_config = config.DATA["ap_config"]
		#print(w_config)
		if password == None:
			wlan_ap.config(essid=ssid)
		else:
			wlan_ap.config(essid=ssid, password=password)
		#wlan.active(True)
		print("AP created")
	except Exception as e:
		print("wifi ap err: {}".format(e))