
procedure redwfcbias(biasl)

# Image Reduction of BIAS of INT-WFC images bin 1x1
# Author: Ovidiu Vaduvescu, updated Nov 2011, La Palma
# Note: biaslist file must not have .fit and must not have last empty line


string  biasl   { prompt = "List of bias images to reduce" }

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

if (access("biaslist4")) delete("biaslist?")
delete("*.fits")


# Slice the 4 CCDs...
listl = biasl

while (fscan(listl, im) != EOF) 
{
  imcopy(im//"[4]", im//"CCD4")
  print(im//"CCD4", >> "biaslist4")
}

# Set up specific WFC parameters...

  zerocombine.gain = "GAIN"
  zerocombine.rdnoise = "READNOIS"
  ccdproc.overscan = yes
  ccdproc.trim = yes
  ccdproc.biassec = "BIASSEC"
  ccdproc.trimsec = "TRIMSEC"
  ccdproc.readaxi = "column"

# Combine biases for the 4 chips...

  zerocombine(input="@biaslist4", output="biasCCD4", ccdtype="zero", combine="median")

time

end

