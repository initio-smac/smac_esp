

#import wifi_client2

#import start

#from ota_test import ota
#ota.download_all_files(version="02", path="")

import _thread
from http_client import HttpClient
from machine import Pin
import utime

def download_file(url, file_path):
    led = Pin(2, Pin.OUT)
    led.on()
    print("staring download...")
    client = HttpClient()
    # url, data=None, json=None, file=None, custom=None, saveToFile=None
    client.request(method="GET", url=url, saveToFile=file_path)
    print("download complete")
    led.off()

#url = "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"
#_thread.start_new_thread( download_file, (url, "jquery.js") )

import run
