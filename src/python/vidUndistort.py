# -*- coding: utf-8 -*-

########################################
#           vidUndistort.py            #
#  Remove lens distortion from video   #
#            Jeff Colvin               #
#             July 2020                #
########################################

#########################################################################
# Python 3.7 script using openCV 4.3 to undistort video taken with a    #
# camera that has been previously calibrated. The camera calibration    #
# file and the video to be undistorted must be in the same directory    #
# as this script.                                                       #
#########################################################################

import numpy as np
import cv2

########################################
# User Input and Initialize parameters #
########################################

# name of video file to undistort
vidfile = input("Name of video file to undistort: ")
#vidfile = "GOPR0025.MP4"

# Load camera calibration parameters from numpy .npz file
camcalibfile = input("Name of camera calibration file: ")
camcalib = np.load(camcalibfile)
#camcalib = np.load('camcalib.npz')
distcoefs = camcalib['distcoefs']
cammatrix = camcalib['cammatrix']
camcalib.close()

#######################################
# Read in video file, undistort, and  #
# write out new undistorted video     #
#######################################

video = cv2.VideoCapture(vidfile)

if video.isOpened():
    width = video.get(3)     # get width of frames
    height = video.get(4)    # get height of frames
    fps = video.get(5)       # get frames per second
    frames = video.get(7)    # get number of frames
    size = (int(width), int(height))
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    current = 80             # some gopro videos have a glitch within the first second
    video.set(1, current)    # this starts video capture at frame 80
                             # to remove, delete video.set(1, current) line and
                             # change current = 0
    
    videoUnd = cv2.VideoWriter(str(vidfile[:-4]) + '_undist.avi', fourcc, fps, size)

    while current < frames:
        success, img = video.read()
        current = video.get(1)
        undist = cv2.undistort(img, cammatrix, distcoefs, None)
        videoUnd.write(undist)
    video.release()
    videoUnd.release()
