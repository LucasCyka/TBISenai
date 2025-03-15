import serial
import dearpygui.dearpygui as dpg

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 350


class App:
    outputItem = None
    inputItem  = None
    portItem   = None
    ser        = None

    def __init__(self):
        self.initInterface()
        self.configSerial()
    
    def mycallback(self,sender,app_data,user_data): #user_data/:  occasionally UI items will send their own data (ex. file dialog)
        print("connecting...")

    def connectTest(self):
        print("connecting...")

    def testeBtn(self):
        pass

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
            dpg.add_text("nao conectado.",pos=(65,30),color=(255,0,0,255))

            dpg.set_colormap
            prt =  dpg.add_input_text(pos=(60,10),width=100,height=20,default_value="/dev/tty/USB0")
            
            
            #buttons
            dpg.add_button(label="Conectar",pos=(165,10))
            dpg.add_button(label="Teste Curva",pos=(0,60),width=100)
            dpg.add_button(label="Muda DC",pos=(100,60),width=100)
            dpg.add_button(label="Sensores",pos=(200,60),width=100)
            dpg.add_button(label="Teste",pos=(300,60),width=100)

            #tooltips
            with dpg.tooltip(prt):
                dpg.add_text("Endereço da porta serial.")
                
        with dpg.window(label="SAIDA",width=200,height=200,pos=(0,100),no_move=True,no_close=True):
            dpg.add_input_text(multiline=True,readonly=True,height=200,width=200)

        with dpg.window(label="ENTRADA",width=200,height=200,pos=(200,100),no_move=True,no_close=True):
            dpg.add_input_text(multiline=True,readonly=True,height=200,width=200)

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


    def configSerial(self):
        pass

    def configInterface(self):
        pass




app = App()

dpg.destroy_context()