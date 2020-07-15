from pytd6 import monkey, hotkey

temple = monkey("Super Monkey")
primary_sacrifice = monkey("Dart Monkey")
military_sacrifice = monkey("Sniper Monkey")
magic_sacrifice = monkey("Ninja Monkey")

temple.place([1100, 520])
temple.upgrade([0, 2, 0])

primary_sacrifice.place([1090, 365])
primary_sacrifice.upgrade([0, 5, 0])

military_sacrifice.place([1317, 531])
military_sacrifice.upgrade([5, 0, 0])

magic_sacrifice.place([1037, 709])
magic_sacrifice.upgrade([0, 0, 5])

temple.upgrade([4, 0, 2], skip_esc=True)
hotkey.confirm()

primary_sacrifice = monkey("Dart Monkey")
military_sacrifice = monkey("Sniper Monkey")
magic_sacrifice = monkey("Ninja Monkey")
support_sacrifice = monkey("Spike Factory")

primary_sacrifice.place([1090, 365])
primary_sacrifice.upgrade([0, 5, 0])

military_sacrifice.place([1317, 531])
military_sacrifice.upgrade([5, 0, 0])

magic_sacrifice.place([1037, 709])
magic_sacrifice.upgrade([0, 0, 5])

support_sacrifice.place([1170, 722])
support_sacrifice.upgrade([0, 5, 0])

temple.upgrade([5, 0, 2], skip_esc=True)
hotkey.confirm()

permanent_brew = monkey("Alchemist")
permanent_brew.place([1309, 529])
permanent_brew.upgrade([5, 0, 2])

