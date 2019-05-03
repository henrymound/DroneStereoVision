import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import numpy as np
import imutils
import cv2

def saveImage(drone, imageName):
	if drone.hasFrame:
    	# Save the image to a subdirectory
    	cv2.imwrite('flight/'+str(imageName)+'.png', drone.frame)

def plannedRoute():
	global tello, mission_complete
	tello.send("takeoff", 3)
	# Take a series of 10 images, each 100 apart
	for i in range(0, 10):
		tello.send("right 50",3)
		saveImage(tello, i)
	tello.send("land", 3)

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

	img = cv2.imread('newspaper1.jpg')
	images.append(img)
	img = cv2.imread('newspaper2.jpg')
	images.append(img)
	img = cv2.imread('newspaper3.jpg')
	images.append(img)
	img = cv2.imread('newspaper4.jpg')
	images.append(img)

	stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
	(status, stitched) = stitcher.stitch(images)

	print("status:",status)

	if status==0:
	    cv2.imshow('Stitched Image', stitched)
	    cv2.waitKey(0)

	cv2.destroyAllWindows()
