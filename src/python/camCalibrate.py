# -*- coding: utf-8 -*-

##############################
#      camCalibrate.py       #
# Camera calibration program #
#       Jeff Colvin          #
#        July 2020           #
##############################

##########################################################################
# Python 3.7 script using openCV 4.3 to calibrate a video camera         #
# and save the camera matrix and distortion parameters to a calibration  #
# file that can be used to undistort images and video from the camera.   #
# Calibration video needs to be in same directory as the python script.  #
##########################################################################

import numpy as np
import cv2
import sys

##############
# User Input #
##############

# name of calibration video file
vidfile = input("Name of calibration video file: ")
#vidfile = "GOPR0023.mp4"

# number of calibration images to capture from video
calimages = int(input("Number of calibration images to capture from video: "))
#calimages = 15

# dimensions of checkerboard (inner corners)
# (edit these numbers if not using the example checkerboard image)
bwidth = 9
bheight = 6

#########################################
# Capture calibration images from video #
# Press <space> to capture              #
# Press <q> to quit capture and exit    #
#########################################

video = cv2.VideoCapture(vidfile)
if video.isOpened():
    frames = video.get(7)
    current = 80
    collected = 0
    video.set(1, current)
    
    while current < frames:
        #video.set(1, current)
        success, img = video.read()
        cv2.imshow('Video Window', img)
        k = cv2.waitKey(1) & 0xFF
        current += 1
        if collected == calimages:
            break
        if k == 32:
            collected += 1
            cv2.imwrite('calimage' + str(collected) + '.png', img)
            print(str(collected) + ' calibration images collected')
        if k == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
else:
    print('... Video load error.')
    sys.exit()

#####################################################################
# Read in calibration images, detect calibration pattern, calculate #
# camera matrix and distortion coefficients and write to file       #
#####################################################################

#########################
# Initialize parameters #
#########################

boarddim = (bwidth, bheight)
points = np.zeros((np.prod(boarddim), 3), np.float32)
points[:,:2] = np.indices(boarddim).T.reshape(-1, 2)

obpoints = []
impoints = []
h, w = 0, 0

######################################################################
# Read in calibration images, locate calibration pattern, and create #
# image point and object point matrices needed for cam calibration   #
######################################################################

term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.001)

for i in range(1, calimages + 1):
    print('... Loading calimage' + str(i))
    img = cv2.imread('calimage' + str(i) + '.png', 0)
    if img is None:
        print('... Failed to load calimage' + str(i) + '.png')
        continue
    h, w = img.shape[:2]
    found, corners = cv2.findChessboardCorners(img, boarddim)
    if found:
        
        cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), term)
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.drawChessboardCorners(vis, boarddim, corners, found)        
        cv2.imwrite('calimage' + str(i) + '_corners.png', vis)
        cv2.imshow('Corner locations', vis)
        cv2.waitKey(0)
    if not found:
        print('... calibration pattern not found')
        continue
    impoints.append(corners.reshape(-1, 2))
    obpoints.append(points)

cv2.destroyAllWindows()

##############################################################################    
# Calculate camera matrix, distortion coefficients, & RMS reprojection error #
##############################################################################

rms, cammatrix, distcoefs, rvecs, tvecs = cv2.calibrateCamera(obpoints, impoints, (w, h), None, None)
print('RMS: ', rms)
print('Camera matrix: ', cammatrix)
print('Distortion Coefficients: ', distcoefs)

################################################################
# Save camera matrix and distortion coefficients as numpy file #
################################################################

print('... Saving camera calibration file.')
np.savez('camcalib', distcoefs=distcoefs, cammatrix=cammatrix)
print('... Finished calibration.')

####################################################
# Use camera matrix and distortion coefficients to #
# undistort the calibration images                 #
####################################################

for i in range(1, calimages + 1):
    img = cv2.imread('calimage' + str(i) + '.png', 1)
    undist = cv2.undistort(img, cammatrix, distcoefs, None)
    cv2.imwrite('calimage' + str(i) + '_undist.png', undist)
    cv2.imshow('Undistorted Image', undist)
    cv2.waitKey(0)
    
cv2.destroyAllWindows()

########################################################################
# These are needed on some systems to insure proper closing of windows #
########################################################################
#cv2.waitKey(1)
#cv2.waitKey(1)
#cv2.waitKey(1)
#cv2.waitKey(1)