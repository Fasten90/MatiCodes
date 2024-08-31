import time
import random
import os
from enum import Enum
import math

DEBUG = False


BOTTOM_LINE_INDEX = 60
LINE_LENGTH = 220

uzenet = \
""" A vonat indulási pontossága megkérdőjelezhető
Számolás...
a hiba jelenethez érkező tehervonat:9:55,21:50
telefon alatt hiba!
telefon
MÁV Zrt. 2024.1
"""

hiba_uzenetek = [
    """HIBA! Exception! Lekezeletlen hiba
""",

    """STACK ERROR! KRITIKUS HIBA!
""",

    """FATAL ERROR! HARD FAULT! SEGMENTATION ERROR
PC# 0x12345678
SP# 0x76543210
""",  # Eddig tart

]


class Position(Enum):
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMLEFT = 3
    BOTTOMRIGHT = 4
    MID = 5


def print_hiba(position, uzenet):
    #match position:
    if position == Position.TOPLEFT.value:
        print(uzenet)
    elif position == Position.TOPRIGHT.value:
        print(' ' * LINE_LENGTH + uzenet)
    elif position == Position.BOTTOMLEFT.value:
        print('\r\n' * BOTTOM_LINE_INDEX)
        print(uzenet)
    elif position == Position.BOTTOMRIGHT.value:
        print('\r\n' * BOTTOM_LINE_INDEX)
        print(' ' * LINE_LENGTH + uzenet)
    elif position == Position.MID.value:
        print('\r\n' * math.floor(BOTTOM_LINE_INDEX/2))
        print(' ' * math.floor(LINE_LENGTH/2) + uzenet)
    else:
        print(uzenet)

def hiba_generalas():
    # Képernyő törlése / Terminál+karakterek törlése
    os.system('cls')
    if DEBUG:
        random_sec = random.randint(1,2)  # Ennyi idő múlva lesz hiba
    else:
        random_sec = random.randint(20,80)  # Ennyi idő múlva lesz hiba
    if DEBUG:
        print(f'Ennyit másodperc múlva lesz hiba: {random_sec}')

    print_hiba(position=Position.BOTTOMLEFT.value, uzenet=uzenet)
    time.sleep(random_sec)  # Várakozás
    #random_pos = random.randint(1,5)
    os.system('cls')
    random_pos = Position.BOTTOMLEFT.value
    hiba_index = random.randint(0, len(hiba_uzenetek))
    if DEBUG:
        print(f'random pos: {random_pos}, hiba index: {hiba_index}')
        input()
    hiba_uzenet = uzenet + hiba_uzenetek[hiba_index]
    print_hiba(random_pos, hiba_uzenet)
    input('')  # Entert várunk


while True:
    hiba_generalas()

