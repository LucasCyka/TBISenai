import dearpygui.dearpygui as dpg
import threading
import time
from source import globals

images_data = {
    "car01" : {
        "data"    : None,
        "width"   : None,
        "height"  : None,
        "channels": None,
        "tag"     : "car1",
        "path"    : "images/car1.png"
        
    },
    "tbi01" : {
        "data"    : None,
        "width"   : None,
        "height"  : None,
        "channels": None,
        "tag"     : "tbi1",
        "path"    : "images/tbi01.png"
        
    },
    "placeholder" : {
        "data"    : None,
        "width"   : None,
        "height"  : None,
        "channels": None,
        "tag"     : "placeholder",
        "path"    : "images/placeholder.png"
        
    },
        "car2" : {
        "data"    : None,
        "width"   : None,
        "height"  : None,
        "channels": None,
        "tag"     : "car2",
        "path"    : "images/car2.png"
        
    },
        "car3" : {
        "data"    : None,
        "width"   : None,
        "height"  : None,
        "channels": None,
        "tag"     : "car3",
        "path"    : "images/car3.png"
        
    }
}

plotxData  = [0.0]
plotyData1 = [0.0]
plotyData2 = [5.0]
timing     = 0

class GUI():
    ser = None
    inter1 = None #font
    onCurveTest = False

    #ui elements
    portInput   = None
    modelInput  = None
    connectBtn  = None
    sensorBtn   = None
    saveBtn     = None
    startBtn    = None
    monitorBtn  = None
    helpBtn     = None
    Test2Btn    = None
    carImage    = None
    tbiImage    = None

    def __init__(self,ser):
        self.ser = ser

    def run(self):
        dpg.create_context()
        self.addFonts()
        self.addImages()
        self.doPopups()
        self.doWindows()

        dpg.create_viewport(title = "Testador de TBI", width= globals.SCREEN_WIDTH, height=globals.SCREEN_HEIGHT,resizable=False) #OS WINDOW
        dpg.setup_dearpygui() # assign the viewport
        dpg.show_viewport()
        dpg.set_primary_window("root",True)
        #dpg.start_dearpygui() #start the loop
        #manual render loop
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            if self.onCurveTest:
                
                dpg.set_value('p1',[plotxData,plotyData1])
                dpg.set_value('p2',[plotxData,plotyData2])
                dpg.set_item_label('p1', 'Pista 1')
                dpg.set_item_label('p2', 'Pista 2')

    def updatePlotData(self):
        while self.onCurveTest:
            global timing
            
            tps1 = self.ser.getLine(self.ser)
            tps2 = self.ser.getLine(self.ser)

            if tps1 == 'END' or tps2 == 'END':
                self.onCurveTest = False
                continue 

            if tps1 == '' or tps2 == '': continue #avoid noise error
            
            interval = (time.perf_counter() - timing) * 1000

            plotxData.append(interval)
            plotyData1.append(float(tps1) * 2.0)
            plotyData2.append(float(tps2) * 2.0)

            

    # create all windows that are necessary here
    def doWindows(self):
        with dpg.window(tag="root"):
            #text
            dpg.add_text("Porta: ",pos=(10,10),tag="PortLabel")
            dpg.add_text("Modelo: ",pos=(400,10),tag="ModelLabel")
            dpg.add_text("Status: Não conectado",pos=(10,40),tag="StatusLabel")
            dpg.add_text("Pista 1: 0,0V",pos=(10,100),tag="TPS1Label")
            dpg.add_text("Pista 2: 0,0V",pos=(10,120),tag="TPS2Label")

            #combos
            self.portInput  = dpg.add_combo(self.ser.getPorts(self.ser),width=150,pos=(70,10),callback=self.updatePorts)
            self.modelInput = dpg.add_combo(("Ford Ka 1.5/1.6","New Fiesta","Ford Focus"),width=150,pos=(480,10),callback=self.updateModel)

            #buttons
            self.connectBtn = dpg.add_button(label="Conectar",pos=(230,10),callback=self.onConnectBtn) 
            self.startBtn   = dpg.add_button(label="INICIAR TESTE",pos=(150,110),callback=self.onStartBtn,width=110) 
            self.sensorBtn  = dpg.add_button(label="LER SENSORES",pos=(270,110),callback=self.onReadBtn,width=116) 
            self.saveBtn    = dpg.add_button(label="SALVAR GRÁFICO",pos=(395,110),callback=self.onSaveBtn,width=135) 
            self.monitorBtn = dpg.add_button(label="MONITORAR",pos=(150,80),width=110) 
            self.Test2Btn   = dpg.add_button(label="ACELERAR",pos=(270,80),width=116) 
            self.helpBtn    = dpg.add_button(label="MANUAL",pos=(395,80),width=135) 

            #images
            self.carImage = dpg.add_image(texture_tag="placeholder",pos = (600,10),width=150,height=150)
            #self.tbiImage = dpg.add_image(texture_tag="tbi1",pos = (700,50),width=80,height=80)

            #plots
            with dpg.plot(label="Sensores de Posição",width=780,height=440,pos=(0,150)):
                dpg.add_plot_legend()
                
                dpg.add_plot_axis(dpg.mvXAxis,label="t(ms)",auto_fit=True)
                dpg.set_axis_limits(dpg.last_item(), 0, 12000)
                dpg.add_plot_axis(dpg.mvYAxis,label="Tensão (V)",tag="tps1",auto_fit=True)
                dpg.add_plot_axis(dpg.mvYAxis2,label="Tensão (V)",tag="tps2",no_label=True,no_tick_labels=True,auto_fit=True)
                dpg.set_axis_limits("tps1",-0.1,6)
                dpg.set_axis_limits("tps2",-0.1,6)

                dpg.add_line_series(plotxData,plotyData1,parent="tps1",label="Pista 1",tag='p1')
                dpg.add_line_series(plotxData,plotyData2,parent="tps2",label= "Pista 2",tag='p2')

    #create all popups that may appear to the user here
    def doPopups(self):
        with dpg.window(label="Warning1",modal=True,show=False,tag="warning1",no_title_bar=True,width= 300,height=100,pos=(globals.SCREEN_WIDTH/2-150,globals.SCREEN_HEIGHT/2-50),no_resize=True):
            dpg.add_text("Selecione o modelo de carro!",pos=(50,20))
            dpg.add_button(label="OK",pos=(125,60),width=50,callback=lambda: dpg.configure_item("warning1",show=False))

        with dpg.window(label="Warning2",modal=True,show=False,tag="warning2",no_title_bar=True,width= 300,height=100,pos=(globals.SCREEN_WIDTH/2-150,globals.SCREEN_HEIGHT/2-50),no_resize=True):
            dpg.add_text("Conecte-se ao testador primeiro!",pos=(40,20))
            dpg.add_button(label="OK",pos=(125,60),width=50,callback=lambda: dpg.configure_item("warning2",show=False))

        with dpg.window(label="Warning3",modal=True,show=False,tag="warning3",no_title_bar=True,width= 300,height=100,pos=(globals.SCREEN_WIDTH/2-150,globals.SCREEN_HEIGHT/2-50),no_resize=True):
            dpg.add_text("Sem resposta do testador!",pos=(60,20))
            dpg.add_button(label="OK",pos=(125,60),width=50,callback=lambda: dpg.configure_item("warning3",show=False))

        with dpg.window(label="Warning4",modal=True,show=False,tag="warning4",no_title_bar=True,width= 400,height=100,pos=(globals.SCREEN_WIDTH/2-200,globals.SCREEN_HEIGHT/2-50),no_resize=True):
            dpg.add_text("Falha nos sensores. Verifique a conexão com o TBI.",pos=(25,20))
            dpg.add_button(label="OK",pos=(170,60),width=50,callback=lambda: dpg.configure_item("warning4",show=False))

        #file dialog popups
        dpg.add_file_dialog(directory_selector=True,show=False,callback=self.saveGraph,tag="graph_dialog",
            width=600,height=300,)

    def onStartBtn(self):
        if not self.ser.isConnected(self.ser):
            dpg.configure_item("warning2",show=True)
            return
        
        if dpg.get_value(self.modelInput) == '':
            dpg.configure_item("warning1",show=True)
            return
        
        if self.ser.startCurveTest(self.ser):
            self.onCurveTest = True
            global timing
            global plotxData
            global plotyData1
            global plotyData2
            timing = time.perf_counter()
            plotxData  = [0.0]
            plotyData1 = [0.0]
            plotyData2 = [5.0]
            threading.Thread(target=self.updatePlotData,daemon=True).start()
        #TODO: check power supply with esp
        

    def onConnectBtn(self):
        portValue = dpg.get_value(self.portInput)
        if portValue == '': 
            dpg.set_value("StatusLabel","Selecione uma porta.")
            dpg.configure_item("StatusLabel",color=(255,255,0,255))
            return

        if self.ser.isConnected(self.ser):
            dpg.set_value("StatusLabel","Conexão já estabelicida.")
            dpg.configure_item("StatusLabel",color=(0,255,0,255))
            return

        dpg.set_value("StatusLabel","Conectando...")
        dpg.configure_item("StatusLabel",color=(255,255,0,255))

        if self.ser.connectTo(self.ser,portValue):
            dpg.set_value("StatusLabel","Conexão estabelecida.")
            dpg.configure_item("StatusLabel",color=(0,255,0,255))
        else:
            dpg.set_value("StatusLabel","Falha ao conectar.")
            dpg.configure_item("StatusLabel",color=(255,0,0,255))

    def onSaveBtn(self):
        dpg.show_item("graph_dialog")

    def onReadBtn(self):
        if not self.ser.isConnected(self.ser):
            dpg.configure_item("warning2",show=True)
            return
        
        val = self.ser.getSensorData(self.ser)

        if val[0] <= 0 and val[1] <= 0:
            dpg.configure_item("warning3",show=True)
            return
        
        dpg.set_value(item="TPS1Label",value="Pista 1: " + str(val[0]) + "V")
        dpg.set_value(item="TPS2Label",value="Pista 2: " + str(val[1]) + "V")

        if(val[0] < 0.2 or val[1] < 0.2):
            dpg.configure_item("warning4",show=True)
            return
        

    def saveGraph(self,sender,app_data):
        dir = app_data['file_path_name']

        with open(dir + '/horizontal.txt','w') as file:
            for line in plotxData:
                file.write(f"{line}\n")

        with open(dir + '/pista1.txt','w') as file:
            for line in plotyData1:
                file.write(f"{line}\n")

        with open(dir + '/pista2.txt','w') as file:
            for line in plotyData2:
                file.write(f"{line}\n")

    def test(self):
        print("this is a test")
        #dpg.configure_item(self.carImage,texture_tag="car1")
       
    def addFonts(self):
        with dpg.font_registry():
            self.inter1 = dpg.add_font(file="fonts/Inter_18pt-Light.ttf",size=18)
            dpg.bind_font(self.inter1) #global binding
             # dpg.bind_item_font(b2, second_font) # when item binding


    def addImages(self):
        
        for key in images_data:

            images_data[key]["width"], images_data[key]["height"], images_data[key]["channels"], images_data[key]["data"] = dpg.load_image(images_data[key]["path"])
        

        with dpg.texture_registry(show=False):

            for key in images_data:
                
                _width    = images_data[key]["width"]
                _height   = images_data[key]["height"]
                _channels = images_data[key]["channels"]
                _data     = images_data[key]["data"]
                _tag      = images_data[key]["tag"]

                dpg.add_static_texture(width=_width,height=_height,default_value=_data,tag=_tag)

    def updateModel(self):
        val = dpg.get_value(self.modelInput)

        match val:
            case "New Fiesta":
                dpg.configure_item(self.carImage,texture_tag="car2")
            case "Ford Focus":
                dpg.configure_item(self.carImage,texture_tag="car3")
            case "Ford Ka 1.5/1.6":
                dpg.configure_item(self.carImage,texture_tag="car1")
            case __:
                pass

    def updatePorts(self):
        val = dpg.get_value(self.portInput)
        
        if val == "ATUALIZAR": #it means the user wants to get all ports available
            dpg.configure_item(self.portInput,items=self.ser.getPorts(self.ser))
            dpg.set_value(self.portInput,"")

    def __exit__():
        dpg.destroy_context()