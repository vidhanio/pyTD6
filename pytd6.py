import keyboard, mouse, json, pygetwindow, pywinauto, time, ctypes, pyautogui, PIL, pytesseract
from PIL import ImageFilter
from PIL import ImageChops
from typing import Tuple, Union
from exceptions import *

# required for the mouse.move() to not be offset when display scaling is enabled.
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

# load json file with monkey information in it.
with open("monkeys.json") as monkeys_json:
    monkeys = json.load(monkeys_json)

# load json file with hero information in it.
with open("heroes.json") as heroes_json:
    heroes = json.load(heroes_json)

# load json file with hotkey information in it.
with open("hotkeys.json") as hotkeys_json:
    hotkeys = json.load(hotkeys_json)

# used to focus btd6 window without IPython error (https://github.com/asweigart/PyGetWindow/issues/16s)
def focus_window(window_title=None):
    window = pygetwindow.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        pywinauto.application.Application().connect(
            handle=window._hWnd
        ).top_window().set_focus()


# used to round price to the nearest 5.
def price_round(x, base=5):
    return base * round(x / base)


# these 3 functions are used to get health, cash, and the round respectively.
def get_health():
    # focus BTD6.
    focus_window("BloonsTD6")
    # take a screenshot of the health.
    health_image = pyautogui.screenshot(region=[120, 20, 150, 40])
    # invert the image, as pytesseract does better with black text.
    health_image = ImageChops.invert(health_image)
    # convert it to a pure black and white binary image, to increase contrast and readability.
    fn = lambda x: 255 if x > 10 else 0
    health_image = health_image.convert("L").point(fn, mode="1")
    # save the image for debug purposes.
    health_image.save("health.png")
    # convert it to a string, with only specified characters allowed.
    health_text = pytesseract.image_to_string(
        health_image, config="-c tessedit_char_whitelist=0123456789 --psm 6",
    )

    # convert it into an integer if possible.
    try:
        health = int(health_text)
    except ValueError:
        health = 1
    return health


def get_cash():
    # focus BTD6.
    focus_window("BloonsTD6")
    # take a screenshot of the cash.
    cash_image = pyautogui.screenshot(region=[320, 20, 240, 40])
    # invert the image, as pytesseract does better with black text.
    cash_image = ImageChops.invert(cash_image)
    # convert it to a pure black and white binary image, to increase contrast and readability.
    fn = lambda x: 255 if x > 10 else 0
    cash_image = cash_image.convert("L").point(fn, mode="1")
    # save the image for debug purposes.
    cash_image.save("cash.png")
    # convert it to a string, with only specified characters allowed.
    cash_text = pytesseract.image_to_string(
        cash_image, config="-c tessedit_char_whitelist=$0123456789 --psm 6",
    )

    # convert it into an integer if possible.
    try:
        cash = int(cash_text[1:])
    except ValueError:
        cash = 0
    return cash


def get_round():
    # focus BTD6.
    focus_window("BloonsTD6")
    # take a screenshot of the round.
    round_image = pyautogui.screenshot(region=[1360, 30, 200, 40])
    # invert the image, as pytesseract does better with black text.
    round_image = ImageChops.invert(round_image)
    # convert it to a pure black and white binary image, to increase contrast and readability.
    fn = lambda x: 255 if x > 10 else 0
    round_image = round_image.convert("L").point(fn, mode="1")
    # save the image for debug purposes.
    round_image.save("round.png")
    # convert it to a string, with only specified characters allowed.
    round_text = pytesseract.image_to_string(
        round_image, config="-c tessedit_char_whitelist=/0123456789 --psm 6",
    )

    # convert it into a [int, int] tuple if possible.
    try:
        round = list(map(int, round_text.split("/")))
    except ValueError:
        round = [0]
    return round


