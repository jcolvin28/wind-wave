###########################################
#  Wave Analysis from Raw Wave Gauge Data #
#       Jeff Colvin, September 2017       #
#          Updated July 2020              #
###########################################

# timestack label
tslabel <- 'hm1'

# load timeseries data
filename <- paste0(tslabel, '.txt')
wavedata <- read.csv(file=filename, header=TRUE, sep=",")

# water level vector
water <- wavedata$value

# time vector
freq <- 32
timelength <- length(water)/freq
dt = 1/freq
t <- seq(dt,timelength,by=dt)

# wave vector
meanlevel <- mean(water)
wave <- water-meanlevel

plot(t, wave)

# initialize zero-down crossing
s <- 0
p <- vector()

for (i in 2:(length(wave)-1)){
  if (wave[i-1]>0 & wave[i+1]<0){
    s <- s+1
    p[s] <- i
  }
}

# remove duplicate values
s <- 0
m <- length(p)
for (i in 1:(m-1)){
  if (p[i+1]-p[i]==1){
    p[i] <- 0
    s <- s+1
  }
}
p <- p[order(p)]
p <- p[!p %in% c(0)]

# calculate wave periods
m <- length(p)
T <- vector()
for (i in 1:(m-1)){
  T[i] <- dt * (p[i+1]-p[i])
}

# calculating wave heights
H <- vector()
for (i in 1:(m-1)){
  a <- vector()
  a <- wave[p[i]:p[i+1]]
  mx <- max(a)
  mn <- min(a)
  H[i] <- mx-mn
}

# final wave by wave analysis calculations
Hc <- mean(H)
Tm <- mean(T)

h <- H[order(H)]
tt <- T[order(T)]          # sig period calc
n <- round((m-1)/3)
h <- h[(2*(n+1)):(m-1)]
tt <- tt[(2*(n+1)):(m-1)]  # sig period calc
Hsig <- mean(h)
Tsig <- mean(tt)           # sig period calc

HRMS <- sqrt(mean(H^2))

# variance calculations
m0 <- var(wave)
Hm0 <- 4*sqrt(m0)
Hrms <- sqrt(8*m0)
Hs <- 3.8*sqrt(m0)

# Print results
print('Wave by wave analysis:')
print(paste0('Mean Period, Tm = ', Tm))
print(paste0('Significant Period, Tsig = ', Tsig))
print('- - -')
#print(paste0('Wave Height, Hc = ', Hc))
print(paste0('Wave Height, Hsig = ', Hsig))
print(paste0('Wave Height, Hrms = ', HRMS))
print('- - -')
print('By variance:')
print(paste0('Wave Height, Hm0 = ', Hm0))
print(paste0('Wave Height, Hs = ', Hs))
print(paste0('Wave Height, Hrms = ', Hrms))
