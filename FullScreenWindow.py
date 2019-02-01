from tkinter import *
from clock import Clock
from slider import Slider
from weather import Weather
from PIL import Image, ImageTk

class FullScreenWindow:
    def __init__(self):
        self.tk = Tk()
        #self.tk.configure(background='black')
        #self.topFrame = Frame(self.tk, background='black')
        #self.bottomFrame = Frame(self.tk, background='black')
        #self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        #self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        #self.state = False
        self.tk.geometry("{0}x{1}+0+0".format(
            self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.tk.attributes('-fullscreen', True)
        self.fname = 'assets/rpi_bg.png'#'assets/rpi_bg.png'
        self.bg_image = ImageTk.PhotoImage(file=self.fname)
        self.cv = Canvas(width=self.tk.winfo_screenwidth(), height=self.tk.winfo_screenheight(), highlightthickness=0)
        self.cv.pack(side=TOP, fill=BOTH, expand=YES)
        self.cv.create_image(0, 0, image=self.bg_image, anchor=NW)

        self.topFrame = Frame(self.cv, background='')
        self.bottomFrame = Frame(self.cv, background='')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

        #Clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)

        #Slider
        self.slider = Slider(self.bottomFrame)
        self.slider.pack(side=BOTTOM, anchor=CENTER)

        #Weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
