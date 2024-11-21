#!/usr/bin/python3

import tkinter as tk
from tkinter import Tk, Label, Button, Entry, X
from tkinter.font import *
from tkinter import ttk


root = Tk()


button_exit = tk.Button(root, width=1, height=1)
button_exit["text"] = "X"
button_exit.grid(row=1, column=0, columnspan=2)

bomb_count_field = tk.Label(root, height=1)
bomb_count_field["text"] = "00"
bomb_count_field.grid(row=1, column=1, columnspan=1)

message_field = tk.Label(root, height=1)
message_field["text"] = ""
message_field.grid(row=1, column=2, columnspan=1)

root.grid_columnconfigure(1, weight=1)# add this line

root.mainloop()


