import os


#gui parameters
SCREEN_WIDTH   = 800
SCREEN_HEIGHT  = 600

#serial communication
START_BYTE = 0x01
END_BYTE   = 0xAA

def get_base_dir():
    pass

def isLinux():
    return os.name == 'posix'