import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils

NUM_IMAGES = 484-436
START_NUM = 436
BATCH_SIZE = 3
images = []
batch_images = []
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


if __name__ == '__main__':
	batch_counter = 0
	batch_index = 1
	for i in range(0, NUM_IMAGES + 1, 1): # Only add every other image
		imgPath = "DJI_0"+str(i + START_NUM)+".JPG"
		img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
		imgToAppend = cv2.resize(img,None,fx=0.1,fy=0.1) # Downscale to 30% of original
		images.append(img) 
		print("Appended: " + imgPath)
		batch_counter+=1
		if batch_counter == BATCH_SIZE:
			print("STITCHING BATCH " + str(batch_index))
			(status, stitched) = stitcher.stitch(images)
			if status == 0: # If stitching is successful
				cv2.imwrite('BATCH'+str(batch_index)+'.JPG',stitched)
				batch_index += 1
				batch_images.append(stitched)
			else:
				print("ERROR STITCHING " + str(batch_index-1))
			images = []
			batch_counter = 0
	print("STITCHING SUBRESULTS")
	(status, stitched) = stitcher.stitch(batch_images)
	#cv2.imshow('Stitched Image', stitched)
	if status == 0:
		cv2.imwrite('FINAL_BATCH_COMPOSITE.JPG',stitched)
	else:
		print("ERROR ON FINAL STITCH")
	cv2.waitKey(0)
	cv2.destroyAllWindows()
