LiDAS - Lightcurve derivation for asteroids

1. Unpack LiDAS.tar in your working directory.

2. ./install.py. This creates the necessary folders.

3. Put your biases, flats and raw images in their respective folders.
 
4. Reduce the data. 

	Do the following:
	
	cd BIAS 
	files r1* > biaslist
	task redwfcbias = redwfcbias.cl
	List of files: biaslist
	
	cd FLAT
	files r1* > flatlist
	task redwfcflat = redwfcflat.cl
	List of files: flatlist
	
	cd SCIENCE
	files r1* > astlist
	task redwfc = redwfc.cl
	List of files: astlist
	
	Only CCD4 was reduced. Find the reduced data in SCIENCE: red_*.

5. Align the images

	cd SCIENCE
	Find a suitable star (5-40,000 counts) visible in the first and last
	images, away from bad columns. This star will be used for alignment.
	cd lightcurve
	./aligner.py
	The initial image will be displayed in ds9, with the IRAF imexam cursor
	available. 
	Press 'a' with the cursor on top of your star. 
	Press 'q' when done. The next frame will be displayed.
	Repeat until the last frame. 
	Wait for alignment.
	Find the aligned images in SCIENCE: al_red*
	
6. Find the coordinates of the asteroid

	There are two scripts for this: coord_finder_auto.py and
	coord_finder_man.py. The first one assumes a linear path of the asteroid
	and the second one lets you find the asteroid on each individual frame,
	similarly to the aligning script.
	It's recommended that you use the auto script first and if you get
	strange results or errors after running lightcurve.py, run the manual
	one. 
	
7. Measure the seeing and sky sigma in the first image

8. Get the lightcurve

	./lightcurve1.x.py
