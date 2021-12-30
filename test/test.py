from debounce import DebouncedSwitch
from machine import Pin

led = Pin(25, Pin.OUT)
p1 = Pin(26, Pin.IN)

def test(*args):
    print("changed", args)

#pp = DebouncedSwitch(p1, test, delay=25)

#p1.irq(handler=test,trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)