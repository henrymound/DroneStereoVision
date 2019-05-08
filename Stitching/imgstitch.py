import numpy as np
import imutils
import cv2

images = []

stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
for x in range(39):
	img = cv2.imread('line1/'+str(x)+'.png')
	print("Added image " + str(x))
	images.append(img)

(status, stitched) = stitcher.stitch(images)
print("status:",status)

if status==0:
	cv2.waitKey(0)
	cv2.imwrite('line1/result_pano.png', stitched)
    #cv2.imshow('Stitched Image', stitched)
    #cv2.destroyAllWindows()
