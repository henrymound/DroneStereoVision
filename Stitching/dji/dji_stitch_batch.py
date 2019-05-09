import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 910-433
START_NUM = 433
BATCH_SIZE = 10
images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':
	c = 0 # Count the batch num
	print("Stitching " + str(NUM_IMAGES) + " with a batch size of " + str(BATCH_SIZE))
	for i in range(0, NUM_IMAGES):
		imgPath = "flight2/DJI_0"+str(i + START_NUM)+".JPG"
		img = cv2.imread(imgPath, cv2.IMREAD_COLOR) 
		imgToAppend = cv2.resize(img,None,fx=0.3,fy=0.3) # Downscale to 30%
		images.append(imgToAppend) 
		print("Appended: " + imgPath)
		if(len(images) == BATCH_SIZE):
			print("Batch " + str(c) + " Complete: Saving in batch/"+str(c)+".JPG")
			(status, stitched) = stitcher.stitch(images)
			cv2.imwrite('batch_downscaled/'+str(c)+'.JPG',stitched)
			cv2.waitKey(0)
			images = []
			c+=1
	#cv2.imshow('Stitched Image', stitched)
	
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
