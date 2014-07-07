#! /usr/bin/env python

import os,numpy
import matplotlib.pyplot as plt

data = numpy.loadtxt('final.dat')
plt.title('143409')
plt.xlabel('MJD')
plt.ylabel('Relative magnitude')
plt.ylim(-0.9,0.7)
plt.xlim(56815.80,56816.10)
plt.plot(data[:,0],data[:,1],linestyle='',marker='o')



fig = plt.gcf()
plt.draw()
fig.savefig('143409.png')
