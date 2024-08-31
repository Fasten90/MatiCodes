import time
import random
import os
from enum import Enum
import math

DEBUG = False


BOTTOM_LINE_INDEX = 60
LINE_LENGTH = 220


hiba_uzenetek = [
    """ A vonat indulási pontossága megkérdőjelezhető
    Számolás...
    ...
    MÁV Zrt. 2024.08.31
    HIBA! Exception! Lekezeletlen hiba
""",

    """Generálás közben log készült. A log helye: C:\\blabla\\tamtam\\log.txt
        Feldolgozás...
        STACK ERROR! KRITIKUS HIBA!
""",

    """Hátralevő idő: 12 másodperc...
11
10
9

FATAL ERROR! HARD FAULT! SEGMENTATION ERROR
PC# 0x12345678
SP# 0x76543210
""",
]


class Position(Enum):
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4
    MID = 5


def print_hiba(position, hiba_index):
    #match position:
    if position == Position.TOPLEFT.value:
        print(hiba_uzenetek[hiba_index])
    elif position == Position.TOPRIGHT.value:
        print(' ' * LINE_LENGTH + hiba_uzenetek[hiba_index])
    elif position == Position.BOTTOMLEFT.value:
        print('\r\n' * BOTTOM_LINE_INDEX)
        print(hiba_uzenetek[hiba_index])
    elif position == Position.BOTTOMRIGHT.value:
        print('\r\n' * BOTTOM_LINE_INDEX)
        print(' ' * LINE_LENGTH + hiba_uzenetek[hiba_index])
    elif position == Position.MID.value:
        print('\r\n' * math.floor(BOTTOM_LINE_INDEX/2))
        print(' ' * math.floor(LINE_LENGTH/2) + hiba_uzenetek[hiba_index])
    else:
        print(hiba_uzenetek[hiba_index])


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
    hiba_index = random.randint(0, len(hiba_uzenetek))
    if DEBUG:
        print(f'random pos: {random_pos}, hiba index: {hiba_index}')
        input()
    print_hiba(random_pos, hiba_index)
    input('')  # Entert várunk


while True:
    hiba_generalas()

