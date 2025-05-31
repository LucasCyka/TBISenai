#!usr/bin/python

import serial
import tkinter as tk
import time
import matplotlib
matplotlib.use("TkAgg") #backend for tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

PORT = '/dev/ttyACM0'

class Interface(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("My window")
        self.geometry("320x200")

        container = tk.Frame(self) #creates a container as root (main window) as parent
        container.pack(side="top", fill="both", expand = True) #"packs" the frame inside the root against the right
        container.grid_rowconfigure(0,weight=1) #row x column with the same size
        container.grid_columnconfigure(0,weight=1)

        self.frames = {} #dictionary to store all frames (pages) that we create


        for page in (StartPage, Page2):

            frame = page(container,self) #creates a new frame as the main container as parent

            self.frames[page] = frame #store the frame created above and uses its class as index

            frame.grid(row=0,column=0,sticky="nsew") #frame will be put inside container with grid. will be 0x0

        self.show_frame(StartPage)

    def show_frame(self,f):
        frame = self.frames[f]
        frame.tkraise() #raise the given frame to show it


class StartPage(tk.Frame): #simply start page with a label widget
    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent) 
        label = tk.Label(self,text = "Goodbye, World", font = ("Arial",12)) #every widget here will be part of this frame
        label.pack(pady=10,padx=10)

        btn1 = tk.Button(self,text = "My button!", command = lambda : controller.show_frame(Page2))
        btn1.pack()


class Page2(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Welcome to page 2!", font = ("Arial", 12))
        label.pack(pady=10,padx=10)

        btn1 = tk.Button(self,text="Home",font=("Arial",12),command=lambda:controller.show_frame(StartPage))
        btn1.pack()

        f = Figure(figsize=(5,5),dpi = 100) #this figure widht x height in inches and resolution in dps per inch
        a = f.add_subplot(111) #figure 1 subplot is a 1x1
        a.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,27,28,29,30,31,32],[
        0,4,8,16,32,64,128,256,512,1024,2048,4096,8000,16000,32000,64000,124000,1,19,20,22,23,24,25,26,27,28,29,30,31,32])

        #graphical part, show it on the screen
        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand = True)



t = Interface()
t.mainloop()

"""

def setupInterface():
    window = tk.Tk()
    myLabel = tk.Label(text = "Goodbye, World!")
    myLabel.pack()
    
    window.mainloop()



setupInterface()

"""


"""

ser = serial.Serial(PORT,9600)

while True:
    if ser.in_waiting > 0:

        val = ser.read(4).decode('utf-8').strip()

        print(val)

        time.sleep(0.05)


ser.close()
"""