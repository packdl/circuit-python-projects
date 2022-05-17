import board
import time
import keypad
import random
import terminalio
import displayio

from adafruit_display_text import label
import neopixel
from adafruit_itertools.adafruit_itertools import cycle

display = board.DISPLAY

main_group = displayio.Group()
display.show(main_group)

font = terminalio.FONT

reg_label = label.Label(font=font, text="Sight Words", scale=2)
reg_label.anchor_point = (0, 0)
reg_label.anchored_position = (20, 20)

main_group.append(reg_label)
time.sleep(1)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)

color_dict = {0:RED,1:GREEN,2:CYAN, 3:BLUE}

pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.01)
k = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    data=board.BUTTON_OUT,
    latch=board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
)

with open('words.txt', mode='rt') as f:
    data = f.readlines()
    words = tuple(d.strip() for d in data)
c = cycle(words)

while True:
    event = k.events.get()
    if not event:
        pixels.fill((0,0,0))
    elif event.pressed:
        if event.key_number == 3:
            color = (random.randint(0,255),random.randint(0,255), random.randint(0,255))
            #print(color)
            pixels.fill(color)
        elif event.key_number == 1:
            reg_label.text = next(c)
        else:
            color = color_dict[event.key_number]
            pixels.fill(color)

    time.sleep(1)
