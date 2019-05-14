import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':

	
	img1 = cv2.imread("p1/FULL.JPG", cv2.IMREAD_COLOR)
	img2 = cv2.imread("p2/FULL.JPG", cv2.IMREAD_COLOR)
	img3 = cv2.imread("p3/FULL.JPG", cv2.IMREAD_COLOR)
	images.append(img1) 
	print("Appended part 1")
	images.append(img2) 
	print("Appended part 2")
	images.append(img3) 
	print("Appended part 3")
	print("STITCHING")
	
	(status, stitched) = stitcher.stitch(images)
	#cv2.imshow('Stitched Image', stitched)
	cv2.imwrite('P1P2P3.JPG',stitched)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
