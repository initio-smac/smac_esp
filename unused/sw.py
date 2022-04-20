import debounce
from machine import Pin

def sw_open():
    print("SW open")

def sw_close():
    print("SW close")

def dbl_click():
    print("Double Click")

def long_press():
    print("Long Press")

import uasyncio as asyncio

p = Pin(33, Pin.IN, Pin.PULL_UP)
#sw = debounce.Switch(p)
#sw.open_func(sw_open, ())
#sw.close_func(sw_close, ())

sw1 = debounce.Pushbutton(p)
sw1.press_func(sw_open, ())
sw1.release_func(sw_close, ())
sw1.double_func(dbl_click, ())
sw1.long_press_ms = 5000
sw1.long_func(long_press, ())

async def my_app():
    await asyncio.sleep(60)


asyncio.run( my_app() )
