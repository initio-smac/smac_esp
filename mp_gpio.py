# references
# https://forum.micropython.org/viewtopic.php?t=7162&start=10
# https://forum.micropython.org/viewtopic.php?t=7162
# page 59 of below pdf
# https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf

#OUT_MASK_BITS = 0b11111111111111111111111111111111
#integer equivalent of OUT_MASK_BITS  = 4294967296
#IN_MASK_BITS = 0b00000000000000000000000000000000

@micropython.viper
def set_gpio(pin:int):
    value = 1 << pin
    #OUT_MASK_BITS = 0b11111111111111111111111111111111
    OUT_MASK_BITS = int(4294967296)
    if pin < 32:
        GPIO_SET = ptr32(0x3FF44008 )
    else:
        GPIO_SET = ptr32(0x3FF44014)
    #GPIO_OUT = ptr32(0x3FF44004) # Read current state of GPIO Output register
    mask = OUT_MASK_BITS - value
    GPIO_SET[0] = (GPIO_SET[0] & mask) | value

@micropython.viper
def clear_gpio(pin:int):
    value = 1 << pin
    #OUT_MASK_BITS = 0b11111111111111111111111111111111
    OUT_MASK_BITS = int(4294967296)
    if pin < 32:
        GPIO_CLR = ptr32(0x3FF4400C )
    else:
        GPIO_CLR = ptr32(0x3FF44018)
    #GPIO_OUT = ptr32(0x3FF44004) # Read current state of GPIO Output register
    mask = OUT_MASK_BITS - value
    GPIO_CLR[0] = (GPIO_CLR[0] & mask) | value


@micropython.viper
def set_gpio_out(pin:int):
    value = 1 << pin
    OUT_MASK_BITS = int(4294967296)
    if pin < 32:
        GPIO_ENABLE_WR = ptr32(0x3FF44024 )
    else:
        GPIO_ENABLE_WR = ptr32(0x3FF44030 )
    #GPIO_ENABLE_OUT = ptr32(0x3FF44020) # GPIO Enable Output register
    mask = (OUT_MASK_BITS - value) 
    GPIO_ENABLE_WR[0] = (GPIO_ENABLE_WR[0] & mask) | value

@micropython.viper
def clear_gpio_out(pin:int):
    value = 1 << pin
    OUT_MASK_BITS = int(4294967296)
    if pin < 32:
        GPIO_ENABLE_CLR = ptr32(0x3FF44028 )
    else:
        GPIO_ENABLE_CLR = ptr32(0x3FF44034 )
    #GPIO_ENABLE_OUT = ptr32(0x3FF44020) # GPIO Enable Output register
    mask = (OUT_MASK_BITS - value) 
    GPIO_ENABLE_CLR[0] = (GPIO_ENABLE_CLR[0] & mask) | value

@micropython.viper
def get_output_gpio(pin:int) -> int:
    value = 1 << pin
    if pin < 32:
        GPIO_OUT = ptr32(0x3FF44004 )
    else:
        GPIO_OUT = ptr32(0x3FF44010 )
    #GPIO_OUT = ptr32(0x3FF44004) # GPIO Input register
    if (GPIO_OUT[0] &  value) == value:
        return 1
    return 0 

@micropython.viper
def get_input_gpio(pin:int) -> int:
    value = 1 << pin
    if pin < 32:
        GPIO_IN = ptr32(0x3FF4403C )
    else:
        GPIO_IN = ptr32(0x3FF44040 )
    if (GPIO_IN[0] &  value) == value:
        return 1 
    return 0


#from machine import Pin

#p = Pin(4, Pin.OUT)
#p.on()
#enable_gpio_out(2)
#set_gpio(2)
#print(p.value())
#while 1:
#    print( get_gpio(0b00000100000000000000000000000000) )
#    print( get_gpio(0b00000100000000000000000000000000) )
