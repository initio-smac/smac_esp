import urequests as requests
from config import config
import json
import uos as os
import machine
import gc

def check_connection(*args):
    url = "https://smacsystem.com/download/esp32/version.json"
    req = requests.get(url)
    req.close()
    if req.status_code == 200:
        return True
    else:
        return False


def download_updates():
    try:
        DOWNLOAD_VERSION = config.get_config_file("download_version")
        config_old = {}
        invalid_version = [ "", None, "0", 0 ]
        with open('config.json', "r") as c1:
            config_old = json.load(c1)
            c1.close()
        
        if (DOWNLOAD_VERSION not in invalid_version):
            print("checking internet connection...")
            while not check_connection():
                pass
            print("downloading version: {}".format(DOWNLOAD_VERSION))
            url = "https://smacsystem.com/download/esp32/{}/files.json".format(DOWNLOAD_VERSION)
            print(url)
            req = requests.get(url)
            res = req.json()
            req.close()
            print(res)
            for f in res.keys():
                print("downloading file: {}, path: {}".format(f, res[f]))
                path = res[f]
                d_paths = path.split("/")
                
                if d_paths[0] != "":
                    print(d_paths)
                    try:
                        print("creating dir : {}".format(d_paths[0]) )
                        os.mkdir(d_paths[0])
                    except Exception as e:
                        print(e)
                    if len(d_paths) > 1:
                        for num, i in enumerate(d_paths):
                            #print(num)
                            #print(len(d_paths)-1)
                            if num < len(d_paths)-1:
                                try:
                                    print("creating dir : {}/{}".format(i, d_paths[num+1]) )
                                    os.mkdir("/{}/{}".format(i, d_paths[num+1]))
                                except Exception as e:
                                    print(e)
                    print(path)
                    u = "https://smacsystem.com/download/esp32/{}/{}/{}".format(DOWNLOAD_VERSION, path, f)
                else:
                    u = "https://smacsystem.com/download/esp32/{}/{}".format(DOWNLOAD_VERSION, f)
                #url_path = "{}/{}".format(path,f)
                
                print(u)
                req1 = requests.get(u)
                res1 = req1.text
                if req1.status_code == 200:
                    with open("{}/{}".format(path, f), "w" ) as f:
                        f.write(res1)
                req1.close()
                
                #print(res1)
                
            # update the variables
            try:
                print("updating new config file")
                con = {}
                with open('config.json', "r") as c1:
                    con = json.load(c1)
                    c1.close()

                with open('config.json', "w") as c2:
                    d = con.copy()
                    if d.get("download_version", None) != None:
                        del d["download_version"]
                    d["VERSION"] = DOWNLOAD_VERSION
                    d["SUB_TOPIC"] = config_old["SUB_TOPIC"]
                    d["ID_DEVICE"] = config_old["ID_DEVICE"]
                    d["NAME_DEVICE"] = config_old["NAME_DEVICE"]
                    d["AP_CONFIG"] = config_old["AP_CONFIG"]
                    d["WIFI_CONFIG"] = config_old["WIFI_CONFIG"]
                    d["MODE"] = 0
                    print(d)
                    c2.write(json.dumps(d))
                    c2.close()
            except Exception as e:
                print("update config file err: {}".format(e))
            gc.collect()
            print("\nSuccessfully downloaded version: {}\nRebooting...".format(DOWNLOAD_VERSION))
            machine.reset()
                    
        else:
            url = "https://smacsystem.com/download/esp32/version.json"
            req = requests.get(url)
            res = req.json()
            req.close()
            #print(res)
            ver = res.get("versions", [])
            if len(ver) > 0:
                config.update_config_file("VERSIONS", value=ver)
    except Exception as e:
        print(e)