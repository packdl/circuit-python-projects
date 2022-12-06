# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import busio
import time
import digitalio
import displayio

# from adafruit_circuitplayground import cp
from adafruit_gizmo import tft_gizmo
import adafruit_lis3dh
import alarm

BRIGHTNESS = 0.1
DELAY = 3

# Create the TFT Gizmo display
display = tft_gizmo.TFT_Gizmo()
display.auto_brightness = False
display.brightness = BRIGHTNESS

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFF0000  # Bright Red

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.OnDiskBitmap("/santareindeer2.bmp")
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_bitmap.pixel_shader, x=20, y=20
)
splash.append(inner_sprite)
display_on = True

# Disable speaker
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.switch_to_output(value=False)

# Setup button A and B
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

a_prev_state = button_a.value
b_prev_state = button_b.value

# Start accelerometer
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_8_G

while True:

    if display_on:
        display.brightness = BRIGHTNESS
    else:
        display.brightness = 0
        button_a.deinit()
        time.sleep(0.1)
        pin_alarm = alarm.pin.PinAlarm(board.BUTTON_A, value=True, pull=True)
        print("I'm asleep")
        alarm.light_sleep_until_alarms(pin_alarm)
        print("This happened")
        button_a = digitalio.DigitalInOut(board.BUTTON_A)
        button_a.switch_to_input(pull=digitalio.Pull.DOWN)

    # Check A & B button state
    a_cur_state = button_a.value
    b_cur_state = button_b.value

    if a_cur_state != a_prev_state:
        if a_cur_state:
            display_on = True
            display_brightness = BRIGHTNESS
    a_prev_state = a_cur_state

    if b_cur_state != b_prev_state:
        if b_cur_state:
            display_on = False
            display.brightness = 0
    b_prev_state = b_cur_state

    # If device is upside down, turn off display after DELAY.
    if display_on:
        _, y, _ = lis3dh.acceleration
        previous_time = time.monotonic()

        while y < 0 and display_on:
            _, y, _ = lis3dh.acceleration
            if previous_time + DELAY < time.monotonic():
                display_on = False
                display_brightness = 0
                break
            else:
                continue

