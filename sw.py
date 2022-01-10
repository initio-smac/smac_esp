import debounce
from machine import Pin

def sw_open():
    print("SW open")

def sw_close():
    print("SW close")

p = Pin(13, Pin.IN, Pin.PULL_UP)
sw = debounce.Pushbutton(p)
sw.press_func(sw_open, ())
sw.release_func(sw_close, ())
