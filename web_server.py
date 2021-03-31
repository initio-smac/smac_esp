import picoweb
from config import config
#config.load_config_variable()
import wifi_ap
from wifi_ap import wlan
import json
import gc
import machine
import wifi_client
import time
from ota_test import ota

ifconfig = wifi_client.wlan.ifconfig()
ADDR = ifconfig[0]

print(__name__)
#app = picoweb.WebApp(__name__)
app = picoweb.WebApp(None)

@app.route("/send_group_request")
def send_group_request(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()

    device_name = config.DEVICE_NAME
    group_id = req.form["group_id"]
    data = {}
    data["data"] = {'device_name': device_name}
    #mqttTest.connect()
    #import _thread
    #_thread.start_new_thread(mqttTest.connect, ())
    #utime.sleep(5)
    #mqttTest.publish(frm=config.DEVICE_ID, to=group_id, command=CMD_REQ_ADD_TO_GROUP, data=data)

    yield from picoweb.start_response(resp)
    yield from resp.awrite("Request sent successfully.")
 
@app.route("/test")
def test(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Hello world from picoweb running on the ESP32")


@app.route("/load_config")
def test(req, resp):
    yield from picoweb.start_response(resp)
    #config = open('config.json', 'r')
    config = {}
    with open('config.json', 'r') as f:
       config = f.read()
    
    rssi = wifi_client.wlan.status('rssi')
    c =  json.loads(config)
    c["connected_ssid"] = wifi_client.wlan.config('essid')
    c["connected_ssid_strength"] = rssi + 135
    print(c)
    print(type(c))
    yield from resp.awrite(json.dumps(c))

@app.route("/")
def index(req, resp):
    htmlFile = open('html/index.html', 'r')
    yield from picoweb.start_response(resp)
    #for line in htmlFile:
    yield from resp.awrite(htmlFile.read())

@app.route("/jquery.min.js")
def resp_jquery(req, resp):
    htmlFile = open('html/jquery.min.js', 'r')
    yield from picoweb.start_response(resp)
    yield from resp.awrite(htmlFile.read())

@app.route("/update_wifi")
def update_wifi(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()

    print(req.form)
    v = req.form
    conn = req.form["connection"]
    key_ = "wifi_config_1" if(conn == '1') else "wifi_config_2"
    yield from picoweb.start_response(resp)
    config.update_config_variable(key=key_, value=req.form )
    yield from resp.awrite("Wifi config updated successfully")

@app.route("/update_mqtt_server")
def update_mqtt_server(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()

    print(req.form)
    yield from picoweb.start_response(resp)
    config.update_config_variable(key="mqtt_server", value=req.form["mqtt_server"] )
    yield from resp.awrite("Mqtt Server updated successfully")

@app.route("/update_name_device")
def update_name_device(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()

    print(req.form)
    yield from picoweb.start_response(resp)
    config.update_config_variable(key="name_device", value=req.form["name_device"] )
    yield from resp.awrite("Device Name updated successfully")

@app.route("/remove_topic")
def remove_topic(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()

    #print("req.form",req.form)
    #print("req.form.keys", req.form.keys())
    print( json.loads(req.form["sub_topic"]) )
    yield from picoweb.start_response(resp)
    for topic in  json.loads(req.form["sub_topic"]):
        config.update_config_variable(key="sub_topic", value=topic, arr_op="REM" )
    yield from resp.awrite("Device Name updated successfully")

@app.route("/update_pin_device")
def update_pin_device(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()

    print(req.form)
    yield from picoweb.start_response(resp)
    config.update_config_variable(key="pin_device", value=req.form["pin_device"] )
    yield from resp.awrite("Device PIN updated successfully")

def http_get(url, https=True):
    import socket
    import ssl
    _, _, host, path = url.split('/', 3)
    print(host)
    print(path)
    
    #addr = socket.getaddrinfo(host, 80)[0][-1]
    #print(addr)
    s = socket.socket()
    port = 443 if https else 80
    s.connect( (host, port) )
    cmd = "GET https://smacsystem.com/download/esp32/version.js HTTP/1.0\r\n\r\n".encode()
    if https:
        
        s = ssl.wrap_socket(s)
    s.write(cmd)
    #s.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n' % (path, host), 'utf8'))
    data = ""
    while True:
        data = s.recv(100)
        if data:
            print("a\n")
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    print("res\n")
    #return str(data, 'utf8')

@app.route("/restart")
def restart(req, resp):
    print("restarting")
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()
    mode = req.form.get("mode", 0)
    config.update_config_variable(key="mode", value=mode )
    machine.reset()

@app.route("/download_update")
def download_update(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()
    print(req.form)
    version = req.form["version"]
    ota.download_all_files(version=version)
    config.delete_config_variable(key="download_version")
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Updates installed. Restarting")
    config.update_config_variable(key="mode", value=0)
    machine.reset()

@app.route("/check_for_update")
def check_for_update(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()
    new_updates = ota.check_for_latest_version()
    if new_updates:
        yield from picoweb.start_response(resp)
        yield from resp.awrite("New Updates available")
    else:
        yield from picoweb.http_error(resp, "400")
        yield from resp.awrite("Device is already upto date.")
        

#import _thread
#_thread.start_new_thread(mqttTest.connect, ())
download_software = config.get_config_variable(key="download_software")
print("download-software", download_software)
if download_software == 1:
    config.delete_config_variable(key="download_software")
    ota.check_and_install_udpates()


app.run(debug=True, host=ADDR)
