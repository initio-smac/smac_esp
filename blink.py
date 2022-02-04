from machine import Pin
import time
LED_PIN = 25

def device_boot_blink_led():
    LED = Pin(LED_PIN, Pin.OUT)
    i = 0
    while i <= 4:
        LED.on()
        time.sleep(.1)
        LED.off()
        time.sleep(.1)
        i += 1

def blink_led():
    LED = Pin(LED_PIN, Pin.OUT)
    while 1:
        LED.on()
        time.sleep(.1)
        LED.off()
        time.sleep(.1)