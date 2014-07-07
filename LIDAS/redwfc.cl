
procedure redwfc(astl)

# Image Reduction of NEAs of INT-WFC images bin 1x1
# Author: Ovidiu Vaduvescu, updated Nov 2011, La Palma
# Note: astlist file must not have .fit and must not have last empty line


string  astl   { prompt = "List of sky images to reduce" }

struct *listl
struct *listl1

# listl to be used only local


begin

string im, str1, str2, UT, junk

time

# Load packages...

noao
imred
ccdred

# Delete former files...

delete("r*.fits")
delete("tmpUT*")


# Slice the 4 CCDs...
listl = astl

while (fscan(listl, im) != EOF) 
{

  imcopy(im//"[4]", im//"CCD4")

  ccdproc.overscan = yes
  ccdproc.trim = yes
  ccdproc.biassec = "[10:2150,4105:4190]"
  ccdproc.trimsec = "[54:2101,1:4096]"
  ccdproc.readaxi = "column"
  ccdproc.darkcor = no
  ccdproc.zerocor = yes
  ccdproc.flatcor = yes
  ccdproc.fixpix = yes
  ccdproc.fixfile = "../../bpm_trimmed"

  ccdproc(images=im//"CCD4", output="red_"//im, ccdtype="object",
  zero="../../BIAS/biasCCD4", flat="../../FLAT/flatCCD4")

}

time

end
