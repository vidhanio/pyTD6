from pytd6 import Monkey, Hotkey

temple = Monkey("Super Monkey")
primary_sacrifice = Monkey("Dart Monkey")
military_sacrifice = Monkey("Sniper Monkey")
magic_sacrifice = Monkey("Ninja Monkey")

temple.place([1100, 520])
temple.upgrade([0, 2, 0])

primary_sacrifice.place([1090, 365])
primary_sacrifice.upgrade([0, 5, 0])

military_sacrifice.place([1317, 531])
military_sacrifice.upgrade([5, 0, 0])

magic_sacrifice.place([1037, 709])
magic_sacrifice.upgrade([0, 0, 5])

temple.upgrade([4, 0, 2], skip_esc=True)
Hotkey.confirm()

primary_sacrifice = Monkey("Dart Monkey")
military_sacrifice = Monkey("Sniper Monkey")
magic_sacrifice = Monkey("Ninja Monkey")
support_sacrifice = Monkey("Spike Factory")

primary_sacrifice.place([1090, 365])
primary_sacrifice.upgrade([0, 5, 0])

military_sacrifice.place([1317, 531])
military_sacrifice.upgrade([5, 0, 0])

magic_sacrifice.place([1037, 709])
magic_sacrifice.upgrade([0, 0, 5])

support_sacrifice.place([1170, 722])
support_sacrifice.upgrade([0, 5, 0])

temple.upgrade([5, 0, 2], skip_esc=True)
Hotkey.confirm()

permanent_brew = Monkey("Alchemist")
permanent_brew.place([1309, 529])
permanent_brew.upgrade([5, 0, 2])

