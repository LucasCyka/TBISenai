import tkinter as tk
import matplotlib
matplotlib.use("TkAgg") #backend for tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import serial
import time

f = Figure(figsize=(5,5),dpi = 100) #this figure widht x height in inches and resolution in dps per inch
a = f.add_subplot(111) #figure 1 subplot is a 1x1
PORT = '/dev/ttyACM0'

def animGraph(i):
    data = open("data.txt","r").read()
    dataArray =  data.split('\n')

    xar = []
    yar = []

    for line in dataArray:
        if len(line) > 1:
            x,y = line.split(',') 
            xar.append(int(x))
            yar.append(float(y))
    a.clear()
    a.plot(xar,yar) 

    a.set_ylim(0,8)

class MainInterface(tk.Tk):
    ser = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Testing Graphs")
        self.geometry("500x600")

        self.frames = {} #all frames I create go here

        mainContainer = tk.Frame(self)
        mainContainer.grid(column = 0, row = 0,sticky = "nsew")

        frame =  MainPage(mainContainer,self)

        self.frames[MainPage] = frame

        frame.pack(side="top",fill="both", expand =True)
        frame.columnconfigure(0,weight = 1)
        frame.rowconfigure(0,weight = 1)

    def show_page(self,p):
        frame = self.frames[p]
        frame.tkraise()

    def GetSamples(self): #get samples from serial port and write it to samples.txt
        samplesCount = 0
        x = []
        y = []

        if self.ser.in_waiting > 1:
            xline = 0
            while samplesCount < 320: #get 600 samples
                
                x.append(xline)
                val = self.ser.readline().decode('utf-8',errors = 'ignore').strip()
                if val.isdigit():
                    y.append(round(float(val) / 1023.0 * 5.0,4))
                    xline += 1
                    samplesCount += 1


            with open("data.txt", "w") as f:
                for xi, yi in zip(x, y):
                    f.write(f"{xi},{yi}\n")
            
            self.after(320, lambda: self.GetSamples()) #call again after sometime

    def ConnectSerial(self): #try to connect with the serial port
        self.ser = serial.Serial(PORT,9600)
        
        print("Connecting...")
        time.sleep(4)

        if self.ser.in_waiting > 0:
            print("serial port has data")
        else:
            print("no data found...")        
    

    def disconnectSerial(self):
        print("disconnecting...")
        self.ser.close()



class MainPage(tk.Frame):
    def __init__(self,parent,app):
        tk.Frame.__init__(self,parent)
        
        btn = tk.Button(self,text = "connect", command = lambda : app.ConnectSerial())
        btn.grid(row=0,column=0,sticky="nsew")

        btn2 = tk.Button(self,text = "plot", command = lambda : app.GetSamples())
        btn2.grid(row=0,column=1,sticky="nsew")

        btn3 = tk.Button(self,text = "disconnect", command = lambda : app.disconnectSerial())
        btn3.grid(row=0,column=2,sticky="nsew")

      
        #a.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,27,28,29,30,31,32],[
        #0,4,8,16,32,64,128,256,512,1024,2048,4096,8000,16000,32000,64000,124000,1,19,20,22,23,24,25,26,27,28,29,30,31,32])

        #graphical part, show it on the screen
        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)




app = MainInterface()
anim = animation.FuncAnimation(f,animGraph,interval=10)
app.mainloop()