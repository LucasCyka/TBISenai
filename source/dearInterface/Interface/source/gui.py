import dearpygui.dearpygui as dpg
from source import globals

class GUI():
    ser = None
    def __init__(self,ser):
        self.ser = ser

    def run(self):
        dpg.create_context()

        self.doWindows()

        dpg.create_viewport(title = "Testador de TBI", width= globals.SCREEN_WIDTH, height=globals.SCREEN_HEIGHT) #OS WINDOW
        dpg.setup_dearpygui() #assign the viewport
        dpg.show_viewport()
        dpg.set_primary_window("root",True)
        dpg.start_dearpygui()

    #create all windows that are necessary here
    def doWindows(self):
        with dpg.window(tag="root"):
            dpg.add_text("test",pos=(0,0))
    
    def __exit__():
        dpg.destroy_context()