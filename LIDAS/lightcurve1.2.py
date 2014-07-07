#! /usr/bin/env python

import os,numpy
import matplotlib.pyplot as plt

cwd = os.getcwd()
os.chdir(os.getenv("HOME"))
from pyraf import iraf
os.chdir(cwd)

iraf.noao(_doprint=0)
iraf.digiphot(_doprint=0)
iraf.daophot(_doprint=0)

# Intro screen
print '\n Lightcurve finder \n Version: 1.2\n'

path = cwd[0:cwd.index('lightcurve')]
if os.path.isfile('imagelist') == True:
	os.remove('imagelist')

iraf.files(path + 'SCIENCE/al*',Stdout = 'imagelist')

f = open('imagelist')
images = f.readlines()
f.close()
indx = images[0][::-1].index('/') # find where the image name starts 
image0 = images[0][-indx:-1]

# Loading parameter file and the FWHM
iraf.unlearn('daophot')
iraf.setimpars('int','yes','no') 
FWHM = raw_input('What is the stellar FWHM in pixels?\n')
skysigma = raw_input('What is the sky sigma in the first image?\n')
iraf.datapars.scale = 1/float(FWHM)
iraf.datapars.sigma = float(skysigma)

# Finding calibration stars
os.system('rm *.coo.*')
iraf.daofind('../SCIENCE/' + image0,'default',verify='no',verbose='no')
os.system('rm *.mag.*')
iraf.phot('../SCIENCE/' + image0,'default','default',verify='no',verbose='no')
try:
	os.remove('calibcoords')
except: True
iraf.txdump(image0 + '.mag.1','xcenter,ycenter',\
"cerror='NoError' && perror='NoError' && serror='NoError' && merr<0.005 && mag>0",Stdout = 'calibcoords')

coordarray = []
f = open('calibcoords')
calibcoords = f.readlines()
f.close()
for i in calibcoords:
	coordarray.append(i)

# Calculate mean calibration star magnitude for each imagine
os.system('rm *.mag.*')
iraf.phot('@imagelist','calibcoords','default',verify='no',verbose='no')

os.system('rm magfiles')
iraf.files(path + 'lightcurve/al*mag.1',Stdout = 'magfiles')
magarray = []
f = open('magfiles')
magfiles = f.readlines()
 
f.close()
for i in magfiles:
	magarray.append(iraf.txdump(i[0:-1],'mag','yes', Stdout=1))
	# magarray - array with magnitudes of calibration stars
	# magarray[x][y]; x-the image index,y-the star index

for j in range(0,len(magfiles)):
# j is the image number
	while 'INDEF' in magarray[j]:
		num = magarray[j].index('INDEF')
		# index is the star number in the j image
		for k in range(0,len(magfiles)):
			del magarray[k][num]
		del coordarray[num]
check = []
for i in range(0,len(magfiles)):
	check.append(len(magarray[i]))
check = set(check)

magarray = numpy.array(magarray).astype(numpy.float)
meanmag = []
# meanmag is an array with the mean magnitudes of the calibration stars. 
# The index is the image number, starting at 0
for i in range(0,len(magfiles)):
	meanmag.append(numpy.mean(magarray[i]))

# Clipping of calibration stars
# Select stars that have a standard deviation in magnitude less than twice the sigma 
# of the variation of all stars. Have at least 25 calibration stars

N = 0
Ni = -1
itera = 0
while N!=Ni and len(magarray[0])>=25:
	
	norm_magarray = []
	for i in range(0,len(magarray[0])):
		norm_magarray.append(list(magarray[:,i]-numpy.mean(magarray[:,i])))	
		#norm_array_trans[x][y] - x: star number, y: image number

	norm_magarray = numpy.transpose(norm_magarray)
	norm_magarray_trans = numpy.transpose(norm_magarray)
	std_list = []
	for i in range(0,len(norm_magarray_trans[:,0])):
		std_list.append(numpy.std(norm_magarray_trans[i]))
	STD_std = numpy.std(std_list)
	MEAN_std = numpy.mean(std_list)
	Ni = N
	for item in list(std_list):
		if item > MEAN_std + 1.3*STD_std:
			index = std_list.index(item)
			std_list.pop(index)
			magarray = numpy.delete(magarray,index,1)
			coordarray.pop(index)
			N += 1
	meanmag = []
	for i in range(0,len(magfiles)):
		meanmag.append(numpy.mean(magarray[i]))
	itera += 1

