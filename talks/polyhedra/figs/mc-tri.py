from __future__ import division
import time
from pylab import *
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.animation as animation

ff = .5

# setup parameters
x0_setup = 1
y0_setup = 1
dx_setup = 2
dy_setup = 1.1
dy2_setup = 1.2

# for triangles
l = 1 # length from center to vertex
xdiff = 0.5
ydiff = 1/(2*sqrt(3))
ydiff2 = 1/sqrt(3)
area = (sqrt(3)/2*l)*(l/2)/2*6

# box
lenx = 20
leny = 10
edge = 1

n = int(ff*lenx*leny/area)
print n


# density
dx = 0.1
histogram = zeros(lenx/dx)
angle_histogram = zeros(lenx/dx)
xcoords = arange(0, lenx, dx) + dx/2

# Movement
phi_m = pi/32
r_m = .1

def move(pos):
  x = 2*rand()-1
  y = 2*rand()-1
  r2 = x*x + y*y
  while (r2 > 1):
      x = 2*rand()-1
      y = 2*rand()-1
      r2 = x*x + y*y
  fac = sqrt(-2*log(r2)/r2)
  newpos = pos + fac*r_m*array([x, y])
  while newpos[1] > leny: newpos[1] -= leny
  while newpos[1] < 0: newpos[1] += leny
  return newpos

def turn(angle):
  x = 2*rand()-1
  y = 2*rand()-1
  r2 = x*x + y*y
  while (r2 > 1):
      x = 2*rand()-1
      y = 2*rand()-1
      r2 = x*x + y*y
  fac = sqrt(-2*log(r2)/r2)
  ang = angle + fac*phi_m*x
  while ang > 2*pi/3:
    ang -= 2*pi/3
  while ang < 0:
    ang += 2*pi/3
  return ang

# Functions
def distsq(pos2, pos1):
  x = pos2[0] - pos1[0]
  if abs(pos2[1] - pos1[1]) < leny - abs(pos2[1] - pos1[1]):
    y = pos2[1] - pos1[1]
  else:
    y = leny - abs(pos2[1] - pos1[1])
  return x*x + y*y

def periodicDiff(pos2, pos1):
  if abs(pos2[1] - pos1[1]) < leny - abs(pos2[1] - pos1[1]):
    return pos2-pos1
  return array([pos2[0]-pos1[0], pos2[1]-pos1[1]-leny])

def touch(pos1, pos2, phi1, phi2):
  if (distsq(pos2, pos1) > 4*l*l):
    return False
  if (distsq(pos2, pos1) < l*l):
    return True
  v1 = verts(pos1, phi1)
  v2 = verts(pos2, phi2)
  for i in range(3):
    p1 = v1[i-1]
    p2 = v1[i]
    m1 = (p2[1]-p1[1])/(p2[0]-p1[0])
    b1 = p1[1]-m1*p1[0]
    for j in range(3):
      p3 = v2[j-1]
      p4 = v2[j]
      m2 = (p4[1]-p3[1])/(p4[0]-p3[0])
      b2 = p3[1]-m2*p3[0]
      xint = (b1-b2)/(m2-m1)
      if xint < p1[0] and xint > p2[0]:
        if xint < p3[0] and xint > p4[0]:
          return True
        if xint < p4[0] and xint > p3[0]:
          return True
      if xint < p2[0] and xint > p1[0]:
        if xint < p3[0] and xint > p4[0]:
          return True
        if xint < p4[0] and xint > p3[0]:
          return True
  return False

def verts(pos, phi):
  x = pos[0]
  y = pos[1]
  return array([[x+l*sin(phi), y+l*cos(phi)], [x+l*sin(phi+2*pi/3), y+l*cos(phi+2*pi/3)], [x+l*sin(phi + 4*pi/3), y+l*cos(phi + 4*pi/3)]])
##########################


centers = zeros((n+1, 2))
centers[n] = array([-100,-100])
angles = zeros(n+1)
colors = zeros(n+1)

