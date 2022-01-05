import network

wlan = network.WLAN( network.STA_IF )
wlan.active( True )

SSID = "initioenergy_act"
PWD = "Smacsystem@6"

SSID = "Realme"
PWD = "nopassword"

print("Connecting to WIFI:{}".format(SSID))
wlan.connect(SSID, PWD)

while not wlan.isconnected():
	pass
