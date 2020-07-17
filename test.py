import pytd6, time
from pytd6 import Ability, Monkey

dm = Monkey("Dart Monkey")
dm.place([400, 250])
dm.upgrade([0, 4, 0])
time.sleep(5)
smfc = Ability(dm, 1)
smfc.activate()
time.sleep(5)
dm.sell()

dm = Monkey("Dart Monkey")
dm.place([400, 250])
dm.upgrade([0, 5, 0])
time.sleep(5)
pmfc = Ability(dm, 1)
pmfc.activate()
time.sleep(5)
dm.sell()
