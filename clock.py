from tkinter import *
import time

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='')
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', 94), fg='white', bg='black')
        self.timeLbl.pack(side=TOP, anchor=E)
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', 28), fg='white', bg='black')
        self.dayOWLbl.pack(side=TOP, anchor=E)
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', 18), fg='white', bg='black')
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        time2 = time.strftime('%H:%M')
        day_of_week2 = time.strftime('%A')
        date2 = time.strftime('%d %b, %Y')
        if time2 != self.time1:
            self.time1 = time2
            self.timeLbl.config(text=time2)
        if day_of_week2 != self.day_of_week1:
            self.day_of_week1 = day_of_week2
            self.dayOWLbl.config(text=day_of_week2)
        if date2 != self.date1:
            self.date1 = date2
            self.dateLbl.config(text=date2)
        self.timeLbl.after(200, self.tick)
