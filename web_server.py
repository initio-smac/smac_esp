import picoweb
import wifi_ap
from wifi_ap import wlan
import json
import config
config.update_config_vars()
import gc
#import urequests

import wifi_client
from client import mqttTest
import utime
from mqtt_keys import CMD_REQ_ADD_TO_GROUP 

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
    import _thread
    _thread.start_new_thread(mqttTest.connect, ())
    utime.sleep(5)
    mqttTest.publish(frm=config.DEVICE_ID, to=group_id, command=CMD_REQ_ADD_TO_GROUP, data=data)

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
    config.update_config_file(key=key_, value=req.form )
    yield from resp.awrite("Wifi config updated successfully")

@app.route("/update_mqtt_server")
def update_mqtt_server(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()

    print(req.form)
    yield from picoweb.start_response(resp)
    config.update_config_file(key="mqtt_server", value=req.form["mqtt_server"] )
    yield from resp.awrite("Mqtt Server updated successfully")

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
    config.update_config_file(key="mode", value=0 )
    import machine
    machine.reset()

@app.route("/download_version")
def download_version(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        req.parse_qs()
    print(req.form)
    version = req.form["version"]
    yield from picoweb.start_response(resp)
    config.update_config_file(key="download_version", value=version )
    yield from resp.awrite("Wifi config updated successfully")

@app.route("/check_for_update")
def check_for_update(req, resp):
        if req.method == "POST":
            yield from req.read_form_data()
        else:  # GET, apparently
            req.parse_qs()
    #try:
        url = 'https://smacsystem.com/download/esp32/version.json'
        import urequests
        req1 = urequests.get( url )
        res = req1.text
        print(res)
        #print(req1.json())
        #res = json.loads(res)
        req1.close()
        #version = res.get("version", "01")
        #print(version)
        #print(config.VERSION)
        #print(config.VERSION != version)
        #if config.VERSION != version:
        yield from picoweb.start_response(resp)
        yield from resp.awrite("New Updates available")
        #req1.close()
        #else:
            #raise Exception("No updates")
        #    yield from picoweb.start_response(resp, status="400")
        #    yield from resp.awrite("No updates available")
        

#import _thread
#_thread.start_new_thread(mqttTest.connect, ())
app.run(debug=True, host=ADDR)
