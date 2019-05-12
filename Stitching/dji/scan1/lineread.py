import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 418-394
START_IMAGE = 394
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':
	# Read a series of NUM_IMAGES images
	for i in range(0, NUM_IMAGES):
		img = cv2.imread("DJI_0"+str(i+START_IMAGE)+".JPG",cv2.IMREAD_COLOR)
		images.append(img) # Append the image and stitch
		print("Added image " + str(i + START_IMAGE))
	print("STITCHING")
	(status, stitched) = stitcher.stitch(images)
	if status == 0: # If image is valid
		cv2.imwrite('RESULTS.JPG', stitched) # Save image
		#cv2.imshow('Stitched Image', stitched)
		cv2.waitKey(1)
	cv2.imshow('Stitched Image', stitched)
	cv2.waitKey(1)
	#(status, stitched) = stitcher.stitch(images)
	#cv2.destroyAllWindows()
