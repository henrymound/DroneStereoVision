import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils
import time

NUM_IMAGES = 10
DELAY = 0
DISTANCE = 50
images = [] # To store images taken
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS) # A new stitcher object
StillRecording = True

def addImages():
	for imageNum in range(0, NUM_IMAGES):
		print("Adding image: '"+'flight/'+str(imageNum)+'.png'+"'")
		images.append(cv2.imread('flight/'+str(imageNum)+'.png')) # Add image to array
		time.sleep(1)
	StillRecording = False
		

if __name__ == '__main__':
	#stitcherThread = threading.Thread(target=addImages)
	#stitcherThread.start()
	for imageNum in range(0, NUM_IMAGES):
		print("Adding image: '"+'flight/'+str(imageNum)+'.png'+"'")
		images.append(cv2.imread('flight/'+str(imageNum)+'.png')) # Add image to array
		(status, stitched) = stitcher.stitch(images) # Update stitcher
		# If there are more than 2 images in the stitcher, start live updating
		if len(images) > 2:
			print("Status: " + str(status))
			cv2.imshow('Stitched Image', stitched)
		time.sleep(1)
	
	cv2.waitKey(0)

