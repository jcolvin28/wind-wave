# -*- coding: utf-8 -*-

#########################################
#          createTimestack.py           #
#  Create timestack at given frequency  #
#             Jeff Colvin               #
#              July 2020                #
#########################################

##########################################################################
# Python 3.7 script using openCV 4.3 to capture video frames at a        #
# given frequency, undistort the frames, and extract the given column to #
# create a timestack image. The camera calibration file created with     #
# camCalibrate.py (camcalib.npz) and the source video must be located in #
# the current working directory.                                         #
##########################################################################

import numpy as np
import cv2

##############
# User Input #
##############

# name of video file to undistort
vidfile = input("Name of source video: ")

# column to strip out of images to create timestack
col = int(input("Enter column of video frames to be stripped: "))

# framestep of timestack
print("\nThe framestep determines the frequency of the timestack that is generated")
print("(with a 60fps video: 1 = 60fps, 2 = 30fps, 3 = 20fps, 4 = 15fps, ...)")
framestep = int(input("Enter framestep for this timestack: "))

# time duration of timestack (in seconds)
duration = int(input("Enter the duration (in seconds) of the timestack: "))

# duration from start of video where timestack creation should begin (in seconds)
startTimestack = int(input("Enter number of seconds into video for timestack creation to begin: "))

camcalibfile = input("Name of camera calibration file: ")

###########################################################
# Load camera calibration parameters from numpy .npz file #
###########################################################

camcalib = np.load(camcalibfile)
distcoefs = camcalib['distcoefs']
cammatrix = camcalib['cammatrix']
camcalib.close()

########################################################################
# Read in video file, pull frames at proper rate, undistort the image, #
# strip column of pixels, and build timestack a column at a time.      #
########################################################################

video = cv2.VideoCapture(vidfile)

if video.isOpened():
    height = int(video.get(4))                           # get video height    
    fps = int(video.get(5)) + 1                          # get frames per second
    freq = fps / framestep                               # frequency of timestack (based on framestep)
    width = int(duration * freq)                         # width of timestack image
    timestack = np.zeros((height, width, 3), np.uint8)   # create blank timestack image    
    current = (startTimestack * fps) + 1                 # starting frame for timestack
    lastframe = (duration * fps) + current - 1           # last frame to be used for timestack
    count = 1

    while current < lastframe:
#        print(current)
        video.set(1, current)                            # set frame of video to read
        success, img = video.read()
        undist = cv2.undistort(img, cammatrix, distcoefs, None)
        pixelcol = undist[:,col:col+1]
        pixelcol = img[:,col:col+1]
        timestack[:, count:count+1] = pixelcol
        cv2.imshow('Timestack', timestack)
        cv2.waitKey(1)
        current += framestep
        count += 1
    cv2.imwrite('pb2timestack_' + str(freq) + 'fps_' + str(duration) + 's.png', timestack)
    video.release()
    cv2.destroyAllWindows()

