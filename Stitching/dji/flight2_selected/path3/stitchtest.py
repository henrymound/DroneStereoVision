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
	counter = 0
	img0 = cv2.imread("BATCH0.JPG", cv2.IMREAD_COLOR)
	img1 = cv2.imread("BATCH1.JPG", cv2.IMREAD_COLOR)
	img2 = cv2.imread("BATCH2.JPG", cv2.IMREAD_COLOR)
	img3 = cv2.imread("BATCH3.JPG", cv2.IMREAD_COLOR)
	img4 = cv2.imread("BATCH4.JPG", cv2.IMREAD_COLOR)
	img5 = cv2.imread("BATCH5.JPG", cv2.IMREAD_COLOR)
	images.append(img0)
	images.append(img1)
	images.append(img2)
	images.append(img3)
	(status, stitched) = stitcher.stitch(images)
	if status == 0: # If stitching is successful
		cv2.imwrite('TEST.JPG',stitched)

	else:
		print("ERROR STITCHING")
		
