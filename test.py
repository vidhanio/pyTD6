import pytd6
from pytd6 import monkey

pytd6.init([1920, 1080])

dart_monkey_1 = monkey("Dart Monkey")
dart_monkey_1.place([500, 400])
dart_monkey_1.upgrade([2, 3, 0])
