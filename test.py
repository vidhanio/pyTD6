import pytd6, time
from pytd6 import monkey

dart_monkey_1 = monkey("Dart Monkey")
dart_monkey_1.place([500, 400])
dart_monkey_1.upgrade([2, 0, 0])
print(dart_monkey_1.upgrades)
dart_monkey_1.upgrade([3, 0, 0])
print(dart_monkey_1.upgrades)
dart_monkey_1.upgrade([3, 2, 0])
print(dart_monkey_1.upgrades)
time.sleep(5)
dart_monkey_1.sell()

pytd6.check_if_btd6_running()
