import os


#gui parameters
SCREEN_WIDTH   = 1024
SCREEN_HEIGHT  = 640

#serial communication
START_BYTE = 0x01
END_BYTE   = 0xAA

def get_base_dir():
    pass

def isLinux():
    return os.name == 'posix'