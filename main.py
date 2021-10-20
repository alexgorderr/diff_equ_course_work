import gui
from tkinter import Tk

if __name__ == '__main__':
    window = Tk()
    window.geometry("1000x500")
    app = gui.Application(window)
    window.mainloop()