class Monkey:
    def __init__(self, monkey: str, delay: int = 0.1):

        # initialize monkey's attributes.
        self.name = monkey
        self.delay = delay
        self.upgrades = [0, 0, 0]
        self.targeting_options = ["First", "Last", "Close", "Strong"]
        self.targeting = "First"
        self.sold = False
        self.placed = False

        # update information about monkey
        # self.get_info()

    def place(self, coordinates: Tuple[int, int]):

        # raise MonkeyPlaced if the monkey has already been placed.
        if self.placed:
            raise MonkeyPlaced

        # raise CoordinateError if invalid type or tuple length.
        if (type(coordinates) != list) and (type(coordinates) != tuple):
            raise CoordinateError
        if len(coordinates) != 2:
            raise CoordinateError

        # activate Bloons TD 6 window.
        focus_window("BloonsTD6")

        # move to the monkey's position
        # send the hotkey for the monkey
        # left click to place the monkey
        # time.sleep required for the monkey to be placed in time.
        mouse.move(coordinates[0], coordinates[1])
        time.sleep(self.delay)
        keyboard.send(hotkeys["Monkeys"][self.name])
        time.sleep(self.delay)
        mouse.click()
        time.sleep(self.delay)

        # record the coordinates of the monkey.
        self.coordinates = coordinates

        # record that the monkey has been placed.
        self.placed = True

    def select(self):

        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # raise CoordinateError if invalid type or tuple length.
        if (type(self.coordinates) != list) and (type(self.coordinates) != tuple):
            raise CoordinateError
        if len(self.coordinates) != 2:
            raise CoordinateError

        mouse.move(self.coordinates[0], self.coordinates[1])
        time.sleep(self.delay)
        mouse.click()
        time.sleep(self.delay)

    def upgrade(self, upgrades: Tuple[int, int, int], skip_esc: bool = False):

        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # raise UpgradeError if invalid type or tuple length.
        if (type(upgrades) != list) and (type(upgrades) != tuple):
            raise UpgradeError
        if len(upgrades) != 3:
            raise UpgradeError

        # raise UpgradeError if all paths have tiers active.
        if upgrades.count(0) == 0:
            raise UpgradeError

        # raise UpgradeError there is a path above the 5th tier or below the base tier.
        if max(upgrades) > 5 or min(upgrades) < 0:
            raise UpgradeError

        # raise UpgradeError if there is more than one path at tier 3 or higher
        third_tier_upgrade_count = len([i for i in upgrades if i >= 3])
        if third_tier_upgrade_count > 1:
            raise UpgradeError

        # activate Bloons TD 6 window.
        focus_window("BloonsTD6")

        # move to the monkey's position
        # send the hotkey for (current upgrade - previous upgrade)
        # send escape to get out of upgrade menu
        self.select()
        for path in range(len(upgrades)):
            for tier in range(upgrades[path] - self.upgrades[path]):
                keyboard.send(hotkeys["Monkeys"]["Upgrades"][path])
                time.sleep(self.delay)
        if not skip_esc:
            keyboard.send("esc")
            time.sleep(self.delay)

        # record the upgrades of the monkey.
        self.upgrades = upgrades

        # update information about monkey
        # self.get_info(self.name)

    def target(self, targeting: str):

        # raise TargetingError if targeting not in targeting_options.
        if targeting not in self.targeting_options:
            raise TargetingError

        # find difference between indexes of new targeting and old targeting
        targeting_index_old = self.targeting_options.index(self.targeting)
        targeting_index = self.targeting_options.index(targeting)
        targeting_index_change = targeting_index - targeting_index_old
        self.select()

        # if new targeting index is lower than old one, use reverse targeting hotkey
        if targeting_index_change <= 0:
            for i in range(abs(targeting_index_change)):
                keyboard.send(hotkeys["Monkeys"]["Change Targeting"][0])
                time.sleep(self.delay)

        # if new targeting index is higher than old one, use normal targeting hotkey
        else:
            for i in range(targeting_index_change):
                keyboard.send(hotkeys["Monkeys"]["Change Targeting"][1])
                time.sleep(self.delay)

        # send escape to get out of upgrade menu
        keyboard.send("esc")
        time.sleep(self.delay)

        # record the targetting of the monkey.
        self.targeting = targeting

    def sell(self):

        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # move to the monkey's position
        # sell monkey
        self.select()
        keyboard.send(hotkeys["Gameplay"]["Sell"])
        time.sleep(self.delay)

        # record that the monkey has been sold.
        self.sold = True

    def get_info(self, upgrades: Tuple[int, int, int] = None):

        # if no upgrade path is passed, use the one provided when the monkey was generated.
        if upgrades == None:
            upgrades = self.upgrades

        # raise UpgradeError if invalid type or tuple length.
        if (type(upgrades) != list) and (type(upgrades) != tuple):
            raise UpgradeError
        if len(upgrades) != 3:
            raise UpgradeError

        # raise UpgradeError if all paths have tiers active.
        if upgrades.count(0) == 0:
            raise UpgradeError

        # raise UpgradeError there is a path above the 5th tier or below the base tier.
        if max(upgrades) > 5 or min(upgrades) < 0:
            raise UpgradeError

        # raise UpgradeError if there is more than one path at tier 3 or higher
        third_tier_upgrade_count = len([i for i in upgrades if i >= 3])
        if third_tier_upgrade_count > 1:
            raise UpgradeError

        # get main path from the 3, represented by highest tier.
        self.main_tier = max(upgrades)
        self.main_path = upgrades.index(self.main_tier)

        # set basic monkey data
        self.monkey_description = monkeys[self.name]["description"]

        # calculate monkey prices for different difficulties.
        self.monkey_price_medium = monkeys[self.name]["price"]
        self.monkey_price_easy = price_round(0.85 * self.monkey_price_medium)
        self.monkey_price_hard = price_round(1.08 * self.monkey_price_medium)
        self.monkey_price_impoppable = price_round(1.2 * self.monkey_price_medium)

        # reset upgrade info every time this method is called.
        self.upgrade_name = None
        self.upgrade_description = None

        self.upgrade_price_medium = 0
        self.upgrade_price_easy = 0
        self.upgrade_price_hard = 0
        self.upgrade_price_impoppable = 0

        # only run this if the monkey has been upgraded.
        if upgrades != [0, 0, 0]:

            # get basic upgrade data from monkeys.json
            self.upgrade_name = monkeys[self.name]["upgrades"][self.main_path][
                self.main_tier - 1
            ]["name"]
            self.upgrade_description = monkeys[self.name]["upgrades"][self.main_path][
                self.main_tier - 1
            ]["description"]

            # calculate upgrade prices for different difficulties.
            self.upgrade_price_medium = monkeys[self.name]["upgrades"][self.main_path][
                self.main_tier - 1
            ]["price"]
            self.upgrade_price_easy = price_round(0.85 * self.upgrade_price_medium)
            self.upgrade_price_hard = price_round(1.08 * self.upgrade_price_medium)
            self.upgrade_price_impoppable = price_round(1.2 * self.upgrade_price_medium)

        # calculate total prices for different difficulties.
        self.total_price_medium = self.monkey_price_medium
        for path in range(len(upgrades)):
            for tier in range(upgrades[path]):
                self.total_price_medium += monkeys[self.name]["upgrades"][path][tier][
                    "price"
                ]
        self.total_price_easy = price_round(0.85 * self.total_price_medium)
        self.total_price_hard = price_round(1.08 * self.total_price_medium)
        self.total_price_impoppable = price_round(1.2 * self.total_price_medium)


