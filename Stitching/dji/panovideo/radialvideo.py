import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 40
STARTNUM = 1
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)


if __name__ == '__main__':
	# Read a series of NUM_IMAGES images
	for i in range(0, NUM_IMAGES, 2):
		img = cv2.imread("frames/"+str(i+STARTNUM).zfill(4)+".jpg",cv2.IMREAD_COLOR)
		images.append(img) # Append the image and stitch
		print("Added image " + str(i+STARTNUM))
	print("STITCHING")
	(status, stitched) = stitcher.stitch(images)
	if status == 0: # If image is valid
		#cv2.imshow('Stitched Image', stitched)
		cv2.imwrite("RESULTS.JPG", stitched)
		cv2.waitKey(1)
		
	cv2.waitKey(0)
	#(status, stitched) = stitcher.stitch(images)
	cv2.destroyAllWindows()
