from cvxopt.solvers import qp 
from cvxopt.base import matrix

import numpy , pylab , random , math

def main():
    N = 1000
    print("Get N random data")
    
    print("Compute P")
    P = createP(X, T)
    print("Init q and h vectors and G matrix")
    g = [-1 for i in range(N)]
    h = [0 for i in range(N)]
    G = numpy.identity(N)
    print("Call qp")  
    r = qp(matrix(P) , matrix(q) , matrix(G) , matrix(h))
    alpha = list(r['x'])

def createP(x, t):
    P = []
    for i in range(len(x)):
        Pi = []
        for j in range(len(x)):
            res = t[i] * t[j] * linearKernel(x[i], x[j])
            Pi.append(res) 
        P.append(Pi)
    return P

def approximate(x, threshold):
    xApp = []
    for i in range(len(x)):
        if x[i] >= threshold:
            xApp.append(x[i])
        else:
            xApp.append(0)
    return xApp

def linearKernel(x, y):
    return x.transpose() * y + 1;

def plot(x):
    xrange=numpy.arange(-4, 4, 0.05) 
    yrange=numpy.arange(-4, 4, 0.05)
    grid=matrix([[indicator(x, y) 
        for y in yrange ] 
        for x in xrange])
    pylab.contour(xrange, yrange, grid, (-1.0, 0.0, 1.0),
    colors=("red", "black", "blue"), linewidths=(1, 3, 1))

main()