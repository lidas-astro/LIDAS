#! /usr/bin/env python

import os,numpy
import matplotlib.pyplot as plt

cwd = os.getcwd()
os.chdir(os.getenv("HOME"))
from pyraf import iraf
os.chdir(cwd)

path = cwd[0:cwd.index('lightcurve')]
if os.path.isfile('imagelist') == True:
	os.remove('imagelist')

iraf.files(path + 'SCIENCE/al*',Stdout = 'imagelist')

f = open('imagelist')
images = f.readlines()
f.close()
indx = images[0][::-1].index('/') # find where the image name starts 
image0 = images[0][-indx:-1]
imageF = images[-1][-indx:-1]
print image0,imageF

iraf.disp(path + 'SCIENCE/' + imageF,2)
iraf.disp(path + 'SCIENCE/' + image0,1)
print 'Press \'a\' on asteroid in Frame 1, change to Frame 2, press \'a\' on asteroid. q to exit.'
os.system('rm rawcoords')
iraf.imexam(Stdout = 'rawcoords')
rawcoords = numpy.loadtxt('rawcoords')
x0 = rawcoords[0][0] 
y0 = rawcoords[0][1] 
xF = rawcoords[2][0] 
yF = rawcoords[2][1] 

os.system('rm MJD')
iraf.hedit('@imagelist','MJD-OBS','.',Stdout = 'MJD')

MJDfile = open('MJD')
MJDlines = MJDfile.readlines()
MJD = []
for i in MJDlines:
	MJD.append(i.split()[len(i.split())-1])

print float(MJD[0]),x0,y0
print MJD[-1],xF,yF
os.system('rm astrcoords')
f = open('astrcoords','a')
for i in range(0,len(MJD)):
	x = x0 + (float(MJD[i])-float(MJD[0]))*(xF-x0)/(float(MJD[-1])-float(MJD[0]))
	y = y0 + (float(MJD[i])-float(MJD[0]))*(yF-y0)/(float(MJD[-1])-float(MJD[0]))
	f.write('%.1f %.1f\n' % (x,y))
f.close()
