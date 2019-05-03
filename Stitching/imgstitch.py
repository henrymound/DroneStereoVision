import numpy as np
import imutils
import cv2

images = []

img = cv2.imread('tello1.JPG')
images.append(img)
img = cv2.imread('tello2.JPG')
images.append(img)
img = cv2.imread('tello3.JPG')
images.append(img)
img = cv2.imread('tello4.JPG')
images.append(img)
img = cv2.imread('tello5.JPG')
images.append(img)
img = cv2.imread('tello6.JPG')
images.append(img)
img = cv2.imread('tello7.JPG')
images.append(img)

stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
(status, stitched) = stitcher.stitch(images)

print("status:",status)

if status==0:
    cv2.imshow('Stitched Image', stitched)
    cv2.waitKey(0)

cv2.destroyAllWindows()
