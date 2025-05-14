import serial
import serial.tools
import serial.tools.list_ports
import serial.tools.list_ports_linux
import time
from source import globals

class SERIAL():

    ser  = serial.Serial()
    busy = False

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

        ports.append("ATUALIZAR")
        return ports
    
    def connectTo(self,port):
        self.ser.port          = port
        self.ser.baudrate      = 230400
        self.ser.timeout       = 1
        self.ser.bytesize      = serial.EIGHTBITS
        self.ser.write_timeout = 1
        self.busy              = True

        try: 
            self.ser.open()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except:
            self.ser.close()
            self.busy = False
            return False
        
        time.sleep(1) 

        #check com
        try:
            self.ser.write(globals.START_BYTE.to_bytes(1,'big'))
            self.ser.write(0x05.to_bytes(1,'big'))
            self.ser.write(0x00.to_bytes(1,'big'))
            self.ser.write(globals.END_BYTE.to_bytes(1,'big'))
        except:
            self.ser.close()
            self.busy = False
            return False
        
        time.sleep(1) 

        #check mcu answer
        rawMsg = []
        conMsg = []

        try:
            rawMsg.append(self.ser.readline())
            time.sleep(1) 
            conMsg = self.convertMsg(self,rawMsg)
        except:
            self.ser.close()
            self.busy = False
            return False
        
        if not  conMsg[0] == 'ConnOk': 
            self.ser.close()
            self.busy = False
            return False
        
        self.busy = False
        return True

    def pingMcu(self):
        
        self.busy = True

        try:
            self.ser.write(globals.START_BYTE.to_bytes(1,'big'))
            self.ser.write(0x05.to_bytes(1,'big'))
            self.ser.write(0x00.to_bytes(1,'big'))
            self.ser.write(globals.END_BYTE.to_bytes(1,'big'))
        except:
            self.busy = False
            self.ser.close()
            return False
        
        #time.sleep(0.1)


        #check mcu answer
        rawMsg = []
        conMsg = []

        try:
            rawMsg.append(self.ser.readline())
            time.sleep(1) 
            conMsg = self.convertMsg(self,rawMsg)
        except:
            self.ser.close()
            self.busy = False
            return False
        
        if conMsg[0] == "ConnOk":
            self.busy = False
            print("pinging")
            return True
        
        self.busy = False
        return False
    
    def isConnected(self):
        return self.ser.is_open
    
    def isBusy(self):
        return self.busy

    def getCurrentPort(self):
        return self.ser.port
    
    def getSensorData(self):
        self.busy = True
        sensorValue = [-1.00,-1.00]

        try:
            self.ser.write(globals.START_BYTE.to_bytes(1,'big'))
            self.ser.write(0x0A.to_bytes(1,'big'))
            self.ser.write(0x00.to_bytes(1,'big'))
            self.ser.write(globals.END_BYTE.to_bytes(1,'big'))
        except:
            self.busy = False
            return sensorValue
        
        time.sleep(1)

        rawMsg = []
        rawMsg.append(self.ser.readline())
        rawMsg.append(self.ser.readline())
        rawMsg.append(self.ser.readline())

        time.sleep(0.5)
        
        if len(rawMsg) == 0: return sensorValue

        convMsg = self.convertMsg(self,rawMsg)
        
        if convMsg[0] == 'PowerError':
            self.busy = False
            return sensorValue #TODO: raise a warning to the interface
        
        if convMsg[0] == "END":
            sensorValue[0] = float(convMsg[1])
            sensorValue[1] = float(convMsg[2])

        self.busy = False
        return sensorValue

    def startCurveTest(self):
        self.busy = True
        try:
            self.ser.write(globals.START_BYTE.to_bytes(1,'big'))
            self.ser.write(0x04.to_bytes(1,'big'))
            self.ser.write(0x00.to_bytes(1,'big'))
            self.ser.write(globals.END_BYTE.to_bytes(1,'big'))
        except:
            self.busy = False
            return False
        
        time.sleep(1)

        rawMsg = []
        rawMsg.append(self.ser.readline())

        convMsg = self.convertMsg(self,rawMsg)
        
        if convMsg[0] == 'PowerError':
            self.busy = False
            return False #TODO: raise a warning to the interface

        if convMsg[0] == 'END': 
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

        self.busy = False
        return True

    def convertMsg(self,message):
        convertedMessage = []
        
        for msg in message:
            convertedMessage.append(msg.decode('utf-8',errors='ignore').strip())

        return convertedMessage
    
    def getLine(self): #just return a line from the uart
        return self.ser.readline().decode('utf-8',errors='ignore').strip()