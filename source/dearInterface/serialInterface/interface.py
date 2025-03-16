import serial
import dearpygui.dearpygui as dpg
import time

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 350

START_BYTE    = 0x01
END_BYTE      = 0xAA

class App:
    connected   = False
    outputItem  = None
    inputItem   = None
    portItem    = None
    statusItem  = None
    btnTestItem = None
    ser         = serial.Serial()

    def __init__(self):
        self.initInterface()
        self.configSerial()
    
    def updateGuiStatus(self,status=0):
        match status:
            case 0:
                dpg.set_value(self.statusItem,"nao conectado...")
                dpg.configure_item(self.statusItem,color=(255,0,0,255))
            case 1:
                dpg.set_value(self.statusItem,"conectando...")
                dpg.configure_item(self.statusItem,color=(255,255,0,255))
            case 2:
                dpg.set_value(self.statusItem,"falha ao conectar, verifique a porta...")
                dpg.configure_item(self.statusItem,color=(255,0,0,255))
            case 3:
                dpg.set_value(self.statusItem,"conectado.")
                dpg.configure_item(self.statusItem,color=(0,255,0,255))
            case _:
                pass

    def configSerial(self):
        self.updateGuiStatus(status = 1)

        #configure serial port
        prt = str(dpg.get_value(self.portItem))
        self.ser.port          = prt
        self.ser.baudrate      = 115200
        self.ser.timeout       = 1
        self.ser.write_timeout = 1
        
        #attempt connection
        try:
            self.ser.open()
            time.sleep(2)
        except:
            self.updateGuiStatus(status = 2)
            return
        
        self.updateGuiStatus(status = 3)
        self.connected = True
        self.ser.reset_input_buffer()

    def mycallback(self,sender,app_data,user_data): #user_data/:  occasionally UI items will send their own data (ex. file dialog)
        dpg.set_value(self.outputItem, str(dpg.get_value(self.outputItem)) + 'test\n')

    def connectTest(self):
        if not self.connected: return

        try:
            self.ser.write(START_BYTE.to_bytes(1,'big'))
            self.ser.write(0x04.to_bytes(1,'big'))
            self.ser.write(0x00.to_bytes(1,'big'))
            self.ser.write(END_BYTE.to_bytes(1,'big'))
        except:
            cons = dpg.get_value(self.outputItem)
            cons = str(cons + '\n\n' 'Erro ao enviar mensagem')
            dpg.set_value(self.outputItem,cons)

        #updates output
        cons = dpg.get_value(self.outputItem)
        cons = str(cons + '\n\n'+ '0x01\n0x04\n0x00\n0xAA\nAguardando resposta do\nESP-32')
        dpg.set_value(self.outputItem,cons)

        time.sleep(1)

        ans = str(self.ser.readline().decode('utf-8',errors='ignore').strip())

        if ans == 'END':
            cons = dpg.get_value(self.outputItem)
            cons = str(cons +  '\n\nComando executado com\nsucesso')
            dpg.set_value(self.outputItem,cons)

            cons2 = dpg.get_value(self.inputItem)
            cons2 = str(cons2 +  '\n\n' + ans)
            dpg.set_value(self.inputItem,cons2)
        else:
            cons = dpg.get_value(self.outputItem)
            cons = str(cons + '\n\nSem resposta do ESP-32')
            dpg.set_value(self.outputItem,cons)
            print(ans)

    def curveTest(self):
        pass


    def initInterface(self):
        dpg.create_context() #always need to be created and destroyed
        #dpg.show_metrics()    

        #### WINDOWS ###
        #primary window -- do not mistake with the OS window (viewport)
        with dpg.window(tag="mainWindow"):
            dpg.add_text("Porta:",pos=(10,10),)
            dpg.add_text("Status:",pos=(10,30))
            dpg.add_text("1.0.0",pos=(10,SCREEN_HEIGHT-30))
            self.statusItem = dpg.add_text("nao conectado.",pos=(65,30),color=(255,0,0,255))

            dpg.set_colormap
            self.portItem =  dpg.add_input_text(pos=(60,10),width=100,height=20,default_value="/dev/ttyUSB0")
            
            
            #buttons
            dpg.add_button(label="Conectar",pos=(165,10),callback=self.configSerial)
            dpg.add_button(label="Teste Curva",pos=(0,60),width=100)
            dpg.add_button(label="Muda DC",pos=(100,60),width=100)
            dpg.add_button(label="Sensores",pos=(200,60),width=100)
            self.btnTestItem = dpg.add_button(label="Teste",pos=(300,60),width=100,callback=self.connectTest)

            #tooltips
            with dpg.tooltip(self.portItem):
                dpg.add_text("Endereço da porta serial.")
                
        with dpg.window(label="SAIDA",width=200,height=200,pos=(0,100),no_move=True,no_close=True):
            self.outputItem = dpg.add_input_text(multiline=True,readonly=True,height=200,width=200,tracked=True,track_offset=1.0,no_horizontal_scroll=True)
        with dpg.window(label="ENTRADA",width=200,height=200,pos=(200,100),no_move=True,no_close=True):
            self.inputItem  = dpg.add_input_text(multiline=True,readonly=True,height=200,width=200,tracked=True,track_offset=1.0,no_horizontal_scroll=True)

        #### DRAWING ###
        dpg.create_viewport(title='Emulador de Interface',width=SCREEN_WIDTH,height=SCREEN_HEIGHT) #OS window
        dpg.setup_dearpygui() #assign the viewport
        dpg.show_viewport()
        dpg.set_primary_window("mainWindow",True)
        dpg.start_dearpygui() #matains the loop
            
        # below replaces, start_dearpygui()
        #while dpg.is_dearpygui_running():
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            #print("this will run every frame")
            #dpg.render_dearpygui_frame()


app = App()
dpg.destroy_context()