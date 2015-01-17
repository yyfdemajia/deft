#!/usr/bin/python2

ww = 1.3
ff = 0.3
N = 20

methods = ["nw","bubble_suppression","robustly_optimistic","gaussian","wang_landau","walker_optimization"]

inputs = ["../data/periodic-ww%04.2f-ff%04.2f-N%i-%s-%s.dat"
          % (ww, ff, N, method.replace(' ',''), postfix)
          for postfix in ['g', 'E', 'lnw', 's']
          for method in methods] + ['styles.pyc']

print '| cd .. && python2 figs/plot-dos.py %f %f %d "%s"' % (ww, ff, N, methods)
for o in ["periodic-ww%02.0f-ff%02.0f-N%i-dos.pdf" % (ww*100, ff*100, N),
          "periodic-ww%02.0f-ff%02.0f-N%i-weights.pdf" % (ww*100, ff*100, N)]:
    print '>', o
for i in inputs:
    print '<', i
print

print '| cd .. && python2 figs/plot-histograms.py %f %f %d "%s"' % (ww, ff, N, methods)
for o in ["periodic-ww%02.0f-ff%02.0f-N%i-E.pdf" % (ww*100, ff*100, N)]:
    print '>', o
for i in inputs:
    print '<', i
print

print '| cd .. && python2 figs/plot-uhc.py %f %f %d "%s"' % (ww, ff, N, methods)
for o in ["periodic-ww%02.0f-ff%02.0f-N%i-u.pdf" % (ww*100, ff*100, N),
          "periodic-ww%02.0f-ff%02.0f-N%i-hc.pdf" % (ww*100, ff*100, N)]:
    print '>', o
for i in inputs:
    print '<', i
print

print '| cd .. && python2 figs/plot-samples.py %f %f %d "%s"' % (ww, ff, N, methods)
for o in ["periodic-ww%02.0f-ff%02.0f-N%i-rt.pdf" % (ww*100, ff*100, N),
          "periodic-ww%02.0f-ff%02.0f-N%i-rt-rate.pdf" % (ww*100, ff*100, N)]:
    print '>', o
for i in inputs:
    print '<', i
print