class Hero:
    def __init__(self, hero: str, delay: int = 0.1):
        self.name = hero
        self.delay = delay
        self.level = 0
        self.targeting = "First"
        self.targeting_options = ["First", "Last", "Close", "Strong"]
        self.sold = False
        self.placed = False

    def place(self, coordinates: Tuple[int, int]):

        # raise MonkeyPlaced if the monkey has already been placed.
        if self.placed:
            raise MonkeyPlaced

        # raise CoordinateError if invalid type or tuple length.
        if (type(coordinates) != list) and (type(coordinates) != tuple):
            raise CoordinateError
        if len(coordinates) != 2:
            raise CoordinateError

        # activate Bloons TD 6 window.
        focus_window("BloonsTD6")

        # move to the monkey's position
        # send the hotkey for the monkey
        # left click to place the monkey
        # time.sleep required for the monkey to be placed in time.
        mouse.move(coordinates[0], coordinates[1])
        time.sleep(self.delay)
        keyboard.send(hotkeys["Monkeys"]["Heroes"])
        time.sleep(self.delay)
        mouse.click()
        time.sleep(self.delay)

        # record the coordinates of the monkey.
        self.coordinates = coordinates

        # record that the monkey has been placed.
        self.placed = True
        self.level = 1

    def select(self, coordinates: Tuple[int, int] = None):

        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # if no coordinates are passed, sue the ones provided when the monkey was placed.
        if coordinates == None:
            coordinates = self.coordinates

        # raise CoordinateError if invalid type or tuple length.
        if (type(coordinates) != list) and (type(coordinates) != tuple):
            raise CoordinateError
        if len(coordinates) != 2:
            raise CoordinateError

        mouse.move(coordinates[0], coordinates[1])
        time.sleep(self.delay)
        mouse.click()
        time.sleep(self.delay)

    def set_level(self, level: int = 1):
        self.level = level

    def upgrade(self, level: int = 1, skip_esc: bool = False):
        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # if no upgrade path is passed, use the one provided when the monkey was generated.

        # raise UpgradeError if invalid type.
        if type(level) != int:
            raise UpgradeError

        # raise UpgradeError there is a path above the 5th tier or below the base tier.
        if level > 20 or level < 1 or level < self.level:
            raise UpgradeError

        # move to the monkey's position
        # send the hotkey for (current level - previous level)
        # send escape to get out of upgrade menu
        self.select()
        for l in range(level - self.level):
            keyboard.send(hotkeys["Monkeys"]["Upgrades"][0])
            time.sleep(self.delay)
        if not skip_esc:
            keyboard.send("esc")
            time.sleep(self.delay)

        # record the level of the hero.
        self.set_level(level)

        # update information about hero
        # self.get_info(self.name)

    def target(self, targeting: str = None):

        # if no targeting is passed, use the one provided when the monkey was generated.
        if targeting == None:
            targeting = self.targeting

        # raise TargetingError if targeting not in targeting_options.
        if targeting not in self.targeting_options:
            raise TargetingError

        # find difference between indexes of new targeting and old targeting
        self.targeting_index_old = self.targeting_options.index(self.targeting)
        self.targeting_index = self.targeting_options.index(targeting)
        self.targeting_index_change = self.targeting_index - self.targeting_index_old
        self.select()

        # if new targeting index is lower than old one, use reverse targeting hotkey
        if self.targeting_index_change <= 0:
            for i in range(abs(self.targeting_index_change)):
                keyboard.send(hotkeys["Monkeys"]["Change Targeting"][0])
                time.sleep(self.delay)

        # if new targeting index is higher than old one, use normal targeting hotkey
        else:
            for i in range(self.targeting_index_change):
                keyboard.send(hotkeys["Monkeys"]["Change Targeting"][1])
                time.sleep(self.delay)

        # send escape to get out of upgrade menu
        keyboard.send("esc")
        time.sleep(self.delay)

        # record the targetting of the monkey.
        self.targeting = targeting

    def sell(self):

        # raise exceptions if the monkey hasn't been placed or has been already sold.
        if not self.placed:
            raise MonkeyNotPlaced
        if self.sold:
            raise MonkeySold

        # move to the monkey's position
        # sell monkey
        self.select()
        keyboard.send(hotkeys["Gameplay"]["Sell"])
        time.sleep(self.delay)

        # record that the monkey has been sold.
        self.sold = True

    def get_info(self, name: str = None, upgrades: Tuple[int, int, int] = None):

        # if no upgrade path is passed, use the one provided when the monkey was generated.
        if upgrades == None:
            upgrades = self.upgrades

        # if no monkey name is passed, use the one provided when the monkey was generated.
        if name == None:
            name = self.name

        # raise UpgradeError if invalid type or tuple length.
        if (type(upgrades) != list) and (type(upgrades) != tuple):
            raise UpgradeError
        if len(upgrades) != 3:
            raise UpgradeError

        # raise UpgradeError if all paths have tiers active.
        if upgrades.count(0) == 0:
            raise UpgradeError

        # raise UpgradeError there is a path above the 5th tier or below the base tier.
        if max(upgrades) > 5 or min(upgrades) < 0:
            raise UpgradeError

        # raise UpgradeError if there is more than one path at tier 3 or higher
        third_tier_upgrade_count = len([i for i in upgrades if i >= 3])
        if third_tier_upgrade_count > 1:
            raise UpgradeError

        # get main path from the 3, represented by highest tier.
        self.main_tier = max(upgrades)
        self.main_path = upgrades.index(self.main_tier)

        # set basic monkey data
        self.name = name
        self.monkey_description = monkeys[name]["description"]

        # calculate monkey prices for different difficulties.
        self.monkey_price_medium = monkeys[name]["price"]
        self.monkey_price_easy = price_round(0.85 * self.monkey_price_medium)
        self.monkey_price_hard = price_round(1.08 * self.monkey_price_medium)
        self.monkey_price_impoppable = price_round(1.2 * self.monkey_price_medium)

        # reset upgrade info every time this method is called.
        self.upgrade_name = None
        self.upgrade_description = None

        self.upgrade_price_medium = 0
        self.upgrade_price_easy = 0
        self.upgrade_price_hard = 0
        self.upgrade_price_impoppable = 0

        # only run this if the monkey has been upgraded.
        if upgrades != [0, 0, 0]:

            # get basic upgrade data from monkeys.json
            self.upgrade_name = monkeys[name]["upgrades"][self.main_path][
                self.main_tier - 1
            ]["name"]
            self.upgrade_description = monkeys[name]["upgrades"][self.main_path][
                self.main_tier - 1
            ]["description"]

            # calculate upgrade prices for different difficulties.
            self.upgrade_price_medium = monkeys[name]["upgrades"][self.main_path][
                self.main_tier - 1
            ]["price"]
            self.upgrade_price_easy = price_round(0.85 * self.upgrade_price_medium)
            self.upgrade_price_hard = price_round(1.08 * self.upgrade_price_medium)
            self.upgrade_price_impoppable = price_round(1.2 * self.upgrade_price_medium)

        # calculate total prices for different difficulties.
        self.total_price_medium = self.monkey_price_medium
        for path in range(len(upgrades)):
            for tier in range(upgrades[path]):
                self.total_price_medium += monkeys[name]["upgrades"][path][tier][
                    "price"
                ]
        self.total_price_easy = price_round(0.85 * self.total_price_medium)
        self.total_price_hard = price_round(1.08 * self.total_price_medium)
        self.total_price_impoppable = price_round(1.2 * self.total_price_medium)


