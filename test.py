import pytd6, time
from pytd6 import monkey

dms = []

for i in range(5):
    dms.append(monkey("Dart Monkey"))

dms[0].place([790, 380])
dms[1].place([252, 342])
dms[2].place([476, 966])
dms[3].place([1424, 744])
dms[4].place([1183, 107])

for dm in dms:
    dm.upgrade([0, 2, 5])

