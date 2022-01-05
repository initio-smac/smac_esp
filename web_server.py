import gc
#import network
#import uasyncio as asyncio
import _thread

#from smac_ota import smacOTA
#import smac_ota
#import re

import wifi_client
import usocket as socket
import machine
import json
from DEVICE.config import config




#import http_client

#import network
#ap = network.WLAN(network.AP_IF)
#ap.active(True)
#ap.config(essid="AP_MODE")


#import utime
#utime.sleep(3)

#cli = http_client.HttpClient()

def copy_folder(COPY_FROM="DEFAULT", COPY_TO="DEVICE"):
    TYPE_FILE = 32768
    TYPE_DIR = 16384
    import uos as os
    try:
        os.rmdir(COPY_TO)
    except:
        pass
    os.mkdir(COPY_TO)
    for i in os.ilistdir(COPY_FROM):
        name = i[0]
        typ = i[1]
        if typ == TYPE_DIR:
            #os.mkdir(COPY_TO + "/" + name)
            print("copying dir {} from {} to {}".format(name, COPY_FROM, COPY_TO))
            copy_folder( COPY_FROM+"/"+name, COPY_TO+"/"+name )
        if typ == TYPE_FILE:
            print("copying file {} from {} to {}".format(name, COPY_FROM, COPY_TO))
            f = open(COPY_TO + "/" + name, "rb")
            with open("DEVICE/" + name, "wb") as f1:
                f1.write(f.read())
                f1.close()
            f.close()


def tf():
    print("starting tf1")
    print("starting tf2")
    from urequests import request
    resp = request(method="GET", url="https://smacsystem.com/download/esp32/version.json")
    #resp = http_get(url="https://smacsystem.com/download/esp32/version.json", port=443)
    print("resp")
    print(resp.json())
    gc.collect()
    VERSION = config.VERSION
    if resp.status_code == 200:
        VERSION = resp.json()["version"]



#print( smacOTA.get_update_version() )

def get_body(conn, size):
    data = b""
    count = 0
    with open("output.txt", "wb") as file:
        while True:
            chunk = conn.recv(1024)
            print(len(chunk))
            print(chunk)
            file.write(chunk)
            count += len(chunk)
            if len(chunk) < 1024:
                break
        file.close()
    print("written {} bytes outof {}".format(count, size))
    '''while True:
        chunk = conn.recv(1024)
        if len(chunk) < 1024:
            return data + chunk
        else:
            data += chunk'''
    '''data = b""
    while b"\r\n\r\n" not in data:
        data += conn.recv(1024)
    return data'''

def get_head(conn):
    """ gets headers from client """
    data = b""
    while not data.endswith(b"\r\n\r\n"):
        data += conn.recv(1)
    return data

def start_server():
    #await asyncio.sleep(1)
    print("Staring Http server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while True:
            #await asyncio.sleep(0)
            conn, addr = s.accept()
        #try:
            print('Got a connection from %s' % str(addr))
            req = get_head(conn)

            #print(req)
            #req = conn.recv(1024)
            req = req.decode('utf-8')
            lines = req.strip().splitlines()
            request = lines[0]
            headers = lines[1:]
            headers = list(line.split(': ') for line in headers)
            headers = dict(headers)
            #print(headers)
            print(request)
            params = {}
            #http_path = req.split("\n")[0]
            h = request.split(" ")
            http_method = h[0]
            http_path = h[1]
            paramstring = http_path.split('?')
            #print(paramstring)
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
            elif http_path.find("/upload_software_file") != -1:
                print(http_method)
                size = int(headers['Content-Length'])
                print(size)
                f = get_body(conn, size)
                #print(f)
                #with open("output.txt", "wb") as file:
                    #file.write(req.encode("utf-8"))
                #    file.write(f)
                gc.collect()
                '''name = re.compile(b'name="file"; filename="(.+)"').search(f).group(1)
                data1 = re.compile(
                    b"WebKitFormBoundary((\n|.)*)Content-Type.+\n.+?\n((\n|.)*)([\-]+WebKitFormBoundary)?")
                d1 = data1.search(f).group(3)
                print(name)
                print(d1)'''
                print("aa\n")
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
                #gc.collect()
                version = params.get("version", None)
                print(params)
                if version != None:
                    print("Downloading update...")
                    from smac_ota import smacOTA
                    _thread.start_new_thread( smacOTA.download_update(version=version) )
            elif http_path.find("/check_and_download_update") != -1:
                print("Restarting in Software Update Mode...")
                # set mode to dowload mode and restart
                config.update_config_variable(key="mode", value=1)
                machine.reset()
            elif http_path.find("/reset_device") != -1:
                print("Resetting to Default Version...")
                copy_folder(COPY_FROM="DEFAULT", COPY_TO="DEVICE")


            elif http_path.find("/check_for_update") != -1:
                #ver = smacOTA.get_update_version()
                # try:
                #wifi_client.wlan_ap.active(False)
                from urequests import request as req1
                resp = req1(method="GET", url="https://smacsystem.com/download/esp32/version.json")
                #gc.collect()
                #wifi_client.wlan_ap.active(True)
                #print(resp)
                dat = {}
                #if resp.status_code == 200:
                cur_version = config.get_config_variable(key="version")
                VERSION = resp.json()["version"]
                if VERSION != -1:
                    if cur_version != VERSION:
                        dat["resp_code"] = 1
                        dat["version"] = VERSION
                        dat["text"] = "New Updates Available"
                    elif cur_version == VERSION:
                        dat["resp_code"] = 0
                        dat["version"] = VERSION
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
            '''except Exception as e:
                conn.send('HTTP/1.1 400 Bad Request\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                print(e)
                conn.sendall(str(e))
                conn.close()'''

#_thread.start_new_thread( start_server, () )
start_server()