class Ability:
    def __init__(
        self,
        monkey: Union[Monkey, Hero],
        hotkey_index: int,
        ability_name: str = None,
        upgrades: Union[Tuple[int, int, int], int] = None,
    ):

        # initialize ability's attributes.
        self.monkey = monkey
        self.name = monkey.name
        self.hotkey_index = hotkey_index
        self.ability_name = ability_name

        if type(monkey) == Monkey:

            # if no upgrade path is passed, use the one provided when the monkey was generated.
            if upgrades == None:
                self.upgrades = monkey.upgrades

            # raise AbilityError if the monkey's upgrade doesn't have an ability.
            if (
                "abilities"
                not in monkeys[self.name]["upgrades"][monkey.main_path][
                    monkey.main_tier - 1
                ].keys()
            ):
                raise AbilityError

            # set list of monkey's abilities in ability_list
            self.ability_list = monkeys[self.name]["upgrades"][monkey.main_path][
                monkey.main_tier - 1
            ]["abilities"]

            # if ability_name isn't passed, default to the first ability that the monkey has.
            # if it is, then find the index of it and set it to that.
            if ability_name == None:
                self.ability_dict = self.ability_list[0]
            else:
                for ability_dict in self.ability_list:
                    if ability_dict["name"] == ability_name:
                        self.ability_dict = ability_dict

            # update information about ability
            self.get_info()
        elif type(monkey) == Hero:

            # if no upgrade path is passed, use the one provided when the monkey was generated.
            if upgrades == None:
                self.level = monkey.level

            # raise AbilityError if the monkey's upgrade doesn't have an ability.
            if "abilities" not in heroes[self.name]["levels"][self.level - 1]:
                print(heroes[self.name]["levels"][self.level - 1])
                raise AbilityError

            # set list of monkey's abilities in ability_list
            self.ability_list = heroes[self.name]["levels"][self.level - 1]["abilities"]

            # if ability_name isn't passed, default to the first ability that the monkey has.
            # if it is, then find the index of it and set it to that.
            if ability_name == None:
                self.ability_dict = self.ability_list[0]
            else:
                for ability_dict in self.ability_list:
                    if ability_dict["name"] == ability_name:
                        self.ability_dict = ability_dict

            # update information about ability
            self.get_info()

    def activate(
        self,
        hotkey_index=None,
        coordinates_1: Tuple[int, int] = None,
        coordinates_2: Tuple[int, int] = None,
    ):

        # if no hotkey_index is passed, use the one provided when the ability was generated.
        if hotkey_index == None:
            hotkey_index = self.hotkey_index

        # type 0 - just activate ability
        # i.e. Super Monkey Fan Club
        if self.ability_dict["type"] == 0:
            keyboard.send(hotkeys["Gameplay"]["Activated Abilities"][hotkey_index - 1])
            time.sleep(self.monkey.delay)

        # type 1 - activate ability then click once.
        # i.e. Overclock
        elif self.ability_dict["type"] == 1:
            keyboard.send(hotkeys["Gameplay"]["Activated Abilities"][hotkey_index - 1])
            time.sleep(self.monkey.delay)
            mouse.move(coordinates_1[0], coordinates_1[1])
            time.sleep(self.monkey.delay)
            mouse.click()
            time.sleep(self.monkey.delay)

        # type 2 - activate ability then click twice.
        # i.e. Chinook Reposition
        elif self.ability_dict["type"] == 2:
            keyboard.send(hotkeys["Gameplay"]["Activated Abilities"][hotkey_index - 1])
            time.sleep(self.monkey.delay)
            mouse.move(coordinates_1[0], coordinates_2[1])
            time.sleep(self.monkey.delay)
            mouse.click()
            time.sleep(self.monkey.delay)
            mouse.move(coordinates_2[0], coordinates_2[1])
            time.sleep(self.monkey.delay)
            mouse.click()
            time.sleep(self.monkey.delay)

    def get_info(self, ability_dict=None):

        # if ability_dict != provided, use the one provided when the ability was generated.
        if ability_dict == None:
            ability_dict = self.ability_dict

        # turn ability dictionary values into attributes.
        self.ability_name = ability_dict["name"]
        self.ability_cooldown = ability_dict["cooldown"]
        self.ability_type = ability_dict["type"]


def play():
    keyboard.send(hotkeys["Gameplay"]["Play/Fast Forward"])
    time.sleep(0.1)


def confirm():
    keyboard.send("enter")
    time.sleep(0.1)
    keyboard.send("esc")
    time.sleep(0.1)
