from tkinter import Tk, Label
import datetime

root = Tk()
clock = datetime.datetime.now()
Label(root, text=str(clock)).pack()
root.mainloop

