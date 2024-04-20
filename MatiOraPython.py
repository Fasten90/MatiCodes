# Mati python ora script
import time
import math

line = 0

print('Első szám')
result = input()

line = int(result)

def convert_line_to_clock(number):
    hour = math.floor(number / 1000)
    minute = math.floor(number / 10) % 100
    second = number % 10
    str = f'{hour}:{minute:02d}:{second:02d}'
    need_skip = True if minute >= 60 else False
    if hour >= 24:
        global line
        line = 0
        need_skip = True
    return str, need_skip

while True:
    clock, need_skip = convert_line_to_clock(line)
    print(f'{line}    {clock}')
    line += 1
    if not need_skip:
        time.sleep(1)
