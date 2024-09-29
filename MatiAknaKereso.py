#!/usr/bin/python3

#https://docs.python.org/3.7/library/tkinter.html
import tkinter as tk
# For Font
from tkinter.font import *
from PIL import Image
from enum import Enum
import math


FLAG_CHARACTER = "🚩"  # Unicode character. PANIC STARTED
BACKGROUND_COLOR = 'black'

root = None
app = None

table_list = []
table_list_displaying = []
table_objects = None

row_count = None
column_count = None

is_play_mode = False


# https://blog.furas.pl/python-tkinter-how-to-set-size-for-empty-row-or-column-in-grid-gb.html

def callback(event):
    name = event.widget._name
    if name == '!entry':
        name = '!entry1'
    index = name.split('!entry')[1]
    index = int(index) - 1
    row = math.floor(index / column_count)
    column = index % row_count 
    print(f'It is row {row} column {column}')
    if not is_play_mode:
        # Editor mode
        if table_list[row][column] != 'X':
            # Clicking firstly / mark as bomb
            table_list[row][column] = 'X'
            table_list_displaying[row][column].set('X')
            event.widget.config(bg='blue')
        else:
            # Click again? Remove the bomb
            table_list[row][column] = 0
            table_list_displaying[row][column].set('')
            event.widget.config(bg='white')
        #event.widget.config(text='x')  # Does not work
    else:
        # Play mode
        value = table_list[row][column]
        # Check what is in the display:
        if table_list_displaying[row][column].get() != FLAG_CHARACTER:
            # First situation: FLAG
            table_list_displaying[row][column].set(FLAG_CHARACTER)
        else:
            # Second situation: What is under on the flag :) BUMMMMMMM
            table_list_displaying[row][column].set(value)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()


    def create_widgets(self):

        # Title
        title_font = ('Arial', 20, 'bold')
        self.title_label = tk.Label(self, text="Mati AknaKereso", font=title_font)
        #self.title_label.grid(row=0, column=0)  # View

        global row_count
        global column_count

        row_count = 12
        column_count = 12

        global table_objects
        #table_objects = [['0'] * column_count].copy() * row_count  # TRAP
        table_objects = [ [0]*column_count for i in range(row_count)]

        global table_list
        #table_list = [['0'] * column_count].copy() * row_count # TRAP
        table_list =[ [0]*column_count for i in range(row_count)]
        global table_list_displaying
        table_list_displaying = [ [0]*column_count for i in range(row_count)]

        # code for creating table
        for i in range(row_count):
            for j in range(column_count):
                table_list_displaying[i][j] = tk.StringVar()
                table_objects[i][j] = tk.Entry(self, width=1, fg='blue',
                            font=('Arial',16,'bold'), textvariable=table_list_displaying[i][j])
                # https://stackoverflow.com/questions/61225793/tkinter-click-event-highlights-the-label-clicked
                table_objects[i][j].bind("<Button-1>", callback)
                table_objects[i][j].grid(row=i, column=j)

        button_colum = math.floor(column_count /2 )
        button_row = row_count + 2

        self.button_new = tk.Button(self, width=1, height=1)
        self.button_new["text"] = "N"
        self.button_new["command"] = self.button_new_event
        self.button_new.grid(row=button_row, column=button_colum-2)

        self.button_calculate = tk.Button(self, width=1, height=1)
        self.button_calculate["text"] = "C"
        self.button_calculate["command"] = self.button_calculate_event
        self.button_calculate.grid(row=button_row, column=button_colum)

        self.button_display_aknas = tk.Button(self, width=1, height=1)
        self.button_display_aknas["text"] = "D"
        self.button_display_aknas["command"] = self.display_aknas
        self.button_display_aknas.grid(row=button_row, column=button_colum+1)

        self.button_play = tk.Button(self, width=1, height=1)
        self.button_play["text"] = "P"
        self.button_play["command"] = self.button_play_event
        self.button_play.grid(row=button_row, column=button_colum+2)

        self.button_exit = tk.Button(self, width=1, height=1)
        self.button_exit["text"] = "X"
        self.button_exit["command"] = self.button_exit_event
        self.button_exit.grid(row=button_row, column=button_colum+4)


    def button_exit_event(self):
        print('Exit button')
        self.quit()


    def button_calculate_event(self):
        print('Calculate button')
        global table_list
        for row_i, row in enumerate(table_list):
            for column_i, cell in enumerate(row):
                if cell == 'X':
                    continue
                elif cell != 'X':
                    # Check neightboor X-s
                    akna = 0
                    for row_calc in range(max(row_i-1, 0), min(row_i+1, row_count-1) + 1):
                        for column_calc in range(max(column_i-1, 0), min(column_i+1, column_count-1) + 1):
                            if table_list[row_calc][column_calc] == 'X':
                                akna +=1
                    table_list[row_i][column_i] = akna


    def display_aknas(self):
        # code for creating table
        global table_list_displaying
        for i in range(row_count):
            for j in range(column_count):
                value = table_list[i][j]
                table_list_displaying[i][j].set(value)


    def clear_table(self, remove=False):
        # code for creating table
        global  table_list
        for i in range(row_count):
            for j in range(column_count):
                if remove:
                    table_list[i][j] = 0
                # Clear displayed text + background
                table_list_displaying[i][j].set('')
                table_objects[i][j].config(bg='white')


    def button_play_event(self):
        print('Play button')
        self.clear_table(remove=False)
        global is_play_mode
        is_play_mode = True


    def button_new_event(self):
        print('New button')
        self.clear_table(remove=True)
        global is_play_mode
        is_play_mode = False


    def quit(self):
        self.master.destroy()
        exit(0)


def start_gui(config=None):
    global root

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = Application(master=root)
    root.configure(bg=BACKGROUND_COLOR)
    app.mainloop()


if __name__ == "__main__":
    start_gui()

