import monkdata as m
from dtree import *

print("MONK-1 " + str() + "\n")
for i in range(0,6):
    print("a" + str(i+1) + " = " + str(averageGain(m.monk1, m.attributes[i])) + "\n")

print("MONK-2\n")
for i in range(0,6):
    print("a" + str(i+1) + " = " + str(averageGain(m.monk2, m.attributes[i])) + "\n")

print("MONK-3\n")
for i in range(0,6):
    print("a" + str(i+1) + " = " + str(averageGain(m.monk3, m.attributes[i])) + "\n")