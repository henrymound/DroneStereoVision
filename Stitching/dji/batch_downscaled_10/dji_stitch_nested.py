import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 5
START_NUM = 16
#BATCH_SIZE = 30
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':
	print("Stitching " + str(NUM_IMAGES) + "batch images")
	for i in range(0, NUM_IMAGES):
		imgPath = str(i + START_NUM)+".JPG"
		img = cv2.imread(imgPath, cv2.IMREAD_COLOR) 
		#imgToAppend = cv2.resize(img,None,fx=0.3,fy=0.3) # Downscale to 30%
		images.append(img) 
		print("Appended: " + imgPath)
	print("STITCING ALL IN ARRAY")	
	(status, stitched) = stitcher.stitch(images)
	cv2.imwrite('result.JPG',stitched)
	cv2.waitKey(0)
	
	#cv2.imshow('Stitched Image', stitched)
	
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
