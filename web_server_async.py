import gc
import uasyncio as asyncio
import _thread

import wifi_client
import usocket as socket
import machine
import json
from DEVICE.config import config
from smac_ota import smacOTA



def copy_folder(COPY_FROM="DEFAULT", COPY_TO="DEVICE"):
    from blink import blink_led
    _thread.start_new_thread(blink_led, ())
    TYPE_FILE = 32768
    TYPE_DIR = 16384
    import uos as os
    #os.rmdir(COPY_TO)
    #os.mkdir(COPY_TO)
    for i in os.ilistdir(COPY_FROM):
        name = i[0]
        typ = i[1]
        if typ == TYPE_DIR:
            #os.mkdir(COPY_TO + "/" + name)
            print("copying dir {} from {} to {}".format(name, COPY_FROM, COPY_TO))
            copy_folder( COPY_FROM+"/"+name, COPY_TO+"/"+name )
        if typ == TYPE_FILE:
            print("copying file {} from {} to {}".format(name, COPY_FROM, COPY_TO))
            f = open(COPY_FROM + "/" + name, "rb")
            with open(COPY_TO +"/"+ name, "wb") as f1:
                while True:
                    b = f.read(1024)
                    if b == b"":
                        break
                    f1.write(b)
                f1.close()
            f.close()


def tf():
    print("starting tf1")
    print("starting tf2")
    from urequests import request
    resp = request(method="GET", url="http://smacsystem.com/download/esp32/version.json")
    #resp = http_get(url="https://smacsystem.com/download/esp32/version.json", port=443)
    print("resp")
    print(resp.json())
    gc.collect()
    VERSION = config.VERSION
    if resp.status_code == 200:
        VERSION = resp.json()["version"]



#print( smacOTA.get_update_version() )

async def get_body(conn, size):
    data = b""
    count = 0
    with open("output.txt", "wb") as file:
        while True:
            chunk = await conn.read(1024)
            print(len(chunk))
            print(chunk)
            file.write(chunk)
            count += len(chunk)
            if len(chunk) < 1024:
                break
        file.close()
    print("written {} bytes outof {}".format(count, size))

async def get_head(conn):
    """ gets headers from client """
    data = b""
    while not data.endswith(b"\r\n\r\n"):
        data += await conn.read(1)
    return data

