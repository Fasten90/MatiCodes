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


def callback(event):
    event.widget.config(bg='blue')


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

        # code for creating table
        row_count = 12
        column_count = 12
        table_list = []
        for i in range(row_count):
            for j in range(column_count):
                #self.e = tk.Entry(root, width=20, fg='blue',
                self.e = tk.Entry(self, width=1, fg='blue',
                            font=('Arial',16,'bold'))
                # https://stackoverflow.com/questions/61225793/tkinter-click-event-highlights-the-label-clicked
                #self.label = tk.Label(self, text=table_values[i][0], width=10, justify='left', bg='white')
                #self.label.bind("<Button-1>", callback)
                #self.label.grid(row=i+1, column=0)
                self.e.grid(row=i, column=j)
                self.e.columnconfigure(0, weight=1)
                #w.columnconfigure(1, weight=1)
                #self.e.insert(tk.END, lst[i][j])

        exit_colum = math.floor(column_count /2 )
        exit_row = row_count + 1
        self.button_3 = tk.Button(self, width=1, height=1)
        self.button_3["text"] = "X"
        self.button_3["command"] = self.button_exit_event
        self.button_3.grid(row=exit_row, column=exit_colum)  # View


    def button_add_event(self):
        print('Add button')
        lines = self.entry_qr.get("0.0", tk.END)  # TODO: Check which line needed... or clear needed
        print(f'Lines: "{lines}"')
        self.add_item(lines)


    def button_exit_event(self):
        print('Exit button')
        self.quit()


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

