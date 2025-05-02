import serial
import serial.tools
import serial.tools.list_ports
import serial.tools.list_ports_linux
import time
from source import globals

class SERIAL():

    ser = serial.Serial()

    def __init__(self):
        pass

    def run(self):
        pass
    """
        print(serial.tools.list_ports_linux.comports(False)[0].name)
        print(serial.tools.list_ports_linux.comports(False)[1].name)
        print(serial.tools.list_ports_linux.comports(False)[2].name)
        print(serial.tools.list_ports_linux.comports(False)[3].name)"
    """

    def getPorts(self):
        ports = []
        linux = globals.isLinux()
        for port in serial.tools.list_ports.comports(True):

            n = port.name

            if linux: n = '/dev/' + n

            ports.append(n)


        return ports
    
    def connectTo(self,port):
        self.ser.port          = port
        self.ser.baudrate      = 115200
        self.ser.timeout       = 1
        self.ser.bytesize      = serial.EIGHTBITS
        self.ser.write_timeout = 1
        
        try: 
            self.ser.open()
        except:
            return False
        

        time.sleep(2) 

        return True
    
    def isConnected(self):
        print(self.ser.is_open)
        return self.ser.is_open
    
    
    def getCurrentPort(self):
        return self.ser.port