print len(magarray[0]),'calibration stars left after',itera,'iterations'

# Write the coordinates if the calibration stars to file, display and check them
f = open('calibcoords-final','w')
for i in coordarray:
	f.write('%s' % i)
f.close()

iraf.display('../SCIENCE/' + image0,1)
iraf.tvmark(1,'calibcoords-final',col=204, mark='circle', radii=12, number='yes')

# Errors from the calibration stars
norm_magarray = []
for i in range(0,len(magarray[0])):
	norm_magarray.append(list(magarray[:,i]-numpy.mean(magarray[:,i])))
cerr = []
norm_magarray = numpy.transpose(norm_magarray)
for i in range(0,len(magfiles)):
	cerr.append(numpy.std(norm_magarray[i,:]))

# Asteroid photometry
astercoords = numpy.loadtxt('astrcoords')
os.system('rm *.mag.2')
for i in range(0,len(magfiles)):
	f = open('tmpcoords','w')
	f.write('%.1f %.1f\n' % (astercoords[i][0],astercoords[i][1]))
	f.close()
	iraf.phot(images[i][0:-1],'tmpcoords','default',verify='no',verbose='no')

os.system('rm tmpcoords')
os.system('rm ast_magfiles')
os.system('rm astrmags')
iraf.files(path + 'lightcurve/al*mag.2',Stdout = 'ast_magfiles')
iraf.txdump('@ast_magfiles','xcenter,ycenter,mag,merr','yes',Stdout = 'astrmags')

os.system('rm MJD')
iraf.hedit('@imagelist','MJD-OBS','.',Stdout = 'MJD')

astdata = numpy.loadtxt('astrmags')
MJDfile = open('MJD')
MJDlines = MJDfile.readlines()
MJD = []
for i in MJDlines:
	MJD.append(i.split()[len(i.split())-1])

# Write to file
f = open('final.dat','w')
for i in range(0,len(images)):
	f.write('%s %.4f %.4f\n' % (MJD[i],astdata[i,2]-meanmag[i]-numpy.mean(astdata[:,2]-meanmag),\
numpy.sqrt(numpy.square(astdata[i,3])+numpy.square(cerr[i]))))
f.close()

# Plotting
plt.subplot(2,2,1)
plt.title('Asteroid - Relative Magnitude')
key_press = raw_input('Error bars? [y/n]')
if key_press == 'y':
	plt.errorbar(MJD,astdata[:,2]-meanmag-numpy.mean(astdata[:,2]-meanmag),\
yerr=numpy.sqrt(numpy.square(astdata[:,3])+numpy.square(cerr)))
elif key_press == 'n':
	plt.plot(MJD,astdata[:,2]-meanmag-numpy.mean(astdata[:,2]-meanmag))
else:
	print 'Sorry, what?'
ymin = plt.ylim()[0]
ymax = plt.ylim()[1]

plt.subplot(2,2,2)
plt.title('Calibration stars - Mean Instrumental Magnitude')
plt.plot(MJD,meanmag)
plt.ylim(numpy.mean(meanmag)-(-ymin+ymax)/2-0.05,numpy.mean(meanmag)+(-ymin+ymax)/2+0.05)

plt.subplot(2,2,3)
norm_magarray = numpy.array(norm_magarray)
for i in range(0,len(magarray[0])):
	plt.plot(MJD,magarray[:,i]-meanmag-numpy.mean(magarray[:,i]-meanmag))
plt.title('Calibration stars - Relative Magnitude')
plt.xlabel('MJD')

plt.subplot(2,2,4)
plt.title('Asteroid - Instrumental Magnitude')
plt.plot(MJD,astdata[:,2])
plt.ylim(numpy.mean(astdata[:,2])-(-ymin+ymax)/2-0.05,numpy.mean(astdata[:,2])+(-ymin+ymax)/2+0.05)

fig = plt.gcf()
plt.draw()
plt.show()
fig.savefig('output.png')



