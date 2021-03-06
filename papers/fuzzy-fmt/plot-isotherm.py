#!/usr/bin/python2
from __future__ import print_function, division

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os, glob
import argparse

parser = argparse.ArgumentParser(description='Creates data for a FE vs gw plot.')

parser.add_argument('--kT', metavar='temperature', type=float,
                    help='reduced temperature - REQUIRED')

args=parser.parse_args()

kT=args.kT

n = []
gw = []
fe_difference = []

files = sorted(list(glob.glob('crystallization/kT%.3f_n*_best.dat' % kT)))
for f in files:
    data = np.loadtxt(f)
    n.append(data[1])
    gw.append(data[3])
    fe_difference.append(data[6])

plt.figure()
plt.plot(n, gw, '.-')
plt.xlabel('n')
plt.ylabel('gw')

plt.figure()
plt.plot(n, fe_difference, '.-')
plt.axhline(0, color='k')
plt.xlabel('n')
plt.ylabel('FED')

plt.show()
