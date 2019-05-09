import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 25#432-367
START_NUM = 367
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':

	for i in range(0, NUM_IMAGES):
		imgPath = "flight1/DJI_0"+str(i + START_NUM)+".JPG"
		imgToAppend = cv2.imread(imgPath, cv2.IMREAD_COLOR) 
		images.append(imgToAppend) 
		print("Appended: " + imgPath)
	
	(status, stitched) = stitcher.stitch(images)
	#cv2.imshow('Stitched Image', stitched)
	cv2.imwrite('result.JPG',stitched)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
