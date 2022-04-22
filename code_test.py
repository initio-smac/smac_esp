#this is a good program

from DEVICE.smac_keys import smac_keys

'''
this is multiline comments]
remove me during optimization
'''
test_var = 1000

'''
secondg comments
lines
remove this too
'''

"""
this is also commnets
remove me also
"""

def hell():
    a = 5 + 5
    print(a)  # a is a local variable
    b = a - 4
    # b is also a local variable
    print(b)
    print(smac_keys["CMD_ONLINE"])
    #smac_keys[""]
    d = {}
    d[ smac_keys["PROPERTY"] ] = "t1"
    d[ smac_keys["TO"] ] = "t2"
    d[ smac_keys["COMMAND"] ] = smac_keys["CMD_SET_PROPERTY"]
    print(d)
    pass

hell()
