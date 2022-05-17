import board
import time
import random
import terminalio
import json
import alarm

from adafruit_magtag.magtag import MagTag

PLAINFONT = False  # Use built in font if True
DATA_SOURCE = (
    "https://packdl.github.io/bcsd-covid-dashboard/output/dailydifference.json"
)
magtag = MagTag()

# Disable lights
magtag.peripherals.neopixel_disable = True  # turn off lights
magtag.peripherals.speaker_disable = True


# main text, index 0
magtag.add_text(
    text_font=terminalio.FONT if PLAINFONT else "Arial-Bold-24.bdf",
    text_position=(
        magtag.graphics.display.width // 2,
        10,
    ),
    text_scale=3 if PLAINFONT else 1,
    line_spacing=1,
    text_anchor_point=(0.5, 0),
)

# button labels, add all 4 in one loop
for x_coord in (10, 75, 150, 220):
    magtag.add_text(
        text_font=terminalio.FONT if PLAINFONT else "Arial-12.bdf",
        text_position=(x_coord, magtag.graphics.display.height - 10),
        line_spacing=1.0,
        text_anchor_point=(0, 1),
    )

# large horoscope text, index 5
magtag.add_text(
    text_font=terminalio.FONT if PLAINFONT else "Arial-12.bdf",
    text_position=(10, magtag.graphics.display.height // 2 - 5),
    line_spacing=1.0,
    text_wrap=35,
    text_maxlen=130,
    text_anchor_point=(0, 0),
)
# small horoscope text, index 6
magtag.add_text(
    text_font=terminalio.FONT if PLAINFONT else "Arial-12.bdf",
    text_position=(10, 10),
    line_spacing=1.0,
    text_wrap=35,
    text_maxlen=130,
    text_anchor_point=(0, 0),
)

try:
    magtag.network.connect()
except (ConnectionError) as e:
    print(e)
    print("Continuing without WiFi")

# clear selections
for i in range(1, 5):
    magtag.set_text("", i, False)


def gen_school_text(name, school):
    school_student = school["current"]["student_cnt"]
    school_staff = school["current"]["staff_cnt"]
    student_delta = school_student - school["previous"]["student_cnt"]
    staff_delta = school_staff - school["previous"]["staff_cnt"]
    return f"{name} ({school['current']['day']})-Kids #:{school_student} ({'+' if student_delta >=0 else ''}{student_delta}). Staff #: {school_staff} ({'+' if staff_delta>=0 else ''}{staff_delta})"


def display_daily_data():
    try:
        print(DATA_SOURCE)
        response = magtag.network.requests.get(DATA_SOURCE)
        schools_delta = response.json()
        magtag.network.enabled = False
        bcsd = schools_delta[0]["Berkeley County School District"]
        mhe = schools_delta[0]["Mount Holly Elementary"]
        print(bcsd)
        magtag.set_text("Refreshes daily", 1, False)
        magtag.set_text("", 5, False)

        bcsd_text = gen_school_text("BCSD", bcsd)
        mhe_text = gen_school_text("MHE", mhe)

        magtag.set_text(bcsd_text, 6, False)
        magtag.set_text(mhe_text, 5)
    except Exception as e:
        print(e)
        magtag.set_text("Refreshes daily", 1, False)
        magtag.set_text("", 6, False)
        magtag.set_text("Wifi not connected", 5)


# Show new Covid data on display
magtag.set_background(0xFFFFFF)  # back to white background
display_daily_data()

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 86400)

# for b in magtag.peripherals.buttons:
#    b.deinit()
# my_alarms = [alarm.pin.PinAlarm(pin=x, value=False, pull=True) for x in [board.BUTTON_A, board.BUTTON_B, board.BUTTON_C, board.BUTTON_D]]
# my_alarms = [alarm.pin.PinAlarm(pin=x, value=False, pull=True) for x in [board.BUTTON_C, board.BUTTON_D]]
# my_alarms.append(time_alarm)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
