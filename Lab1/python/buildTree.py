import monkdata as m
from dtree import *

t=buildTree(m.monk1, m.attributes);
print("MONK-1 " + str() + "\n")
print(1 - check(t, m.monk1))
print(1 - check(t, m.monk1test))

t=buildTree(m.monk2, m.attributes);
print("MONK-2 " + str() + "\n")
print(1 - check(t, m.monk2))
print(1 - check(t, m.monk2test))

t=buildTree(m.monk3, m.attributes);
print("MONK-3 " + str() + "\n")
print(1 - check(t, m.monk3))
print(1 - check(t, m.monk3test))