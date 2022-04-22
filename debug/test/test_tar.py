#import sys
import uos
#import shutil
import utarfile

t = utarfile.TarFile("esp32.tar")
for i in t:
    print(i)
    if i.type == utarfile.DIRTYPE:
        if i.name[-1] == "/":
            uos.mkdir(i.name[:-1])
    else:
        f = t.extractfile(i)
        #print(f)
        #shutil.copyfileobj(f, open(i.name, "wb"))
        with open(i.name, "wb") as f1:
            f1.write(f.read())