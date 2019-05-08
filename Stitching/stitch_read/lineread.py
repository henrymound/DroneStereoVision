import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 25
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':
	# Read a series of NUM_IMAGES images
	for i in range(0, NUM_IMAGES):
		img = cv2.imread("../upline/"+str(i)+".png",cv2.IMREAD_COLOR)
		images.append(img) # Append the image and stitch
		(status, stitched) = stitcher.stitch(images)
		print("Added image " + str(i) + " with status: " + str(status))
		if status == 0: # If image is valid
			cv2.imwrite('../upline/results/stitched'+str(i)+'.png', stitched) # Save image
			#cv2.imshow('Stitched Image', stitched)
			cv2.waitKey(1)
	cv2.imshow('Stitched Image', stitched)
	cv2.waitKey(1)
	#(status, stitched) = stitcher.stitch(images)
	#cv2.destroyAllWindows()
