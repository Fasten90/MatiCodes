import time
import random
import os

DEBUG = False


def generate_hiba():
    # Clearing the Screen
    os.system('cls')
    random_sec = random.randint(20,120)  # 20 másodperc és 2 perc között
    if DEBUG:
        print(f'Ennyit másodperc múlva lesz hiba: {random_sec}')
    time.sleep(random_sec)
    print('hiba')
    input('')  # Entert várunk


while True:
    generate_hiba()

