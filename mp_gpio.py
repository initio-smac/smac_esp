# references
# https://forum.micropython.org/viewtopic.php?t=7162&start=10
# https://forum.micropython.org/viewtopic.php?t=7162
# page 59 of below pdf
# https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf

#OUT_MASK_BITS = 0b11111111111111111111111111111111
#IN_MASK_BITS = 0b00000000000000000000000000000000

@micropython.viper
def set_gpio(value:int):
    #OUT_MASK_BITS = 0b11111111111111111111111111111111
    OUT_MASK_BITS = int(4294967296)
    GPIO_OUT = ptr32(0x3FF44004) # GPIO Output register
    print(OUT_MASK_BITS)
    mask = (value & OUT_MASK_BITS) 
    GPIO_OUT[0] = (GPIO_OUT[0] & mask) | value


@micropython.viper
def enable_gpio_out(value:int):
    OUT_MASK_BITS = int(4294967296)
    GPIO_ENABLE_OUT = ptr32(0x3FF44020) # GPIO Enable Output register
    mask = (value & OUT_MASK_BITS) 
    GPIO_ENABLE_OUT[0] = (GPIO_ENABLE_OUT[0] & mask) | value


@micropython.viper
def get_gpio(value:int) -> int:
    IN_MASK_BITS = 0
    GPIO_IN = ptr32(0x3FF4403C) # GPIO Input register
    mask = (value & IN_MASK_BITS) 
    return (GPIO_IN[0] | mask) & value


from machine import Pin

p = Pin(4, Pin.OUT)
p.on()
enable_gpio_out(4)
set_gpio(4)
print(p.value())
#while 1:
#    print( get_gpio(0b00000100000000000000000000000000) )
#    print( get_gpio(0b00000100000000000000000000000000) )
