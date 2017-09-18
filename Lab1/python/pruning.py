import monkdata as m
from dtree import *
import random
import matplotlib.pyplot as plt
import statistics
import numpy as np

def partition(data, fraction):
    ldata = list(data)
    random.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]

fractions = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

errorTrain = [ [], [], [], [], [], [], [] ]
errorTest =  [ [], [], [], [], [], [], [] ]
candidate = 0

#LOOP for having average
for i in range(0,500):
    # for each fraction value possible for the dataset
    for key, fract in enumerate(fractions):
        # we partition
        monk3train, monk3val = partition(m.monk3, fract)
        
        candidateScore = 0
        t1 = buildTree(monk3train, m.attributes)
        nodes = allPruned(t1)
        if len(nodes) > 0:
            # LOOP until no improvement on error measure on test set
            while True:
                candidate = nodes[0]
                score = check(candidate, monk3val)
                # We check every node
                for n in nodes:
                    if check(n, monk3val) > check(candidate, monk3val):
                        candidate = n
                        score = check(candidate, monk3val)           
                # if no improvement, STOP
                if candidateScore > score:
                    break
                else:
                    candidateScore = score
                # Next pruning
                nodes = allPruned(candidate)
            # Adding error values
            errorTest[key].append(1-candidateScore)
            errorTrain[key].append(1-check(candidate, monk3train))
        

# Error measure plot
plt.plot(fractions, [sum(x)/float(len(x)) for x in errorTrain], color='r', label="Train set")
plt.plot(fractions, [sum(x)/float(len(x)) for x in errorTest], color='b', label="Test set")
plt.ylabel("Error measure on set")
plt.xlabel("Fraction of Train set")
plt.legend(loc='upper right', frameon=False)
plt.title("Error measure of pruning effect for monk3 dataset")
plt.show()

# Spread distribution of error measure
plt.plot(fractions, [statistics.variance(x) for x in errorTrain], color='r', label="Train set")
plt.plot(fractions, [statistics.variance(x) for x in errorTest], color='b', label="Test set")
plt.ylabel("Error measure distribution on set")
plt.xlabel("Fraction of Train set")
plt.legend(loc='upper right', frameon=False)
plt.title("Spread distribution of error measure for monk3 dataset")
plt.show()
 