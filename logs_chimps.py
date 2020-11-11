import pytd6, time
from pytd6 import Monkey, Hero, get_cash

# Setup monkeys

druids = []
for i in range(6):
    druids.append(Monkey("Druid", 0.1))

obyn = Hero("Obyn Greenfoot", 0.5)

village = Monkey("Monkey Village")

alchemists = [Monkey("Alchemist"), Monkey("Alchemist")]


# Setup monkey coords

druid_coords = [[470, 580], [550, 580], [630, 580], [470, 510], [550, 510], [630, 510]]
obyn_coords = [630, 680]
village_coords = [530, 700]
alchemist_coords = [[510, 460], [590, 460]]

# Actual Gameplay

druids[0].place(druid_coords[0])

pytd6.play()
pytd6.play()

while pytd6.get_cash() < 700:
    time.sleep(1)

obyn.place(obyn_coords)

for druid_index in range(1, len(druids)):

    while pytd6.get_cash() < 460:
        time.sleep(1)

    druids[druid_index].place(druid_coords[druid_index])

obyn.set_level(3)

brambles = pytd6.Ability(obyn, 1)

while pytd6.get_round()[0] != 24:
    print(pytd6.get_round())
    time.sleep(1)

brambles.activate()

while pytd6.get_round()[0] != 33:
    print(pytd6.get_round())
    time.sleep(1)


village.place(village_coords)

village.upgrade([1, 2, 0])

for druid in druids:
    while get_cash() < 270:
        time.sleep(1)

    druid.upgrade([0, 1, 0])

for druid in druids:
    while get_cash() < 110:
        time.sleep(1)

    druid.upgrade([0, 1, 1])

for druid in druids:
    while get_cash() < 325:
        time.sleep(1)

    druid.upgrade([0, 1, 2])

for druid in druids:
    while get_cash() < 650:
        time.sleep(1)

    druid.upgrade([0, 1, 3])


while get_cash() < 595:
    time.sleep(1)

alchemists[0].place(alchemist_coords[0])

while get_cash() < 270:
    time.sleep(1)

alchemists[0].upgrade([1, 0, 0])

while get_cash() < 380:
    time.sleep(1)

alchemists[0].upgrade([2, 0, 0])

while get_cash() < 1350:
    time.sleep(1)

alchemists[0].upgrade([3, 0, 0])

while get_cash() < 3240:
    time.sleep(1)

alchemists[0].upgrade([4, 0, 0])

while get_cash() < 700:
    time.sleep(1)

alchemists[0].upgrade([4, 0, 1])


for druid in druids:
    while get_cash() < 2700:
        time.sleep(1)

    druid.upgrade([0, 1, 4])

while get_cash() < 595:
    time.sleep(1)

alchemists[1].place(alchemist_coords[1])

while get_cash() < 270:
    time.sleep(1)

alchemists[1].upgrade([1, 0, 0])

while get_cash() < 380:
    time.sleep(1)

alchemists[1].upgrade([2, 0, 0])

while get_cash() < 1350:
    time.sleep(1)

alchemists[1].upgrade([3, 0, 0])

while get_cash() < 3240:
    time.sleep(1)

alchemists[1].upgrade([4, 0, 0])

while get_cash() < 700:
    time.sleep(1)

alchemists[1].upgrade([4, 0, 1])

while get_cash() < 48600:
    time.sleep(1)

print(get_cash())

druids[5].upgrade([0, 1, 5])

while get_cash() < 1620:
    time.sleep(1)

village.upgrade([2, 2, 0])

while get_cash() < 8100:
    time.sleep(1)

village.upgrade([2, 3, 0])
