#!/usr/bin/python

import pylab

# Read in data
data = pylab.loadtxt('prefac-out.txt')

T = data[:,0]
nvapor = data[:,1]
nliquid = data[:,2]

# Plot the curve
pylab.plot(nvapor, T)
pylab.plot(nliquid, T)

pylab.xlabel('n (g/mL)')
pylab.ylabel('T (K)')

pylab.show()
