import wifi_client2
from ntptime import time as tim
import time

offset = int(5.5*3600)
print(tim())
print( type(tim()) )
print(offset)
print(type(offset) )


t = time.localtime( tim()+offset )
print(t)