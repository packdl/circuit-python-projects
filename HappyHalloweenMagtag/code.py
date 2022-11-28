# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

matrixportal = MatrixPortal(
    url=None,
    status_neopixel=board.NEOPIXEL,
)

# --- Display Setup --- #

# Delay for scrolling the text
SCROLL_DELAY = 0.06

text_colors=[0xFF5518,0x663399,0x663399]

# (ID = 0)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(
        (matrixportal.graphics.display.width // 3)-2,
        4,
    ),
    text_color=text_colors[0],
)

# (ID = 1)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(
        (matrixportal.graphics.display.width // 9) - 1,
        (matrixportal.graphics.display.height // 2) - 2,
    ),
    text_color=text_colors[0],
)
#matrixportal.preload_font("0123456789")

# Learn guide title (ID = 2)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, 25),
    text_color=text_colors[1],
    scrolling=True,
)

text_blue = True
while True:
    matrixportal.set_text('Happy', 0)
    matrixportal.set_text('Halloween', 1)
    matrixportal.set_text('Welcome',2)
    matrixportal.scroll_text(SCROLL_DELAY)
    time.sleep(2)
    text_blue = not text_blue
    if text_blue:
        matrixportal.set_text_color(text_colors[2],2)
    else:
        matrixportal.set_text_color(text_colors[1],2)
