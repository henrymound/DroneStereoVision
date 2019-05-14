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
	progress_index = 1
	for i in range(9, 0, -1): # Fill Array
		imgPath = "path"+str(i)+".JPG"
		img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
		images.append(img) 
		print("Appended: " + imgPath)

	currently_stitched = []
	if len(images) > 0:
		currently_stitched.append(images[0])
		images.remove(images[0])

	while len(images) > 0:
		for img in images:
			currently_stitched.append(img)
			(status, stitched) = stitcher.stitch(currently_stitched)
			if status == 0:
				cv2.imwrite('progress'+str(progress_index)+'.JPG',stitched)
				progress_index+=1
				images.remove(img)

	(status, stitched) = stitcher.stitch(images)
	if status == 0:
		cv2.imwrite('final.JPG',stitched)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
