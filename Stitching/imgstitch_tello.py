import sys
import traceback
import threading
import tellopy
from tello import Tello
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 5
DELAY = 3
tello = Tello()	
mission_complete = False
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


def plannedRoute():
	tello.send("takeoff", DELAY)
	# Take a series of NUM_IMAGES images, each 50 apart
	for i in range(0, NUM_IMAGES):
		tello.send("right 50",DELAY)
		if tello.hasFrame:
			cv2.imwrite('flight/'+str(i)+'.png', tello.frame) # Save the image to a subdirectory
			images.append(tello.frame) # Append the image and stitch
			(status, stitched) = stitcher.stitch(images)
	tello.send("land", DELAY)

	# Notify the program that the flight mission is complete
	mission_complete = True


if __name__ == '__main__':
	# Turn on the video
	tello.startVideo()

	# Start the Tello mission
	route_thread = threading.Thread(target=plannedRoute)
	route_thread.start()

	# Turn off the video stream
	tello.stopVideo()

	
	for x in range(0, NUM_IMAGES):
		
		print("status:",status)
		#if status==0: # Live stiching
		cv2.imshow('Stitched Image', stitched)
		cv2.waitKey(0)
	#(status, stitched) = stitcher.stitch(images)
	cv2.destroyAllWindows()
