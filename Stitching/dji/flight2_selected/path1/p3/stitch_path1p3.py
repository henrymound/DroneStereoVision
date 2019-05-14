import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 484-469
START_NUM = 469
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':

	for i in range(0, NUM_IMAGES + 1, 1): # Only add every other image
		imgPath = "DJI_0"+str(i + START_NUM)+".JPG"
		img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
		imgToAppend = cv2.resize(img,None,fx=0.1,fy=0.1) # Downscale to 30% of original
		images.append(img) 
		print("Appended: " + imgPath)
	
	(status, stitched) = stitcher.stitch(images)
	#cv2.imshow('Stitched Image', stitched)
	cv2.imwrite('FULL.JPG',stitched)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
