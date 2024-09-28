#!/usr/bin/python3

#https://docs.python.org/3.7/library/tkinter.html
import tkinter as tk
# For Font
from tkinter.font import *
from PIL import Image
from enum import Enum
import math


root = None
app = None

table_list = []
table_list_displaying = []
table_objects = None

row_count = None
column_count = None


# https://blog.furas.pl/python-tkinter-how-to-set-size-for-empty-row-or-column-in-grid-gb.html

def callback(event):
    event.widget.config(bg='blue')
    name = event.widget._name
    if name == '!entry':
        name = '!entry1'
    index = name.split('!entry')[1]
    index = int(index) - 1
    row = math.floor(index / column_count)
    column = index % row_count 
    print(f'It is row {row} column {column}')
    table_list[row][column] = 'X'
    #event.widget.config(text='x')


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()


    def create_widgets(self):

        # Specials
        #global gui_variable_status
        #gui_variable_status = tk.StringVar(value='Status')

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
                #self.e = tk.Entry(root, width=20, fg='blue',
                #self.e =
                table_list_displaying[i][j] = tk.StringVar()
                table_objects[i][j] = tk.Entry(self, width=1, fg='blue',
                            font=('Arial',16,'bold'), textvariable=table_list_displaying[i][j])
                # https://stackoverflow.com/questions/61225793/tkinter-click-event-highlights-the-label-clicked
                #self.label = tk.Label(self, text=table_values[i][0], width=10, justify='left', bg='white')
                #self.e =
                table_objects[i][j].bind("<Button-1>", callback)
                #self.label.grid(row=i+1, column=0)
                #self.e =
                table_objects[i][j].grid(row=i, column=j)
                #self.e.columnconfigure(0, weight=1)
                #w.columnconfigure(1, weight=1)
                #self.e.insert(tk.END, lst[i][j])

        exit_colum = math.floor(column_count /2 )
        exit_row = row_count + 1
        self.button_3 = tk.Button(self, width=1, height=1)
        self.button_3["text"] = "X"
        self.button_3["command"] = self.button_exit_event
        self.button_3.grid(row=exit_row, column=exit_colum-1)  # View

        self.button_new = tk.Button(self, width=1, height=1)
        self.button_new["text"] = "N"
        self.button_new["command"] = self.button_new
        self.button_new.grid(row=exit_row, column=exit_colum)  # View

        self.button_4 = tk.Button(self, width=1, height=1)
        self.button_4["text"] = "C"
        self.button_4["command"] = self.button_calculate_event
        self.button_4.grid(row=exit_row, column=exit_colum+1)  # View

        self.button_5 = tk.Button(self, width=1, height=1)
        self.button_5["text"] = "P"
        self.button_5["command"] = self.button_play_event
        self.button_5.grid(row=exit_row, column=exit_colum+2)  # View

        self.button_6 = tk.Button(self, width=1, height=1)
        self.button_6["text"] = "D"
        self.button_6["command"] = self.display_aknas
        self.button_6.grid(row=exit_row, column=exit_colum+3)  # View


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
        for i in range(row_count):
            for j in range(column_count):
                value = table_list[i][j]
                table_list_displaying[i][j].set(value)


    def button_play_event(self):
        print('Play button')

    def button_new(self):
        print('New button')


    def quit(self):
        self.master.destroy()
        exit(0)


    def entry_changed_input(self, event):
        """ Called at newlines"""
        print(f'entry_changed_input: {event}')

        #content = self.entry_qr.get()  # entry
        content = self.entry_qr.get("0.0", tk.END)
        print(f'Content: {content}')
        if '\n' not in content:
            return
        lines = content.split('\n')
        lines = [item.strip() for item in lines]
        for new_line in lines:
            if len(new_line) == 0:
                continue
            # Item LETS GO
            print(f'Find new line: {new_line}')
            # TODO
        self.entry_qr.delete("0.0", tk.END)


def start_gui(config=None):
    global root

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    start_gui()

