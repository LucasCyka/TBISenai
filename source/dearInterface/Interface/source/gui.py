import dearpygui.dearpygui as dpg
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

plotxData  = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
plotyData1 = [0,1,2,3,4,5,5,5,5,5,4,3,2,1,0]
plotyData2 = [5,4,3,2,1,0,0,0,0,0,1,2,3,4,5]

class GUI():
    ser = None
    inter1 = None #font

    #ui elements
    portInput   = None
    modelInput  = None
    connectBtn  = None
    sensorBtn   = None
    saveBtn     = None
    startBtn    = None
    carImage    = None
    tbiImage    = None

    def __init__(self,ser):
        self.ser = ser

    def run(self):
        dpg.create_context()
        self.addFonts()
        self.addImages()
        self.doWindows()

        dpg.create_viewport(title = "Testador de TBI", width= globals.SCREEN_WIDTH, height=globals.SCREEN_HEIGHT,resizable=False) #OS WINDOW
        dpg.setup_dearpygui() # assign the viewport
        dpg.show_viewport()
        dpg.set_primary_window("root",True)
        #dpg.start_dearpygui() #start the loop
        #manual render loop
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            #loop here, update plots here maybe?

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
            self.portInput  = dpg.add_combo(self.ser.getPorts(self.ser),width=150,pos=(70,10))
            self.modelInput = dpg.add_combo(("Ford Ka 1.5/1.6","New Fiesta","Ford Focus"),width=150,pos=(480,10),callback=self.updateModel)

            #buttons
            self.connectBtn = dpg.add_button(label="Conectar",pos=(230,10),callback=self.onConnectBtn) 
            self.startBtn = dpg.add_button(label="INICIAR TESTE",pos=(150,110)) 
            self.sensorBtn = dpg.add_button(label="LER SENSORES",pos=(270,110)) 
            self.saveBtn = dpg.add_button(label="SALVAR GRÁFICO",pos=(395,110)) 

            #images
            self.carImage = dpg.add_image(texture_tag="placeholder",pos = (600,10),width=150,height=150)
            #self.tbiImage = dpg.add_image(texture_tag="tbi1",pos = (700,50),width=80,height=80)

            #plots
            with dpg.plot(label="Sensores de Posicao",width=780,height=440,pos=(0,150)):
                dpg.add_plot_legend()
                
                dpg.add_plot_axis(dpg.mvXAxis,label="t(ms)")
                dpg.add_plot_axis(dpg.mvYAxis,label="Tensão (V)",tag="tps1")
                dpg.add_plot_axis(dpg.mvYAxis2,label="Tensão (V)",tag="tps2",no_label=True,no_tick_labels=True)
                dpg.set_axis_limits("tps1",-0.1,6)
                dpg.set_axis_limits("tps2",-0.1,6)

                dpg.add_line_series(plotxData,plotyData1,parent="tps1",label="Pista 1")
                dpg.add_line_series(plotxData,plotyData2,parent="tps2",label= "Pista 2")

    
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

        

    def __exit__():
        dpg.destroy_context()