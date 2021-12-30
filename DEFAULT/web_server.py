import gc
import usocket as socket
import network
#import uasyncio as asyncio
import _thread

#from smac_ota import smacOTA
import smac_ota
import wifi_client
import json
from config import config
import machine
from urequests import request

#ap = network.WLAN(network.AP_IF)
#ap.active(True)
#ap.config(essid="AP_MODE")



def start_server():
    print("Staring Http server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        try:
            print('Got a connection from %s' % str(addr))
            req = conn.recv(1024)
            req = req.decode('utf-8')
            params = {}
            http_path = req.split("\n")[0]
            http_path = http_path.split(" ")[1]
            paramstring = http_path.split('?')
            print(paramstring)
            if( len(paramstring) > 1 ) and (paramstring[1] != ""):
                #paramstring = paramstring[1].split(' ')[0]  # chop off the HTTP version
                paramarray = paramstring[1].split('&')
                for i in paramarray:
                    p = i.split("=")
                    params[ p[0] ] = p[1]

            #print('Content = %s' % request)
            print(params)
            print(http_path)
            #print(http_path.find("/load_config"))
            if http_path == "/":
                response = open("html/index.html", "r").read()
            elif http_path.find("/test") != -1:
                response = "Hello world from Socket running on the ESP32"
            elif http_path.find("/load_config") != -1:
                con = open("config.json", "r").read()
                rssi = wifi_client.wlan.status('rssi')
                c = json.loads(con)
                c["connected_ssid"] = wifi_client.wlan.config('essid')
                c["connected_ssid_strength"] = rssi + 135
                response = json.dumps(c)
            elif http_path.find("/update_wifi") != -1:
                print("update wifi")
                conn1 = params["connection"]
                key_ = "wifi_config_1" if (conn1 == '1') else "wifi_config_2"
                config.update_config_variable(key=key_, value=params)
                response = "Wifi config updated successfully"
            elif http_path.find("/update_name_device") != -1:
                config.update_config_variable(key="name_device", value=params["name_device"])
                response = "Device Name Updated Successfully."
            elif http_path.find("/remove_topic") != -1:
                print(params["sub_topic"])
                sub_topic = params["sub_topic"].replace("%22", '"')
                for topic in json.loads(sub_topic):
                    config.update_config_variable(key="sub_topic", value=topic, arr_op="REM")
                response = "Topics Updated Successfully."
            elif http_path.find("/update_pin_device") != -1:
                config.update_config_variable(key="pin_device", value=params["pin_device"])
                response = "Device PIN Updated Successfully."
            elif http_path.find("/restart") != -1:
                mode = params.get("mode", 0)
                config.update_config_variable(key="mode", value=mode)
                machine.reset()
                response = "Resetting Device."
            elif http_path.find("/download_update") != -1:
                gc.collect()
                version = params.get("version", None)
                if version != None:
                    print("Downloading update...")
                    _thread.start_new_thread( smac_ota.smacOTA.download_update(version=version) )

            elif http_path.find("/check_for_update") != -1:
                #ver = smacOTA.get_update_version()
                # try:
                resp = request(method="GET", url="https://smacsystem.com/download/esp32/version.json")
                gc.collect()
                print(resp)
                dat = {}
                if resp.status_code == 200:
                    cur_version = config.get_config_variable(key="version")
                    ver = resp.json()["version"]
                    if ver != -1:
                        if cur_version != ver:
                            dat["resp_code"] = 1
                            dat["version"] = ver
                            dat["text"] = "New Updates Available"
                        elif cur_version == ver:
                            dat["resp_code"] = 0
                            dat["version"] = ver
                            dat["text"] = "Your Device is Upto Date"
                else:
                    dat["resp_code"] = -1
                    dat["text"] =  "Error While Checking For Updates"
                response = json.dumps(dat)

            '''if params.get("led", None) == "on":
                print('LED ON')
                led.value(1)
                response = web_page()
            elif params.get("led", None) == "off":
                print('LED OFF')
                led.value(0)
                response = web_page()'''

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except Exception as e:
            conn.send('HTTP/1.1 400 Bad Request\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            print(e)
            conn.sendall(str(e))
            conn.close()

#_thread.start_new_thread( start_server, () )
start_server()