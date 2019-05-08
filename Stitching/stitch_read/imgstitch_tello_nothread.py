import sys
import traceback
import threading
import tellopy
from tello import Tello
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 10
DELAY = 0
DISTANCE = 50

if __name__ == '__main__':
	tello = Tello()	# Create a new Tello object
	images = [] # To store images taken
	stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS) # A new stitcher object
	tello.startVideo() # Turn on the video
	tello.send("takeoff", DELAY) # Drone takeoff
	tello.send("up 100", DELAY)
	# Take a series of NUM_IMAGES images, each DISTANCE mm apart
	for i in range(0, NUM_IMAGES):
		tello.send("right " + str(DISTANCE), DELAY)
		if tello.hasFrame:
			cv2.imwrite('flight/'+str(i)+'.png', tello.frame) # Save the image to a subdirectory
			images.append(tello.frame) # Append the image and stitch live
			if i > 2:
				(status, stitched) = stitcher.stitch(images)
				print("Status: " + str(status))
				cv2.imshow('Stitched Image', stitched)
		else:
			print("Tello has no frame to stitch!")
	tello.send("land", DELAY)
	tello.stopVideo()
	cv2.waitKey(0)

