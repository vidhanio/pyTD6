from pytd6 import Monkey
import time

# mauler_1 = Monkey("Bomb Shooter")
# mauler_1.place([560, 470])
# mauler_1.upgrade([0, 3, 0])
# mauler_1.target("Strong")

# mauler_2 = Monkey("Bomb Shooter")
# mauler_2.place([560, 570])
# mauler_2.upgrade([0, 3, 0])
# mauler_2.target("Strong")

# mauler_3 = Monkey("Bomb Shooter")
# mauler_3.place([560, 710])
# mauler_3.upgrade([0, 3, 0])
# mauler_3.target("Strong")


reactor_1 = Monkey("Monkey Sub")
reactor_1.place([780, 520])
reactor_1.upgrade([4, 0, 0])
reactor_1.targeting_options.append("Submerge")
reactor_1.targeting = "Submerge"

# reactor_2 = Monkey("Monkey Sub")
# reactor_2.place([880, 520])
# reactor_2.upgrade([4, 0, 0])
# reactor_2.targeting_options.append("Submerge")
# reactor_2.targeting = "Submerge"

reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
reactor_1.target("Strong")
reactor_1.target("Submerge")
