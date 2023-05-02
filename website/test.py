import pymongo

from __init__ import *

location = data_analysis['897c19387cc446e9affd38d10a827724']
hello = location.find_one()
print(hello['performance'])


