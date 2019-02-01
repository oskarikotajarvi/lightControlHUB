from tkinter import*

class Slider(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        self.slider = Scale(
            parent, from_=0, to=100, font=('Helvetica', 24), fg='white', orient=HORIZONTAL, troughcolor='grey', length=2000, bg='black',  label='Light dimmer',highlightthickness=0)
        self.slider.pack(side=BOTTOM, anchor=E, pady=50, padx=200)
