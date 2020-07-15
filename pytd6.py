import keyboard, mouse, json, pygetwindow, time, ctypes
from typing import Tuple
from exceptions import *

# required for the mouse.move to not be offset when display scaling is enabled.
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# load json file with monkey information in it.
with open("monkeys.json") as monkeys_json:
    monkeys = json.load(monkeys_json)


def price_round(x, base=5):
    return base * round(x / base)


class monkey:
    def __init__(self, monkey: str):

        # initialize monkey's attributes.
        self.sold = False
        self.placed = False
        self.upgrades = [0, 0, 0]
        self.monkey_name = monkey
        self.info(self.monkey_name)

    def place(self, coordinates: Tuple[int, int]):

        # raise CoordinateError if invalid type or tuple length.
        if (type(coordinates) is not list) and (type(coordinates) is not tuple):
            raise CoordinateError
        if len(coordinates) != 2:
            raise CoordinateError
        # raise MonkeyPlaced if the monkey has already been placed.
        if self.placed:
            raise MonkeyPlaced

        self.hotkeys = {
            "monkeys": {"Dart Monkey": "q"},
            "upgrades": [",", ".", "?"],
        }

        # activate Bloons TD 6 window.
        btd6_window = pygetwindow.getWindowsWithTitle("BloonsTD6")[0]
        btd6_window.activate()

        # get current mouse position
        # move to the monkey's position
        # send the hotkey for the monkey
        # left click to place the monkey
        # move back to previous position.
        # time.sleep required for the monkey to be placed in time.
        previous_position = mouse.get_position()
        mouse.move(coordinates[0], coordinates[1])
        time.sleep(0.1)
        keyboard.send(self.hotkeys["monkeys"][self.monkey_name])
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.1)
        mouse.move(previous_position[0], previous_position[1])
        time.sleep(0.1)

        # record the coordinates of the monkey.
        self.coordinates = coordinates

        # record that the monkey has been placed.
        self.placed = True

    def upgrade(self, upgrades: Tuple[int, int, int] = None):

        # if no upgrade path is passed, use the one provided when the monkey was generated.
        if upgrades is None:
            upgrades = self.upgrades

        # raise UpgradeError if invalid type or tuple length.
        if (type(upgrades) is not list) and (type(upgrades) is not tuple):
            raise UpgradeError
        if len(upgrades) != 3:
            raise UpgradeError

        # raise UpgradeError if all paths have tiers active.
        if upgrades.count(0) == 0:
            raise UpgradeError

        # raise UpgradeError there is a path above the 5th tier.
        if max(upgrades) > 5:
            raise UpgradeError

        # raise UpgradeError if there is more than one path at tier 3 or higher
        third_tier_upgrade_count = len([i for i in upgrades if i >= 3])
        if third_tier_upgrade_count > 1:
            raise UpgradeError

        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # get current mouse position
        # move to the monkey's position
        # send the hotkey for (current upgrade - previous upgrade)
        # send escape to get out of upgrade menu
        # move back to previous position
        previous_position = mouse.get_position()
        mouse.move(self.coordinates[0], self.coordinates[1])
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.1)
        for path in range(len(upgrades)):
            for tier in range(upgrades[path] - self.upgrades[path]):
                keyboard.send(self.hotkeys["upgrades"][path])
                time.sleep(0.1)
        keyboard.send("esc")
        time.sleep(0.1)
        mouse.move(previous_position[0], previous_position[1])
        time.sleep(0.1)

        # record the upgrades of the monkey.
        self.upgrades = upgrades

        # update information about tower
        self.info(self.monkey_name)

    def sell(self):

        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # get current mouse position
        # move to the monkey's position
        # sell monkey
        # move back to previous position.
        previous_position = mouse.get_position()
        mouse.move(self.coordinates[0], self.coordinates[1])
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.1)
        keyboard.send("backspace")
        time.sleep(0.1)
        mouse.move(previous_position[0], previous_position[1])
        time.sleep(0.1)

        # record that the monkey has been sold.
        self.sold = True

    def info(self, monkey_name: str = None, upgrades: Tuple[int, int, int] = None):

        # if no upgrade path is passed, use the one provided when the monkey was generated.
        if upgrades == None:
            upgrades = self.upgrades

        # if no monkey name is passed, use the one provided when the monkey was generated.
        if monkey_name == None:
            monkey_name = self.monkey_name

        main_tier = max(upgrades)
        main_path = upgrades.index(main_tier)

        self.monkey_name = monkey_name
        self.monkey_description = monkeys[monkey_name]["description"]

        self.monkey_price_medium = monkeys[monkey_name]["price"]
        self.monkey_price_easy = price_round(0.85 * self.monkey_price_medium)
        self.monkey_price_hard = price_round(1.08 * self.monkey_price_medium)
        self.monkey_price_impoppable = price_round(1.2 * self.monkey_price_medium)

        self.upgrade_name = None
        self.upgrade_description = None

        self.upgrade_price_medium = 0
        self.upgrade_price_easy = 0
        self.upgrade_price_hard = 0
        self.upgrade_price_impoppable = 0

        if upgrades != [0, 0, 0]:
            self.upgrade_name = monkeys[monkey_name]["upgrades"][main_path][
                main_tier - 1
            ]["name"]
            self.upgrade_description = monkeys[monkey_name]["upgrades"][main_path][
                main_tier - 1
            ]["description"]
            self.upgrade_price_medium = monkeys[monkey_name]["upgrades"][main_path][
                main_tier - 1
            ]["price"]
            self.upgrade_price_easy = price_round(0.85 * self.upgrade_price_medium)
            self.upgrade_price_hard = price_round(1.08 * self.upgrade_price_medium)
            self.upgrade_price_impoppable = price_round(1.2 * self.upgrade_price_medium)

        self.total_price_medium = self.monkey_price_medium
        for path in range(len(upgrades)):
            for tier in range(upgrades[path]):
                self.total_price_medium += monkeys[monkey_name]["upgrades"][path][tier][
                    "price"
                ]
        self.total_price_easy = price_round(0.85 * self.total_price_medium)
        self.total_price_hard = price_round(1.08 * self.total_price_medium)
        self.total_price_impoppable = price_round(1.2 * self.total_price_medium)

