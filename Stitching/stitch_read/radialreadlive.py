import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 21
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)


if __name__ == '__main__':
	# Read a series of NUM_IMAGES images
	for i in range(0, NUM_IMAGES):
		img = cv2.imread("../radial_flights/radial1/"+str(i)+".png",cv2.IMREAD_COLOR)
		images.append(img) # Append the image and stitch
		(status, stitched) = stitcher.stitch(images)
		print("Added image " + str(i) + " with status: " + str(status))
		if status == 0: # If image is valid
			cv2.imshow('Stitched Image', stitched)
			#cv2.imwrite("../radial_flights/radial2/results/stitched"+str(i)+".png", stitched)
			cv2.waitKey(1)
		
	cv2.waitKey(0)
	#(status, stitched) = stitcher.stitch(images)
	cv2.destroyAllWindows()
