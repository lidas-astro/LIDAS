
procedure redwfcflat(flatl)

# Image Reduction of FLAT of INT-WFC images bin 1x1
# Author: Ovidiu Vaduvescu, updated Nov 2011, La Palma
# Note: flatlist file must not have .fit and must not have last empty line


string  flatl   { prompt = "List of flat images to reduce" }

struct *listl
# listl to be used only local


begin

string im
      
time


# Load packages...

noao
imred
ccdred

# Delete former files...

if (access("flatlist4")) delete("flatlist?")
delete("r*.fits")
delete("flatCCD?.fits")

# Slice the 4 CCDs...
listl = flatl

while (fscan(listl, im) != EOF) 
{
  imcopy(im//"[4]", im//"CCD4")
  print(im//"CCD4", >> "flatlist4")

}

  ccdproc.overscan = yes
  ccdproc.trim = yes
  ccdproc.zerocor = yes
  ccdproc.flatcor = no
  ccdproc.biassec = "[10:2150,4105:4190]"
  ccdproc.trimsec = "[54:2101,1:4096]"
  ccdproc.readaxi = "column"
  ccdproc.darkcor=no
  ccdproc.fixpix = yes
  ccdproc.fixfile = "../bpm_trimmed"
  flatcombine.gain = "GAIN"
  flatcombine.rdnoise = "READNOIS"

  ccdproc.zero = "../BIAS/biasCCD4"
  flatcombine(input="@flatlist4", output="flatCCD4", combine="median", ccdtype="", process = yes)

time

end

