
try:
    import urequests as requests
    import uos as os
except:
    import requests

import gc

URL_RELEASES = "https://api.github.com/repos/initio-smac/smac_esp/releases"
URL_LATEST_RELEASE = "https://api.github.com/repos/initio-smac/smac_esp/releases/latest"
#URL_RELEASE_FILES = "https://api.github.com/repos/initio-smac/smac_esp/commits"
#URL_RELEASE_FILES = "https://api.github.com/repos/initio-smac/smac_esp/git/trees/a3751edbc92861fb75c48ba18c3bdce9167c25e5"
URL_RELEASE_FILES = "https://api.github.com/repos/initio-smac/smac_esp/contents?ref=01"
URL_FILE = "https://raw.githubusercontent.com/repos/initio-smac/smac_esp/0.1/wifi_client2.py"


class OTAUpdate():
    repo_owner = "initio-smac"
    repo_name = "smac_esp"
    tag_name = ""
    version_name = ""
    path = ""

    def __init__(self, repo_owner="", repo_name="", *args ):
        if repo_owner != "":
            self.repo_owner=repo_owner
        if repo_name != "":
            self.repo_name = repo_name

    def check_for_latest_version(self):
        URL = "https://api.github.com/repos/{}/{}/releases/latest".format(self.repo_owner, self.repo_name)
        try:
            req = requests.get(URL, headers= {'user-agent': 'micropython'})
            #print(req.text)
            res = req.json()
            if res.get("name", None) != None:
                self.version_name = res.get("name")
                self.tag_name = res.get("tag_name")
                req.close()
                return True
            else:
                req.close()
                return False
        except Exception as e:
            print("except while checking latest version: {}".format(e))
            return False


    def get_all_versions(self):
        URL = "https://api.github.com/repos/{}/{}/releases".format(self.repo_owner, self.repo_name)
        try:
            req = requests.get(URL, headers= {'user-agent': 'micropython'})
            arr = []
            res = req.json()
            for rel in res:
                if rel.get("name", None) != None:
                    arr.append( (res.get("name"), res.get("tag_name")) )
                    #self.version_name = res.get("name")
                    #self.tag_name = res.get("tag_name")
            req.close()
            return arr
        except Exception as e:
            print("except while getting all versions: {}".format(e))
            return []

    def create_dir(self, path):
        try:
            os.mkdir(path)
        except Exception as e:
            print("Can't create a dir, e:{}".format(e))
            #raise
            #return False


    def download_all_files(self, version, path=''):
        try:
            gc.collect()
            if(path != '') and (path != None):
                self.create_dir(path)
            print(path)
            URL = "https://api.github.com/repos/{}/{}/contents/{}?ref={}".format(self.repo_owner, self.repo_name, path, version)
            #else:
            #    URL = "https://api.github.com/repos/{}/{}/contents?ref={}".format(self.repo_owner, self.repo_name, version)
            print(URL)
            req = requests.get(URL, headers= {'user-agent': 'micropython'})
            for f in req.json():
                if f["type"] == "file":
                    print("downloading file: {}/{}".format(path, f["name"]))
                    #p = "/" if path=="" else path
                    new_path = path+"/" if(path!="") else path
                    self.download_file(filename=f["name"], url=f["download_url"], pathToSave=new_path, version=version)
                elif f["type"] == "dir":
                    #URL = "https://api.github.com/repos/{}/{}/contents?ref={}".format(self.repo_owner, self.repo_name, version)
                    new_path = (path + "/" + f["name"]) if(path != "") else (path + f["name"])
                    self.download_all_files(version, new_path)
            req.close()
            gc.collect()
        except Exception as e:
            print("except while getting all files: {}".format(e))

    def download_file(self, filename, version, url=None,  pathToSave=''):
        try:
            URL = "https://raw.githubusercontent.com/{}/{}/{}{}".format(self.repo_owner, self.repo_name, version+"/"+pathToSave, filename)
            print(URL)
            res = requests.get(URL)
            print("saving file to {}".format(pathToSave))
            with open("{}/{}".format(pathToSave, filename), "w") as f:
                f.write(res.text)
            res.close()
            gc.collect()
        except Exception as e:
            print("Exception while downloading file: {}. e:{}".format(filename, e))

    def test(self):
        req = requests.get(URL_RELEASE_FILES)
        try:
            res = req.json()
            #print(res)
            for i in res:
                print(i["name"])
                print(i["download_url"])
                print(i["type"])
            if res.get("name", None) != None:
                version_name = res.get("name")
                print("Update avaiable: version={}".format(version_name))
            else:
                print("No updates available")
        except Exception as e:
            print(e)
            print("No update abailable")

ota = OTAUpdate()
#ota.download_all_files(version="02")