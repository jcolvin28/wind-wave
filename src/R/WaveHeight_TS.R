###########################################
# Script to calculate wave height given   #
# pixel location of wave crest and trough #
# from distortion-corrected timestack.    #
#                                         #
#      Jeff Colvin, August 2017           #
#         Updated July 2020               #
###########################################

# An example wavedata.txt file is included in the sample data directory
# This is a text file with the pixel locations of wave crests and troughs
# from a timestack image. Research is underway to automate this process.

filename <- 'wavedata.txt'
wavedata <- read.csv(file=filename, header=TRUE, sep=",")

crest <- wavedata$crest     # y-pixel locations of crest
trough <- wavedata$trough   # y-pixel locations of trough

cam.height <- 98            # camera height in cm above SWL
op.axis <- 534              # y-pixel of optical axis (from cam calibration file)

k <- 1/3                    # amount of wave below SWL (see article)

swl <- trough - k * (trough - crest)

wave.height <- cam.height/(1-k)*((swl-op.axis)-(crest-op.axis))/(swl-op.axis)
print(wave.height)
mean.wave <- mean(wave.height)
print(mean.wave)
