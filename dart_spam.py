from pytd6 import Monkey
import keyboard, mouse, time

keyboard.add_hotkey("delete", exit)
for x in range(50, 1500, 10):
    for y in range(0, 1080, 10):
        Monkey("Dart Monkey").place([x, y])
        mouse.move(1601, 121)
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.1)

