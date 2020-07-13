###############################################
# Generate spectral plot from timestack image #
#        Jeff Colvin, July 2020               #
###############################################

library(EBImage)
library(signal)

tslabel <- 'hm1'
rownum <- 655

a <- 10
b <- 3840

filename = paste0(tslabel, 'timestack_60fps_64s.png')

img = readImage(filename)
display(img, method='raster')

img = channel(img, "gray")
display(img, method='raster')

height = ncol(img)
img = gblur(img, sigma = 5)
display(img, method='raster')

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

bf <- butter(2, 0.3/(freq/2), type="high")
intensityf <- filter(bf, intensity)

# filtered
Y <- fft(intensityf[a:b])
mag <- sqrt(Re(Y)^2+Im(Y)^2)*2/n

peakfreq <- paste0('Timestack: Filtered Peak frequency = ',f[which.max(mag[2:256])])

intensityff <- (intensityf[a:b] - min(intensityf[a:b]))/(max(intensityf[a:b])-min(intensityf[a:b]))
plot(t[a:b],intensityff,type='l', lwd=2, xlim=c(0,timelength), main=paste0('Time Series Plot: Row = ',rownum), xlab='time (s)', ylab='normalized intensity')
plot(f[1:192],mag[1:192],type='l', lwd=2, xaxp  = c(0, 3, 24), main=paste0(peakfreq, ' ; Row = ', rownum), xlab='frequency (Hz)', ylab='strength')
