from pytd6 import Hero, Ability

obyn = Hero("Obyn Greenfoot")
obyn.place([550, 680])
obyn.set_level(3)
brambles = Ability(obyn, 0)
brambles.activate()
