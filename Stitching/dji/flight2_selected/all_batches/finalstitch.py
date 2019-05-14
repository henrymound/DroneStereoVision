import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 20
START_NUM = 0
SCALE = 1
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':

	for i in range(0, NUM_IMAGES, 1): 
		imgPath = str(i + START_NUM)+".JPG"
		img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
		imgToAppend = cv2.resize(img,None,fx=SCALE,fy=SCALE)
		images.append(imgToAppend) 
		print("Appended: " + imgPath)
	print("STITCHING")
	(status, stitched) = stitcher.stitch(images)
	#cv2.imshow('Stitched Image', stitched)
	cv2.imwrite('result.JPG',stitched)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
