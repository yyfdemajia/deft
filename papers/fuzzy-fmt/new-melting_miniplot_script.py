#!/usr/bin/python2
#NOTE: Run this plot script from directory deft/papers/fuzzy-fmt 
#with comand ./new-melting_miniplot_script.py [directory where data stored] [temp]
#to create plots from plot.dat files already in the data directory

import os
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 3:
    print "Usage: directory temperature"
    exit(1)

data_directory=sys.argv[1]
temp=sys.argv[2]
data_file=data_directory+"/plot_kT"+temp+".dat"

thisdata = np.loadtxt(data_file)
print thisdata

densities=thisdata[:,1]
crystal_energies_per_atom = thisdata[:,2]
homogeneous_energies_per_atom = thisdata[:,3]
energy_differences_per_atom = thisdata[:,4]
crystal_energies_per_volume = thisdata[:,5]

print 'densities', densities
print 'crystal_energies_per_atom', crystal_energies_per_atom
print 'homogeneous_energies_per_atom', homogeneous_energies_per_atom
print 'energy_differences_per_atom', energy_differences_per_atom
print 'crystal_energies_per_volume', crystal_energies_per_volume

plot1=data_directory+"/plot1_cFEvsDen_kT"+temp+".png"
plot2=data_directory+"/plot2_hFEvsDen_kT"+temp+".png"
plot3=data_directory+"/plot3_Pressure_kT"+temp+".png"

# Plot Crystal Free Energy per sphere vs Reduced Density
plt.plot(densities, crystal_energies_per_atom)
plt.title('Crystal Free Energy per sphere vs Reduced Density at Fixed kT='+temp)
plt.xlabel('Reduced Density')
plt.ylabel('Crystal Free Energy')
plt.savefig(plot1)

plt.figure()

# Plot Crystal Free Energy per sphere vs Reduced Density
plt.plot(densities, homogeneous_energies_per_atom)
plt.title('Homogeneous Free Energy per sphere vs Reduced Density at Fixed kT='+temp)
plt.xlabel('Reduced Density')
plt.ylabel('Homogeneous Free Energy')
plt.savefig(plot2)

plt.figure()

f =crystal_energies_per_atom
#print "f=", f
df=np.diff(f)  #Caution: depends on order of data files!
#print "df=", df
n =densities
#print "n=", n
dn=np.diff(n)  #Caution: depends on order of data files!
#print "dn=", dn
mid_n=n[0:len(n)-1]+dn/2
#print "mid_n=", mid_n
pressure = -(mid_n*mid_n)*(df/dn) #for fixed N and T
#print "pressure =", pressure

# Plot Pressure vs Reduced Density
plt.plot(mid_n, pressure)
plt.title('Reduced Pressure vs Reduced Density at Fixed kT='+temp)
plt.xlabel('Reduced Density')
plt.ylabel('Reduced Pressure')
plt.savefig(plot3)

plt.show()

