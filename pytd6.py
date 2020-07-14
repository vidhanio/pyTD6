import keyboard, mouse, json, pygetwindow, time, ctypes
from typing import Tuple
from exceptions import *

# required for the mouse.move to not be offset when display scaling is enabled.
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

with open("monkeys.json") as monkeys_json:
    monkeys = json.load(monkeys_json)

initiated = False


class init:
    def __init__(self, resolution: Tuple[int, int] = [1920, 1080]):

        if resolution[0] / resolution[1] >= 16 / 9:
            placeable_width = (41 / 48) * resolution[0]
            self.placeable_area = (round(placeable_width), resolution[1])
        else:
            placeable_height = (8 / 9) * resolution[1]
            self.placeable_area = (resolution[0], round(placeable_height))

        self.check_if_btd6_running()

    def check_if_btd6_running(self):
        btd6_window = pygetwindow.getWindowsWithTitle("BloonsTD6")
        if not btd6_window:
            raise BloonsTD6NotOpen


class monkey(init):
    def __init__(self, monkey: str, upgrades: Tuple[int, int, int] = [0, 0, 0]):
        if (type(upgrades) is not list) and (type(upgrades) is not tuple):
            raise UpgradeError
        if len(upgrades) != 3:
            raise UpgradeError
        upgrades = [int(upgrade) for upgrade in upgrades]
        self.name = monkeys[monkey]["name"]
        self.description = monkeys[monkey]["description"]
        self.category = monkeys[monkey]["category"]
        self.upgrades = upgrades

    def place(self, coordinates: Tuple[int, int]):

        # raise CoordinateError if invalid type or tuple length.
        if (type(coordinates) is not list) and (type(coordinates) is not tuple):
            raise CoordinateError
        if len(coordinates) != 2:
            raise CoordinateError

        self.hotkeys = {"monkeys": {"Dart Monkey": "q"}, "upgrades": [",", ".", "/"]}

        # activate Bloons TD 6 window.
        btd6_window = pygetwindow.getWindowsWithTitle("BloonsTD6")[0]
        btd6_window.activate()

        # get previous mouse pos, move to new pos, enter monkey hotkey, place, move back to previous pos.
        # time.sleep required for the monkey to be placed in time.
        previous_position = mouse.get_position()
        mouse.move(coordinates[0], coordinates[1])
        keyboard.send(self.hotkeys["monkeys"][self.name])
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.1)
        mouse.move(previous_position[0], previous_position[1])
        time.sleep(0.1)

        # remember the coordinates of the monkey.
        self.coordinates = coordinates

    def upgrade(self, upgrades: Tuple[int, int, int] = None):

        # if no upgrade path is passed, use the one provided when the monkey was generated.
        if upgrades is None:
            upgrades = self.upgrades

        # raise UpgradeError if invalid type or tuple length.
        if (type(upgrades) is not list) and (type(upgrades) is not tuple):
            raise UpgradeError
        if len(upgrades) != 3:
            raise UpgradeError

        # get previous mouse pos, move to new pos, enter upgrade hotkey, place, move back to previous pos.
        previous_position = mouse.get_position()
        mouse.move(self.coordinates[0], self.coordinates[1])
        mouse.click()
        time.sleep(0.1)
        for path in range(len(upgrades)):
            for tier in range(upgrades[path]):
                keyboard.send(self.hotkeys["upgrades"][path])
                time.sleep(0.1)
        keyboard.send("esc")

