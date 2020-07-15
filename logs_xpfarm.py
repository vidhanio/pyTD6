from pytd6 import monkey

mauler_1 = monkey("Bomb Shooter")
mauler_2 = monkey("Bomb Shooter")
mauler_3 = monkey("Bomb Shooter")

mauler_1.place([560, 470])
mauler_2.place([560, 570])
mauler_3.place([560, 710])

mauler_1.upgrade([0, 3, 0])
mauler_2.upgrade([0, 3, 0])
mauler_3.upgrade([0, 3, 0])


reactor_1 = monkey("Monkey Sub")
reactor_2 = monkey("Monkey Sub")

reactor_1.place([780, 520])
reactor_2.place([880, 520])

reactor_1.upgrade([4, 0, 0])
reactor_2.upgrade([4, 0, 0])
