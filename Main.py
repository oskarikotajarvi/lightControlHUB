import sys
from tkinter import *
from FullScreenWindow import FullScreenWindow

if __name__ == '__main__':
    try:
        w = FullScreenWindow()
        w.tk.mainloop()
    except KeyboardInterrupt:
        sys.exit()
