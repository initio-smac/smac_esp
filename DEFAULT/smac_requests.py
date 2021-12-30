from config import config
import json

from smac_client import client

try:
    import urequests
except:
    import requests as urequests


SMAC_SERVER = "https://smacsystem.com/smacapi/"
#SMAC_SERVER = "https://reqres.in/api/products/3"
REQ_HEADERS = {'Accept': 'application/json',
               'content-type': 'application/json'
               }




def req_get_password(username):
    try:
        print(username)
        #print(datetime.now(tz=timezone.utc))
        date_now = machine.RTC().datetime()
        dt = utime.mktime(date_now)
        du = username.replace("D_", "")
        du = int("0x{}".format(du), 0)
        password = dt - du

        print(password)
        return str(password)
    except Exception as e:
        print("get password err: {}".format(e) )


def rest_call(url, method, request, data=None, json=None, headers=REQ_HEADERS ):
    try:
        if request == "request_device_uid":
            headers['Authorization'] = 'smac:smac1'

        if config.ID_DEVICE != "":
            username = config.ID_DEVICE
            password = req_get_password(username)
            headers['Authorization'] = '{}:{}'.format(username, password)

        req = urequests.request(method, url, data=data, json=json, headers=headers)
        res = req.text
        
        print(res)
        print(type(res))
        r = json.loads(res)
        print(r)
        #r = res
        if request == "request_device_uid":
            d = r["device_id"]
            config.update_config_file(key="ID_DEVICE", value=d)
            config.update_config_file(key="SUB_TOPIC", value=d)
            config.update_config_file(key="NAME_DEVICE", value="smac_{}".format(d))
            config.update_config_vars()
            client.subscribe(d)
        req.close()
    except Exception as e:
        print("urequests error: {}".format(e) )

def req_get_device_id():
    request = "request_device_uid"
    url = SMAC_SERVER + request
    rest_call(url=url, method="GET", request=request )


def req_check_connection(*args):
    url = "https://smacsystem.com/download/esp32/version.json"
    req = urequests.get(url)
    req.close()
    if req.status_code == 200:
        return True
    else:
        return False

