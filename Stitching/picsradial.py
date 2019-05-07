import sys
import traceback
import threading
import tellopy
from tello import Tello
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 18
DELAY = 0
tello = Tello()	
images = []
stitcher = cv2.Stitcher_create(cv.Stitcher_PANORAMA)


if __name__ == '__main__':
	# Turn on the video
	tello.startVideo()

	# Start the Tello mission
	tello.send("takeoff", DELAY)
	tello.send("up 500")
	# Take a series of NUM_IMAGES images, each 50 apart
	for i in range(0, NUM_IMAGES):
		tello.send("cw " + str(360/NUM_IMAGES), DELAY)
		if tello.hasFrame:
			cv2.imwrite('radial/'+str(i)+'.png', tello.frame) # Save the image to a subdirectory
			images.append(tello.frame) # Append the image and stitch
			(status, stitched) = stitcher.stitch(images)
	tello.send("land", DELAY)

	# Turn off the video stream
	tello.stopVideo()

	
	cv2.imshow('Stitched Image', stitched)
	cv2.waitKey(0)
	#(status, stitched) = stitcher.stitch(images)
	cv2.destroyAllWindows()
