#! /usr/bin/env python

import os,numpy

cwd = os.getcwd()
os.chdir(os.getenv("HOME"))
from pyraf import iraf
os.chdir(cwd)

f = open('aligned_list')
images = f.readlines()
f.close()

print 'Press \'a\' on the asteroid in all frames. Press \'q\' to load the next frame.'
os.system('rm astrcoords')
f = open('astrcoords','a')

for i in range(0,len(images)):

	iraf.disp('../SCIENCE/' + images[i][0:-1],1)
	os.system('rm tmpcoords')
	iraf.imexam(Stdout = 'tmpcoords')
	g = numpy.loadtxt('tmpcoords')
	f.write('%d %d\n' % (g[0][0],g[0][1]))
#if i != len(images)-1:
#	iraf.disp(images[-1][0:-1],1)
#	os.system('rm tmpcoords')
#	iraf.imexam(Stdout = 'tmpcoords')
#	g = numpy.loadtxt('tmpcoords')
#	f.write('%d %d\n' % (round(x0-g[0][0],0),round(y0-g[0][1],0)))
f.close()
os.system('rm tmpcoords')

