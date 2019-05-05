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
DELAY = 1

def saveImage(drone, imageName):
	if drone.hasFrame:
		cv2.imwrite('flight/'+str(imageName)+'.png', drone.frame) # Save the image to a subdirectory

def plannedRoute():
	global tello, mission_complete
	tello.send("takeoff", DELAY)
	# Take a series of 10 images, each 100 apart
	for i in range(0, NUM_IMAGES):
		tello.send("right 50",DELAY)
		saveImage(tello, i)
	tello.send("land", DELAY)

	# Notify the program that the flight mission is complete
	mission_complete = True


def main():
	# Create a new instance of the Tello.
	tello = Tello()
	mission_complete = False

	# Turn on the video
	tello.startVideo()

	# Start the Tello mission
	route_thread = threading.Thread(target=plannedRoute)
	route_thread.start()

	# Turn off the video stream
	tello.stopVideo()

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
	images = []
	stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
	for x in range(0, NUM_IMAGES):
		img = cv2.imread('flight/'+str(x)+'.png')
		images.append(img)
		(status, stitched) = stitcher.stitch(images)
		print("status:",status)
		if status==0: # Live stiching
		    cv2.imshow('Stitched Image', stitched)
		    cv2.waitKey(0)
	#(status, stitched) = stitcher.stitch(images)
	cv2.destroyAllWindows()
