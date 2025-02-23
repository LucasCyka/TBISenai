import serial
import time

class app:

    commands = {
        '4.1':0x02
    }


    port = '/dev/ttyUSB0'
    baud = 115200
    ser  = serial.Serial()

    STARTBYTE = 0x01
    ENDBYTE   = 0xAA

    def __init__(self):
        print("********* Emulador de Interface *********")
        print("Programa para simular a troca de dados entre o ESP32 e a interface.")
        self.getPort()
        self.getBaud()
        if not self.configSerial():
            print("Erro: Conexão serial nao estabelecida...")
            print("Finalizando programa...")
            return
        else:
            print("Conexao estabelecida com sucesso...")
            option = '0'

            while option != '2': 
                option = self.showMenu()

                if option == '1':
                    self.showCMenu()

        self.ser.close()
        return

                
    def getPort(self):
        self.port = input("Digite a porta serial (PADRAO: /dev/ttyUSB0): ")
        if self.port == '':
            self.port = '/dev/ttyUSB0'
            print("Usando /dev/ttyUSB0 padrao.")

    def getBaud(self):
        self.baud = input("Digite o baud rate (PADRAO: 115200): ")
        if self.baud == '':
            self.baud = 115200
            print("Usando 115200")
        pass
    
    def configSerial(self):
        self.ser.port      = self.port
        self.ser.baudrate  = self.baud
        self.ser.timetout  = 1
        self.write_timeout = 1
        connected = True
 
        try :
            self.ser.open()
            time.sleep(2)
        except:
            connected = False

        return connected

    def showMenu(self):
        print("********* Emulador de Interface - Conectado a porta %s *********" % self.port)
        print("Selecione uma opcao: ")
        print("[1] Enviar comando")
        print("[2] Sair")

        return input("Opcao: ")

    def showCMenu(self):
        success = True
        for command in self.commands.keys():
            print(command)

        usrcmd = input("Escolha o comando: ")
        usrDat = input("Dados (em inteiro): ")

        cmd = self.commands[usrcmd].to_bytes(1,'big')
        dat = int(usrDat).to_bytes(1,'big')

        print("Enviando comando...")

        try:
            self.ser.write(self.STARTBYTE.to_bytes(1,'big'))
            self.ser.write(cmd)
            self.ser.write(dat)
            self.ser.write(self.ENDBYTE.to_bytes(1,'big'))
        except:
            success = False


        if success: print("Comando enviado com sucesso.")
        else: print("Erro ao enviar comando.")

        #a = 0x02
        #self.ser.write(a.to_bytes(1,'big'))



myApp = app()