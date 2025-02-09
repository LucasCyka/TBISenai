import tkinter as tk
from tkinter import ttk


class MainInterface(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)

        self.title("Pages Example")
        self.geometry("320x200")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.columnconfigure(0,weight=1)
        container.rowconfigure(0,weight=1)

        self.frames = {}

        for page in (PageOne, PageTwo, PageThree):

            frame = page(container,self)

            self.frames[page] = frame

            frame.grid(row = 0, column = 0,sticky = "nsew")


        self.show_page(PageOne)
        frame = PageOne(container,self)

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

class PageOne(tk.Frame):
    def __init__(self,parent,base):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self,text="Welcome to page one!")
        label.pack(pady=10,padx=10)

        button = ttk.Button(self,text = "Page 2",command = lambda : base.show_page(PageTwo))
        button.pack(pady=10,padx=10)

class PageTwo(tk.Frame):
    def __init__(self,parent,base):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self,text="Welcome to page two!")
        label.pack(pady = 10, padx = 10)

        button = tk.Button(self,text = "Home",command = lambda : base.show_page(PageOne))
        button.pack(pady = 10, padx = 10)

        button2 = tk.Button(self,text = "Page 3",command = lambda : base.show_page(PageThree))
        button2.pack(pady = 10, padx = 10)

class PageThree(tk.Frame):
    def __init__(self,parent,base):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self,text="Welcome to page three!")
        label.pack(pady = 10, padx = 10)

        button = tk.Button(self,text = "Home",command = lambda : base.show_page(PageOne))
        button.pack(pady = 10, padx = 10)

        button2 = tk.Button(self,text = "Page 2",command = lambda : base.show_page(PageTwo))
        button2.pack(pady = 10, padx = 10)


window = MainInterface()
window.mainloop()