async def on_new_connection(reader, writer, *args):
    print("new connection")
    print(args)
    req = await get_head(reader)
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
    response = ""
    if http_path == "/":
        response = open("html/index.html", "r").read()
    elif http_path == "/scripts.js":
        response = open("html/scripts.js", "r").read()
    elif http_path.find("/upload_software_file") != -1:
        print(http_method)
        size = int(headers['Content-Length'])
        print(size)
        f = await get_body(conn, size)
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
        con = open("DEVICE/config.json", "r").read()
        c = json.loads(con)
        try:
            rssi = wifi_client.wlan.status('rssi')
            c["connected_ssid"] = wifi_client.wlan.config('essid')
            c["connected_ssid_strength"] = rssi + 135
        except Exception as e:
            pass
        response = json.dumps(c)
    elif http_path.find("/update_wifi") != -1:
        print("update wifi")
        conn1 = params["connection"]
        key_ = "wifi_config_1" if (conn1 == '1') else "wifi_config_2"
        config.update_config_variable(key=key_, value=params)
        response = "Wifi config updated successfully"
    elif http_path.find("/update_wifi_ap") != -1:
        print("update wifi Access Point")
        config.update_config_variable(key="ap_config", value=params)
        response = "Wifi Access Point config updated successfully"
    elif http_path.find("/update_name_device") != -1:
        config.update_config_variable(key="name_device", value=params["name_device"])
        response = "Device Name Updated Successfully."
    elif http_path.find("/remove_topic") != -1:
        print(params["sub_topic"])
        sub_topic = params["sub_topic"].replace("%22", '"')
        for topic in json.loads(sub_topic):
            config.update_config_variable(key="sub_topic", value=topic, arr_op="REM")
        response = "Topics Updated Successfully."
    elif http_path.find("/remove_blocked_topic") != -1:
        print(params["blocked_topic"])
        blocked_topic = params["blocked_topic"].replace("%22", '"')
        for topic in json.loads(blocked_topic):
            config.update_config_variable(key="blocked_topic", value=topic, arr_op="REM")
        response = "Blocked Topics Updated Successfully."
    elif http_path.find("/update_pin_device") != -1:
        config.update_config_variable(key="pin_device", value=params["pin_device"])
        response = "Device PIN Updated Successfully."
    elif http_path.find("/restart_webrepl") != -1:
        #mode = params.get("mode", 0)
        config.update_config_variable(key="mode", value=3)
        print(config.get_config_variable("mode"))
        machine.reset()
        response = "Restarting Device in WebREPL mode."
    elif http_path.find("/restart") != -1:
        #mode = params.get("mode", 0)
        config.update_config_variable(key="mode", value=0)
        machine.reset()
        response = "Restarting Device."
    elif http_path.find("/update_input_type") != -1:
        ip_type = params.get("input_type", "switch")
        config.update_config_variable(key="input_type", value=ip_type)
        response = "Input Type Updated."
    elif http_path.find("/check_and_download_update") != -1:
        #print("Restarting in Software Update Mode...")
        # set mode to dowload mode and restart
        #config.update_config_variable(key="mode", value=1)
        #machine.reset()
        print("checking for updates")
        cur_version = config.get_config_variable(key="version")
        new_version = await smacOTA.get_update_version(cur_version)
        print("cur_version ", cur_version)
        print("new_version ", new_version)
        #new_version = "03"
        #await smacOTA.download_update(version=new_version)
        if (new_version != -1):
            print("New Updates Available")
            print("Initiating Update Software")
            await smacOTA.download_update(version=new_version)
        else:
            print("No Updates Available")
            response = "No Updates Available"


    elif http_path.find("/reset_device") != -1:
        print("Resetting to Default Version...")
        copy_folder(COPY_FROM="DEFAULT", COPY_TO="DEVICE")
        config.update_config_variable(key="mode", value=2)
        #machine.reset()
        response = "Device Reset Completed"
    #elif http_path.find("/download_update") != -1:
    #    #gc.collect()
    ##    version = params.get("version", None)
    #   print(params)
    #    if version != None:
    #        print("Downloading update...")
    #        
    #        #_thread.start_new_thread( smacOTA.download_update(version=version) )
    #        await smacOTA.download_update(version)'''

    #elif http_path.find("/check_for_update") != -1:
    #    cur_version = config.get_config_variable(key="version")
    #    resp = await smacOTA.get_update_version(cur_version)
        #ver = smacOTA.get_update_version()
        # try:
        #wifi_client.wlan_ap.active(False)
        #from urequests import request as req1
        #resp = req1(method="GET", url="https://smacsystem.com/download/esp32/version.json")
        #dat = {}
        #if resp.status_code == 200:
        #cur_version = config.get_config_variable(key="version")
        #VERSION = resp.json()["version"]
        #if VERSION != -1:
        #    if cur_version != VERSION:
        #        dat["resp_code"] = 1
        #        dat["version"] = VERSION
        #        dat["text"] = "New Updates Available"
        #    elif cur_version == VERSION:
        #        dat["resp_code"] = 0
        #        dat["version"] = VERSION
        ##        dat["text"] = "Your Device is Upto Date"
        #else:
        #    dat["resp_code"] = -1
        #    dat["text"] =  "Error While Checking For Updates"
        #response = json.dumps(dat)'''


    try:
        writer.write('HTTP/1.1 200 OK\n')
        await writer.drain()
        writer.write('Content-Type: text/html\n')
        await writer.drain()
        writer.write('Connection: close\n\n')
        await writer.drain()
        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        gc.collect()
    except Exception as e:
        print("Error while serving: {}".format(e))

async def tt():
    await asyncio.sleep(1)
    while 1:
        await asyncio.sleep(1)

async def main():
#    #t2 = asyncio.create_task(tt())
    print("starting server")
    t1 = asyncio.create_task( start_server() )
#    await t2
    await t1

async def start_server():
    await asyncio.sleep(0)
    #import DEVICE.wifi_client2
#asyncio.run( main() )
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(on_new_connection, "0.0.0.0", 80))
    try: 
        loop.run_forever()
    except KeyboardInterrupt:
        print("closing")
        loop.close()

#asyncio.run(main())