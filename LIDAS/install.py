#!/usr/bin/env python

# Makes the necessary directories and redistributes the scripts

import os

if os.path.isdir('../BIAS')==False:
	os.system('mkdir ../BIAS')
if os.path.isdir('../FLAT')==False:
	os.system('mkdir ../FLAT')
if os.path.isfile('../bpm_trimmed.pl')==False:
	os.system('cp bpm_trimmed.pl ../')

for i in range(1,10):
	if (os.path.isdir('../object' + str(i))==False):
		os.system('mkdir ../object' + str(i))
		os.system('mkdir ../object' + str(i) + '/SCIENCE')
		os.system('mkdir ../object' + str(i) + '/lightcurve')
		
		os.system('cp readme.txt ../')
		os.system('cp redwfcbias.cl ../BIAS')
		os.system('cp redwfcflat.cl ../FLAT')
		os.system('cp redwfc.cl ../object' + str(i) + '/SCIENCE')
		os.system('cp int.pars aligner.py coord_finder*.py plotter.py \
		 lightcurve*.py ../object' + str(i) + '/lightcurve')
		break
