import time
import random
import os
from enum import Enum
import math

DEBUG = False


BOTTOM_LINE_INDEX = 60
LINE_LENGTH = 220


class Position(Enum):
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4
    MID = 5


def print_hiba(position):
    #match position:
    if position == Position.TOPLEFT.value:
        print('hiba')
    elif position == Position.TOPRIGHT.value:
        print(' ' * LINE_LENGTH + 'hiba')
    elif position == Position.BOTTOMLEFT.value:
        print('\r\n' * BOTTOM_LINE_INDEX)
        print('hiba')
    elif position == Position.BOTTOMRIGHT.value:
        print('\r\n' * BOTTOM_LINE_INDEX)
        print(' ' * LINE_LENGTH + 'hiba')
    elif position == Position.MID.value:
        print('\r\n' * math.floor(BOTTOM_LINE_INDEX/2))
        print(' ' * math.floor(LINE_LENGTH/2) + 'hiba')
    else:
        print('hiba')


def hiba_generalas():
    # Képernyő törlése / Terminál+karakterek törlése
    os.system('cls')
    if DEBUG:
        random_sec = random.randint(1,2)  # Ennyi idő múlva lesz hiba
    else:
        random_sec = random.randint(20,80)  # Ennyi idő múlva lesz hiba
    if DEBUG:
        print(f'Ennyit másodperc múlva lesz hiba: {random_sec}')
    time.sleep(random_sec)  # Várakozás
    random_pos = random.randint(1,5)
    if DEBUG:
        print(f'random pos: {random_pos}')
        input()
    print_hiba(random_pos)
    input('')  # Entert várunk


while True:
    hiba_generalas()

