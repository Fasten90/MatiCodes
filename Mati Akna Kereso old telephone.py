#!/usr/bin/python3

import tkinter as tk
from tkinter.font import *
import math


# Extreme static variables
#FLAG_CHARACTER = "🚩"  # Unicode character. PANIC STARTED
FLAG_CHARACTER = "|>"  # for mobile
BOMB_IN_EDITOR_MODE = 'X'

BACKGROUND_COLOR = 'black'

# Settings (static) variables
row_count = 9
column_count = 12

# Dynamic variables
root = None

table_list = []
table_list_displaying = []
table_objects = None

is_play_mode = False
bomb_count = 0


root = tk.Tk()


def callback(event):
    global bomb_count
    name = event.widget._name
    if name == '!entry':
        name = '!entry1'
    index = name.split('!entry')[1]
    index = int(index) - 1
    row = math.floor(index / column_count)
    column = index % column_count
    print(f'It is row {row} column {column}')
    if not is_play_mode:
        # Editor mode
        if table_list[row][column] != BOMB_IN_EDITOR_MODE:
            # Clicking firstly / mark as bomb
            table_list[row][column] = BOMB_IN_EDITOR_MODE
            table_list_displaying[row][column].set(BOMB_IN_EDITOR_MODE)
            event.widget.config(bg='blue')
            bomb_count += 1
        else:
            # Click again? Remove the bomb
            table_list[row][column] = 0
            table_list_displaying[row][column].set('')
            event.widget.config(bg='white')
            bomb_count -= 1
        #event.widget.config(text='x')  # Does not work
    else:
        # Play mode
        value = table_list[row][column]
        # Check what is in the display:
        if table_list_displaying[row][column].get() != FLAG_CHARACTER:
            # First situation: FLAG
            table_list_displaying[row][column].set(FLAG_CHARACTER)
            bomb_count -= 1
        else:
            # Second situation: What is under on the flag :) BUMMMMMMM
            table_list_displaying[row][column].set(value)
            bomb_count += 1
        check_if_finish()
    bomb_count_field["text"] = '{:02}'.format(bomb_count)


def check_if_finish():
    # Check if all field contains clicked value:
    for i in range(row_count):
        for j in range(column_count):
            value_of_display_field = table_list_displaying[i][j].get()
            expected_value = str(table_list[i][j])  # Convert the 1 to '1'
            if value_of_display_field == '':
                # Contains empty - not clicked field. The game has not finished yet
                return False
            elif value_of_display_field == expected_value:
                # Value
                continue
            elif value_of_display_field == FLAG_CHARACTER and expected_value == BOMB_IN_EDITOR_MODE:
                # Bomb field
                continue
            else:
                return False
    message_field["text"] = 'Win!'
    return True


def button_exit_event():
    print('Exit button')
    quit()


def button_calculate_event():
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


def display_aknas():
    # code for creating table
    global table_list_displaying
    for i in range(row_count):
        for j in range(column_count):
            value = table_list[i][j]
            table_list_displaying[i][j].set(value)


def clear_table(remove=False):
    # code for creating table
    global  table_list
    for i in range(row_count):
        for j in range(column_count):
            if remove:
                table_list[i][j] = 0
            # Clear displayed text + background
            table_list_displaying[i][j].set('')
            table_objects[i][j].config(bg='white')


def button_play_event():
    print('Play button')
    clear_table(remove=False)
    global is_play_mode
    is_play_mode = True


def button_new_event():
    print('New button')
    clear_table(remove=True)
    global is_play_mode
    is_play_mode = False
    global bomb_count
    bomb_count = 0


def quit():
    root.destroy()
    exit(0)

#table_objects = [['0'] * column_count].copy() * row_count  # TRAP
table_objects = [ [0]*column_count for i in range(row_count)]


#table_list = [['0'] * column_count].copy() * row_count # TRAP
table_list =[ [0]*column_count for i in range(row_count)]
table_list_displaying = [ [0]*column_count for i in range(row_count)]

# code for creating table
for i in range(row_count):
    for j in range(column_count):
        table_list_displaying[i][j] = tk.StringVar()
        table_objects[i][j] = tk.Entry(root, width=1, fg='blue',
                    font=('Arial',16,'bold'), textvariable=table_list_displaying[i][j])
        table_objects[i][j].bind("<Button-1>", callback)
        table_objects[i][j].grid(row=i, column=j)

#button_colum = math.floor(column_count /2 )
button_row = row_count + 2

button_new = tk.Button(root, width=1, height=1)
button_new["text"] = "N"
button_new["command"] = button_new_event
button_new.grid(row=button_row, column=0, columnspan=3)

button_calculate = tk.Button(root, width=1, height=1)
button_calculate["text"] = "C"
button_calculate["command"] = button_calculate_event
button_calculate.grid(row=button_row, column=3, columnspan=2)

button_display_aknas = tk.Button(root, width=1, height=1)
button_display_aknas["text"] = "D"
button_display_aknas["command"] = display_aknas
button_display_aknas.grid(row=button_row, column=5, columnspan=2)

button_play = tk.Button(root, width=1, height=1)
button_play["text"] = "P"
button_play["command"] = button_play_event
button_play.grid(row=button_row, column=7, columnspan=2)

button_exit = tk.Button(root, width=1, height=1)
button_exit["text"] = "X"
button_exit["command"] = button_exit_event
button_exit.grid(row=button_row, column=10, columnspan=2)

bomb_count_field = tk.Label(root, height=1)
bomb_count_field["text"] = "00"
bomb_count_field.grid(row=button_row+1, column=0, columnspan=column_count)

message_field = tk.Label(root, height=1)
message_field["text"] = ""
message_field.grid(row=button_row+2, column=0, columnspan=column_count)



root.mainloop()

