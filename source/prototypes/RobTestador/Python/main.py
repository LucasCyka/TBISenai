import serial
import os
import time

class app:
    STARTBYTE = 0x01
    ENDBYTE   = 0xAA
    
    ser       = serial.Serial()
    connected = False
    port      = '/dev/ttyS0'

    def __init__(self):
        self.appLoop()
    
    def appLoop(self):
        option = 1
        os.system('clear' if os.name == 'posix' else 'cls')
        while option != 0:
            self.showMainMenu()
            
            usrInput = input("Escolha uma opcao: ")

            if not usrInput.isdigit():
                print("Digite um numero de 0 a 3")
                continue

            option = int(usrInput)

            match option:
                case 1:
                    self.showConnectionScreen()
                case 2:
                    self.showTestScreen()
                case _:
                    pass
        if self.ser.is_open:self.ser.close()
            

    def showMainMenu(self):
        print("*************** Testador de TBI automotivo - Menu principal ***************")
        print("STATUS:", end = ' ')
        if not self.connected: print("Testador não conectado. ")
        else: print("ESP32 conectado na porta %s" % self.ser.port)
        
        print(" ")

        print("[1] Conectar testador")
        print("[2] Testar borboleta")
        print("[3] Valor das pistas")
        print("[0] Sair")

        print(" ")

    def showConnectionScreen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        com  =  '/dev/ttyUSB0'
        baud =  115200

        print("*************** Tela de conexão ***************")
        print(" ")
        usrInput = input("Digite o nome da porta (PADRAO: /dev/ttyUSB0): ")
        if usrInput != '': com = usrInput
        print("Conectando...")
        self.ser.port = com
        self.ser.baudrate = baud
        self.ser.timeout  = 1
        self.ser.write_timeout = 1
        try:
            self.ser.open()
            time.sleep(2)
            
        except:
            print("Falha ao conectar com o testador... Tecle enter para retornar ao menu principal ")
            self.connected = False
            usrInput = input(" ")
            return


        print("Conectado com o testador na porta %s " % com)
        self.connected = True
        usrInput = input("")

    def showTestScreen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        self.ser.reset_input_buffer()
        if not self.ser.is_open:
            print("Testador nao conectado... Pressione enter para voltar ao menu principal")
            self.connected = False
            usrInput = input(" ")
            return
        print("*************** Testar borboleta ***************")
        print(" ")

        print("[1] Iniciar teste ")
        print("[2] voltar ao menu principal ")

        print(" ")

        try:
            self.ser.write(self.STARTBYTE.to_bytes(1,'big'))
            self.ser.write(0x0A.to_bytes(1,'big'))
            self.ser.write(0x00.to_bytes(1,'big'))
            self.ser.write(self.ENDBYTE.to_bytes(1,'big'))
        except:
            print("Nao foi possivel solicitar os sensores do testador.")
            usrInput = input("")
            return
        
        initialReadings = []
        try:
            initialReadings.append(self.ser.readline())
            initialReadings.append(self.ser.readline())
        except:
            print("Testador nao esta respondendo...")
            usrInput = input("")
            return

        tps1 = float(initialReadings[0].decode('utf-8',errors='ignore').strip()) * 2.0
        tps2 = float(initialReadings[1].decode('utf-8',errors='ignore').strip()) * 2.0

        print("PISTA 1: %.2fV" % tps1)
        print("PISTA 2: %.2fV" % tps2)

        print(" ")

        usrInput = input("Digite uma opcao: ")

        if not usrInput.isdigit():
            print("Digite um numero de 1 a 2")
            return
        
        if int(usrInput) == 1:
            #start test here
            try:
                self.ser.write(self.STARTBYTE.to_bytes(1,'big'))
                self.ser.write(0x02.to_bytes(1,'big'))
                self.ser.write(0x32.to_bytes(1,'big'))
                self.ser.write(self.ENDBYTE.to_bytes(1,'big'))
            except:
                print("Falha ao enviar comando para testador. Verifique a conexao e tente novamente.")
                usrInput = input(" ")
                return
        else:
            return

           

        #read what he sends back
        readings= []
        readings.append(self.ser.readline())

        readings.append(tps1)
        readings.append(tps2)

        stop = False
        lastScrUpdt = time.time_ns() / 1000000

        time.sleep(0.015) #wait 15 mileseconds before reading responses
        os.system('clear' if os.name == 'posix' else 'cls')
        while not stop:
            val = self.ser.readline()
            val = val.decode('utf-8',errors='ignore').strip()

            #try if val received is float
            isFloat = True
            valConverted =None
            try:
                valConverted = float(val)
            except:
                isFloat = False

            if isFloat:
                valConverted *= 2
                readings.append(valConverted)

                if ((time.time_ns() / 1000000) - lastScrUpdt) > 100:
                    #updates screen
                    lastScrUpdt = time.time_ns() / 1000000
                    os.system('clear' if os.name == 'posix' else 'cls')
                    #print("valor recebido: %.2f" % valConverted)
                    if(len(readings) % 2 == 0):
                        print("TPS1: %.2fV" % readings[len(readings) -2])
                        print("TPS2: %.2fV" % readings[len(readings) -1])
                    else:
                        print("TPS1: %.2fV" % readings[len(readings) -1])
                        print("TPS2: %.2fV" % readings[len(readings) -2])
                time.sleep(0.025)
            else:
                if val == "STOP":
                    stop = True
                    
                    #create data files
                    with open('TPS1.txt', 'w') as file:
                        id = 0
                        for line in readings:
                            if id % 2 == 0:
                                file.write(f"{line}\n")
                            id += 1
                                
                    with open('TPS2.txt', 'w') as file:
                        id = 0
                        for line in readings:
                            if id % 2 != 0:
                                file.write(f"{line}\n")
                            id += 1
                                
                    
                    print("Teste finalizado. Pressione enter para voltar ao menu principal.")
                    usrInput = input("")
                    return
                else: 
                    continue
                pass

        """
        while self.ser.in_waiting > 0:
            readings1.append(self.ser.readline())
            readings2.append(self.ser.readline())
            os.system('clear' if os.name == 'posix' else 'cls')
            print("*************** Testar borboleta ***************")
            print(" ")
            print("Teste em execucao...")
            print(" ")
            tps1 = float(readings1[len(readings1) -1].decode('utf-8',errors='ignore').strip()) * 2.0
            tps2 = float(readings2[len(readings2) -1].decode('utf-8',errors='ignore').strip()) * 2.0

            print("PISTA 1: %.2f " % tps1)
            print("PISTA 2: %.2f " % tps2)


        with open('data1.txt', 'w') as f:
            for line in readings1:
                f.write(f"{line.decode('utf-8',errors='ignore').strip()}\n")

        with open('data2.txt', 'w') as f:
            for line in readings2:
                f.write(f"{line.decode('utf-8',errors='ignore').strip()}\n")
        """


myApp = app() 