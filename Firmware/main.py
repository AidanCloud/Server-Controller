import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Macros

import busio
import adafruit_ssd1306
import time

i2c = busio.I2C(board.SCL, board.SDA)

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.show()

keyboard = KMKKeyboard()

macros = Macros()
keyboard.modules.append(macros)

PINS = [board.GPIO2, board.GPIO4, board.GPIO3]

Change_Internet = KC.USER0
Git_Pull = KC.USER1
Start_and_Stop_Server = KC.USER2

connection = "server"
server_status = "online"

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

keyboard.keymap = [
    [Change_Internet, Git_Pull, Start_and_Stop_Server]
]

def process_keys(key, is_pressed):
    global connection, server_status
    if key == Change_Internet and is_pressed:
        if connection == "server":
            connection = "Home"
        elif connection == "Home":
            connection = "School"
        elif connection == "School":
            connection = "Phone"
        elif connection == "Phone":
            connection = "server"
        
        oled.fill(0)
        oled.text("Mode:" + connection, 0, 0, 1)
        oled.show()
        return False
    elif key == Git_Pull and is_pressed:
        if connection != "server":
            oled.fill(0)
            oled.text("Attempting Git Pull", 0, 16, 1)
            oled.show()
            time.sleep(3)
            oled.fill(0)
            oled.text("Pull Complete", 0, 16, 1)
            oled.show()
            time.sleep(1)

        oled.fill(0)
        oled.text("Mode:" + connection, 0, 0, 1)
        oled.show()
        return False
    elif key == Start_and_Stop_Server and is_pressed:
        if server_status == "online":
            server_status = "offline"
        elif server_status == "offline":
            server_status = "online"

        oled.fill(0)
        oled.text("Mode:" + connection, 0, 0, 1)
        oled.show()
        return False

    return True

if __name__ == '__main__':
    keyboard.process_key = process_keys
    keyboard.go()
