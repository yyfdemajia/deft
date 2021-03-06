#!/usr/bin/python2

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import argparse

parser = argparse.ArgumentParser(description='Creates data for a FE vs gw plot.')

parser.add_argument('--kT', metavar='temperature', type=float,
                    help='reduced temperature - REQUIRED')
parser.add_argument('--nmin', type=float,
                    help='min density - REQUIRED')
parser.add_argument('--nmax', type=float,
                    help='max density - REQUIRED')
parser.add_argument('--dn', type=float,
                    help='change of density', default=0.01)

parser.add_argument('--dgw', type=float,
                    help='change in gw', default=0.01)
parser.add_argument('--maxgw', type=float,
                    help='max gw', default=0.15)

parser.add_argument('--fv', metavar='vacancies', type=float,
                    help='fraction of vacancies - Default 0')
parser.add_argument('--gw', metavar='width', type=float,
                    help='width of Gaussian - Default 0.01')
parser.add_argument('--dx', metavar='dx', type=float,
                    help='scaling dx - Default 0.5')
parser.add_argument('--mcerror', metavar='mc_error', type=float,
                    help='monte carlo mc_error - Default 0.001')
parser.add_argument('--mcconstant', metavar='const', type=int,
                    help='monte carlo integration mc_constant - Default 5')
parser.add_argument('--mcprefactor', metavar='prefac', type=int,
                    help='monte carlo integration mc_prefactor - Default 50000')
parser.add_argument('--datafile', metavar='addtoname', type=str,
                    help='added to name of data file - Default "FE_vs_gw"')

args=parser.parse_args()

kT=args.kT

if args.fv:
    fv=args.fv
else :
    fv=0

if args.dx:
    dx=args.dx
else :
    dx=.5

if args.mcerror:
    mcerror=args.mcerror
else :
    mcerror=0.001

if args.mcconstant:
    mcconstant=args.mcconstant
else :
    mcconstant=5
    
if args.mcprefactor:
    mcprefactor=args.mcprefactor
else :
    mcprefactor=50000

if args.datafile:    
    datafile='FE_vs_gw_'+args.filedat
else :
    datafile='FE_vs_gw'

for n in np.arange(args.nmin, args.nmax, args.dn):
    cmd = 'rq run -J isotherm-kT%g-n%g' % (kT, n)
    cmd += ' figs/new-melting.mkdat --kT %g --n %g' % (kT, n)
    cmd += ' --gwstart=%g --gwend %g --gwstep %g' % (args.dgw, args.maxgw, args.dgw)
    cmd += ' --fv %g --dx %g' % (fv, dx)
    cmd += ' --mc-error %g --mc-constant %g --mc-prefactor %g' % (mcerror, mcconstant, mcprefactor)
    cmd += ' --filename isotherm-kT-%g.dat' % kT
    print(cmd)
    os.system(cmd)



