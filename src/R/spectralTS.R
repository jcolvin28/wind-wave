###############################################
# Generate spectral plot from timestack image #
#         Jeff Colvin, August 2017            #
#             updated July 2020               #
###############################################

library(EBImage)
library(signal)

## tslabel specified the location and timestack number for a
## particular field experiment, i.e., hm1 was specified hurricane
## Matthew, timestack #1. The naming convention for timestack images
## is <tslabel>timestack_<frames per second>fps_<length of time>s.png
## hm1timestack_60fps_64s.png is included in the sample files.
tslabel <- 'hm1'

## rownum specifies the row number of the timestack image from which a pixel
## intensity time series will be made. This row ideally includes the waves
## closest to the camera (lower in the image) and before any breaking occurs.
rownum <- 655

a <- 10
b <- 3840

filename = paste0(tslabel, 'timestack_60fps_64s.png')

# Read in and display the original timestack image
img = readImage(filename)
display(img, method='raster')

# Convert to grayscale and display image
img = channel(img, "gray")
display(img, method='raster')

# Perform Gaussian blur and display image
# This acts like a low pass filter removing high frequency pixel noise
# sigma is standard deviation of the filter (sigma=5 give blur radius of ~30 pixels)
height = ncol(img)
img = gblur(img, sigma = 5)
display(img, method='raster')

# The timestacks in this research were all 64s at 60fps
timelength = 64
freq = 60
dt = 1/freq
n <- timelength/dt
df <- 1/timelength

t <- seq(dt,timelength,by=dt)
f <- 1:length(t)/timelength

intensityRaw = img[1:3840, rownum]
intensityNorm = normalize(intensityRaw)

intensity <- as.array(intensityNorm)

# Perform high-pass butterworth filter to remove low frequency signals
bf <- butter(2, 0.3/(freq/2), type="high")
intensityf <- filter(bf, intensity)

# Perform FFT and display pixel intensity time series plot
# and spectral plot showing wave frequencies
Y <- fft(intensityf[a:b])
mag <- sqrt(Re(Y)^2+Im(Y)^2)*2/n

peakfreq <- paste0('Timestack: Filtered Peak frequency = ',f[which.max(mag[2:256])])

intensityff <- (intensityf[a:b] - min(intensityf[a:b]))/(max(intensityf[a:b])-min(intensityf[a:b]))
plot(t[a:b],intensityff,type='l', lwd=2, xlim=c(0,timelength), main=paste0('Time Series Plot: Row = ',rownum), xlab='time (s)', ylab='normalized intensity')
plot(f[1:192],mag[1:192],type='l', lwd=2, xaxp  = c(0, 3, 24), main=paste0(peakfreq, ' ; Row = ', rownum), xlab='frequency (Hz)', ylab='strength')