# initial setup
x_setup = x0_setup
y_setup = y0_setup
phi_setup = 0
for i in range(n):
  centers[i, 0] = x_setup
  centers[i, 1] = y_setup
  angles[i] = phi_setup

  if max(verts(centers[i], angles[i])[:,0]) > lenx:
    x_setup = x0_setup + (pi - phi_setup)/pi*x0_setup
    y_setup += (pi - phi_setup)/pi*dy_setup + phi_setup/pi*dy2_setup
    phi_setup = pi - phi_setup
    centers[i, 0] = x_setup
    centers[i, 1] = y_setup
    angles[i] = phi_setup
  x_setup += dx_setup

coords = zeros((n, 3, 2))
for i in range(n):
  coords[i] = verts(centers[i], angles[i])
# Plotting
fig = figure()
ax = fig.add_subplot(221)
ax2 = fig.add_subplot(222, sharex=ax)
ax3 = fig.add_subplot(223, sharex=ax)
setp(ax.get_xticklabels(), visible=False)
#fig, (ax, ax2, ax3) = subplots(3,2, sharex=True)
#fig2 = figure(2)
#ax3 = fig2.add_subplot(111)

ax.axvline(x=0, linestyle='-', color='k', linewidth=3)
ax.axvline(x=lenx, linestyle='-', color='k', linewidth=3)
ax.axhline(y=0, linestyle='--', linewidth=3, color='b')
ax.axhline(y=leny, linestyle='--', linewidth=3, color='orange')



ax.set_ylim(-edge, leny+edge)
ax.set_xlim(-edge, lenx+edge)
ax2.set_title("density")
ax3.set_title("average angle")
line, = ax2.plot(xcoords, histogram)
angline, = ax3.plot(xcoords, angle_histogram)
ax2.set_xlim(-edge, lenx+edge)

def init():
  coll = PolyCollection(coords)
  ax.add_collection(coll)
  line.set_ydata(histogram)
  angline.set_ydata(angle_histogram)
  return line, ax2

cdefault = .3
cspecial = .9
count = 0
success = 0
skip = 100
def mc():
  global count, centers, angles, coords, skip, colors, histogram, success, angle_histogram
  for j in range(skip):
    count += 1
    for i in range(n):
      keep = True
      temp = move(centers[i])
      tempa = turn(angles[i])
      xs = verts(temp, tempa)[:,0]
      if max(xs) > lenx or min(xs) < 0:
        keep = False
      else:
        for j in range(n):
          if j != i and touch(temp, centers[j], tempa, angles[j]):
            keep = False
            break
      if keep:
        centers[i] = temp
        angles[i] = tempa
        coords[i] = verts(centers[i], angles[i])
        colors[i] += 1/skip
      if keep:
        success += 1
    for i in range(n):
      x = int(centers[i,0]/dx)
      if x >= 0 and x < len(histogram):
        histogram[x] += 1
        angle_histogram[x] += angles[i] - pi/3

def animate(p):
  global count, centers, angles, coords, skip, colors, histogram, success, angle_histogram
  mc()
  density = histogram/leny/dx/count
  line.set_ydata(density)
  angline.set_ydata(angle_histogram/count)
  ax2.set_ylim(0, 0.8)
  ax3.set_ylim(-.4, .4)
  coll = PolyCollection(coords)

  colors = zeros(n) + cdefault
  colors[0] = cspecial
  coll.set_color([cm.jet(x) for x in colors])
  ax.collections=[]
  ax.add_collection(coll)
  ax.set_title("Attempted moves: %i, Successful moves: %i" %(count*n, success))
  fig.tight_layout()
  #time.sleep(3)
  return line, ax2, ax3

fig.tight_layout()
ax.set_aspect('equal')
ax.set_ylim(-edge, leny+edge)

#anim = animation.FuncAnimation(fig, animate, init_func=init)
fig.set_size_inches(12,7)

# for i in range(1000):
#   print i
#   mc()
for p in range(1000):
  print p
  animate(p)
  savefig("anim/mc100-%4.2f-%03i.pdf" %(ff, p))
show()