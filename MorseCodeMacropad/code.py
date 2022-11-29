# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
MacroPad tone demo. Plays a different tone for each key pressed and lights up each key a different
color while the key is pressed.
"""
import time
from rainbowio import colorwheel
from adafruit_macropad import MacroPad

from morse import morse

"""
0  -  DOT
1  -  DASH
2  -  Accept Morse letter
3  -  Delete Morse letter
5  -  Word space
9  -  Clear Display & stored letters
11 -  Play Morris code for message

"""


DOT = "."
DASH = "-"
DOT_TIME = .05



macropad = MacroPad()

text_lines = macropad.display_text(title="Morse code")

dot_tone = 300
key_colors = [(0,255,0), (0,255,0), (0,255,0),(255,0,0),(0,0,0),(0,255,0),(0,0,0),(0,0,0),(0,0,0),(255,0,0),(0,0,0),(0,0,255)]
current_morse_letter = ""
display_word = ""
morse_words = []

print('Press a key')

while True:
    try:
        key_event = macropad.keys.events.get()

        if key_event:
            if key_event.pressed:
                macropad.pixels[key_event.key_number] = key_colors[key_event.key_number]

            if key_event.released:
                number = key_event.key_number
                if number == 0:
                    current_morse_letter = current_morse_letter + DOT
                elif number == 1:
                    current_morse_letter = current_morse_letter + DASH
                elif number == 2:
                    display_word += morse[current_morse_letter]
                    morse_words.append(current_morse_letter)
                    current_morse_letter = ""
                elif number == 3:
                    current_morse_letter = ""
                elif number == 5:
                    if current_morse_letter and morse[current_morse_letter] != 'NA':
                        display_word += morse[current_morse_letter]
                        morse_words.append(current_morse_letter)
                        current_morse_letter = ""
                    morse_words.append(" ")
                    display_word+= " "
                elif number == 9:
                    display_word = ""
                    morse_words.clear()
                    current_morse_letter=""
                elif number == 11:
                    print(morse_words)
                    for character in morse_words:
                        for partial in character:
                            if partial == DOT:
                                macropad.play_tone(dot_tone, DOT_TIME)
                                time.sleep(DOT_TIME)
                            elif partial == DASH:
                                macropad.play_tone(dot_tone, DOT_TIME*3)
                                time.sleep(DOT_TIME)
                            else:
                                time.sleep(DOT_TIME * 7.0)
                        time.sleep(DOT_TIME*3)
                text_lines[0].text = "MC:'{}'".format(current_morse_letter)
                text_lines[1].text = "Char:{}".format(morse.get(current_morse_letter,'NA'))
                text_lines[2].text = "Word: {}".format(display_word)
                text_lines.show()
                # macropad.start_tone(dot_tone)
        else:
            macropad.pixels.fill((0, 0, 0))
            # macropad.stop_tone()
    except KeyError as excp:
        print(excp)
