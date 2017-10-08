from cvxopt.solvers import qp 
from cvxopt.base import matrix

import numpy , pylab , random , math


def createP(x, t, kernel):
    P = []
    for i in range(len(x)):
        Pi = []
        for j in range(len(x)):
            res = t[i] * t[j] * kernel(x[i,:], x[j,:])
            Pi.append(res) 
        P.append(Pi)
    return numpy.array(P)

def nonZeroAlpha(alpha, threshold):
    nonZ = []
    for i in range(len(alpha)):
        if alpha[i] >= threshold:
            nonZ.append(i)
    return nonZ


def euclidDist(x, y):
    return math.sqrt( (x[0] - y[0]) **2   +   (x[1] - y[1])** 2 )



def linearKernel(x, y):
    return x.transpose().dot(y) + 1;

def polynomialKernel(x, y, p = 3):
    return (x.dot(y) +1)**p

def radialBasisKernel(x, y, sigma = 1.5):
    return math.exp(  - euclidDist(x,y)  /  (2 * (sigma ** 2)) )
    


def indicator(row, X, t, alpha, nonZeroIdx, kernel):
    return numpy.sum( [ alpha[i] * t[i] * kernel(row, X[i,:]) for i in nonZeroIdx ] )

def plot(x):
    xr=numpy.arange(-4, 4, 0.05) 
    yr=numpy.arange(-4, 4, 0.05)
    grid=matrix([[indicator(x, y) 
        for y in yr ] 
        for x in xr])
    pylab.contour(xr, yr, grid, (-1.0, 0.0, 1.0),
    colors=("red", "black", "blue"), linewidths=(1, 3, 1))


def main(N, kernel, useSlack = True, slackCoeff = 1):
    # Random data
    
    # numpy.random.seed(100)
    classA = [ (random.normalvariate(-1.5, 1),
                random.normalvariate(0.5, 1),
                1.0) for i in range (N/4) ] + \
            [ ( random.normalvariate(1.5, 1),
               random.normalvariate(0.5, 1),
               1.0) for i in range (N/4) ]
    classB = [ ( random.normalvariate(0.0, 0.5),
                random.normalvariate(-0.5, 0.5),
                -1.0) for i in range (N/2) ]
    data = classA + classB
    
    # Show data
    
    pylab.hold(True)
    pylab.plot( [p[0] for p in classA],
                [p[1] for p in classA],
                'bo')
    pylab.plot( [p[0] for p in classB],
                [p[1] for p in classB],
                'ro')
    pylab.show()
    
    random.shuffle(data)
    
    
    arrayClassA = numpy.array([[row[0], row[1]] for row in classA])
    arrayClassB = numpy.array([[row[0], row[1]] for row in classB])
    
    X = numpy.array([[row[0], row[1]] for row in data])
    t = numpy.array([row[2] for row in data])
    
    # Create P
    P = createP(X, t, kernel)
    
    # Init q, h, G
    q = -numpy.ones(N)
    
    # Use of slack parameter
    if useSlack:
        h = numpy.concatenate((numpy.zeros(N), numpy.ones(N) * slackCoeff))
    else:
        h = numpy.zeros(N)
      
    # Use of slack parameter
    if useSlack:
        G = numpy.concatenate((-numpy.identity(N), numpy.identity(N)))
    else:
        G = -numpy.identity(N)
    
    # Call qp
    r = qp(matrix(P) , matrix(q) , matrix(G) , matrix(h))
    alpha = list(r['x'])
    
    # Search alpha > threshold (not zero alphas)
    nonZIdx = nonZeroAlpha(alpha, 0.00001)
    
    xr = numpy.arange(-4, 4, 0.05)
    yr = numpy.arange(-4, 4, 0.05)
    grid = matrix( [    [indicator(numpy.array((x, y)), X, t, alpha, nonZIdx, kernel) for y in yr ]  for x in xr ] )
    
    # Show results
    
    pylab.hold(1)
    pylab.plot(arrayClassA[:,0], arrayClassA[:,1],'bo')
    pylab.plot(arrayClassB[:,0], arrayClassB[:,1],'ro')
    
    pylab.contour(xr, yr, grid,
                  (-1.0, 0.0, 1.0),
                  colors = ('red', 'black', 'blue'),
                  linewidths = (1,3,1))
    pylab.show()
# End main


for kernel in [linearKernel, polynomialKernel, radialBasisKernel]:
    for N in [20, 100]:
        main(N, kernel, False)
        main(N, kernel, True)