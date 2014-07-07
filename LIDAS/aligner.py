#! /usr/bin/env python

import os,numpy

cwd = os.getcwd()
os.chdir(os.getenv("HOME"))
from pyraf import iraf
os.chdir(cwd)

path = cwd[0:cwd.index('lightcurve')]
if os.path.isfile('imagelist') == True:
	os.remove('imagelist')

iraf.files(path + 'SCIENCE/red_*',Stdout = 'imagelist')

f = open('imagelist')
images = f.readlines()
f.close()

print 'Press \'a\' on the same star in al frames. Press \'q\' to load the next frame.'
os.system('rm shifts')
f = open('shifts','a')

for i in range(0,len(images)):

	iraf.disp(images[i][0:-1],1)
	os.system('rm tmpcoords')
	iraf.imexam(Stdout = 'tmpcoords')
	g = numpy.loadtxt('tmpcoords')
	if i == 0:
		x0 = g[0][0]
		y0 = g[0][1]
	f.write('%d %d\n' % (round(x0-g[0][0],0),round(y0-g[0][1],0)))
if i != len(images)-1:
	iraf.disp(images[-1][0:-1],1)
	os.system('rm tmpcoords')
	iraf.imexam(Stdout = 'tmpcoords')
	g = numpy.loadtxt('tmpcoords')
	f.write('%d %d\n' % (round(x0-g[0][0],0),round(y0-g[0][1],0)))
f.close()
os.system('rm tmpcoords')

print '\n Aligning... \n'

# Shift the images
os.system('rm aligned_list')
f = open('aligned_list','a')
for i in range(0,len(images)):
	indx = images[i][::-1].index('/') 
	image = images[i][-indx:-1]
	f.write('al_%s\n' % image)
f.close()
os.system('rm al_red*')
iraf.imshift('@imagelist','@aligned_list',shifts='shifts')
os.system('mv al_red_* ../SCIENCE/')




