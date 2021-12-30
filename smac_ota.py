import gc

from machine import Pin
import machine

from http_client import HttpClient
import utime
import utarfile
import uos
from config import config

# tar creation
# tar -cf <name.tar> <file1> <file2> <dir1> <dir2>
# tar -cf esp32.tar file1

class TarExtracter:

    def extract(self, file):
        t = utarfile.TarFile(file)
        for i in t:
            print("Extracting: {}".format(i.name) )
            if i.type == utarfile.DIRTYPE:
                if i.name[-1] == "/":
                    try:
                        uos.mkdir(i.name[:-1])
                    except Exception as e:
                        print(e)
            else:
                f = t.extractfile(i)
                with open(i.name, "wb") as f1:
                    f1.write(f.read())
        uos.remove(file)
        gc.collect()



class SmacOTA:
    client = HttpClient()
    SMAC_NEW_UPDATE_URL = "https://smacsystem.com/download/esp32/"
    DOWNLOAD_COMPLETE = 0
    CHUNK_SIZE = 512

    def toggle_pin(self, pin):
        led = Pin(pin, Pin.OUT)
        while not self.DOWNLOAD_COMPLETE:
            led.on()
            utime.sleep(.5)
            led.off()
            utime.sleep(.5)
        led.off()

    def get_update_version(self):
        gc.collect()
        print("checking for updates...")
        FILENAME =  "version.json"
        url = self.SMAC_NEW_UPDATE_URL + FILENAME
        #try:
        resp = self.client.request(method="GET", url=url)
        print(resp)
        if resp.status_code == 200:
            return resp.json()["version"]

        return -1
        #except Exception as e:
        print("Error while checking for updates", e)
        return -1



    def download_update(self, version):
        print("downloading software2...")
        self.DOWNLOAD_COMPLETE = 0
        FILENAME = "esp32_v{}.tar".format(version)
        url = self.SMAC_NEW_UPDATE_URL + FILENAME
        #_thread.start_new_thread(self.toggle_pin, (2,))
        try:
            resp = self.client.request(method="GET", url=url, saveToFile=FILENAME)
            if resp.status_code == 200:
                ext = TarExtracter()
                ext.extract(FILENAME)
                config.update_config_variable(key="version", value=version)
                self.DOWNLOAD_COMPLETE = 1
                print("Software Update is success. Rebooting Device...")
            else:
                self.DOWNLOAD_COMPLETE = 1
                print("cannnot initiate Software Update.", resp.reason)
        except Exception as e:
            print("Error while downloadin update", e)
            self.DOWNLOAD_COMPLETE = 1
        utime.sleep(2)
        config.update_config_variable(key="mode", value=0)
        machine.reset()


    # old method, dont use it
    def download_update2(self):
        print("downloading software...")
        self.DOWNLOAD_COMPLETE = 0
        url = self.SMAC_NEW_UPDATE_URL + "files.txt"
        #url = "https://smacsystem.com/download/esp32/new/files.txt"
        #url = "https://mpython.readthedocs.io/en/master/library/mPython/urequests.html"
        resp = self.client.request(method="GET", url=url)
        #gc.collect()
        if resp.status_code == 200:
            dat = resp.text.split("\n")
            #_thread.start_new_thread(self.toggle_pin, (2,))
            #print(dat)
            for f in dat:
                file_name, file_path = f.split(",")
                file_url = self.SMAC_NEW_UPDATE_URL + file_path
                self.download_file(file_url, file_path)
                #if not downloaded:
                #    self.DOWNLOAD_COMPLETE = 1
                #    print("Cannot download file: {}. Aborting Software Update.".format(file_name))
                #    #break
                #    gc.collect()
                #    return
                gc.collect()
                utime.sleep(5)
            self.DOWNLOAD_COMPLETE = 1
            print("Software Update is success. Rebooting Device...")
            utime.sleep(2)
            config.update_config_variable(key="mode", value=0)
            machine.reset()
        else:
            print("cannnot initiate Software Update.", resp.reason)
        resp.close()

smacOTA = SmacOTA()
