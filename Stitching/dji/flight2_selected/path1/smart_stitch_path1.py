import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils
import math

IMAGE_PATH_PREFIX = "DJI_0"
IMAGE_PATH_SUFFIX = ".JPG"

IMAGE_SCALE_FACTOR = .2
# STITCH_HEIGHT_MIN_RATIO: A scale factor applied to input image height to determine 
# 	the minimum stitched height for a 'valid' batch result.
STITCH_HEIGHT_MIN_RATIO = 2 

NUM_IMAGES = 484-436
START_NUM = 436
BATCH_BOUND = 10 # The maximum images allowed in a batch
BATCH_MIN = 4 # The minimum number of photos to fill a batch

#images = [None] * BATCH_BOUND # Empty array bound by the maximum batch size
images = [] # Images is a list of dynamic size
batch_images = [None] * int(NUM_IMAGES/BATCH_MIN) # Empty array with size bound by batch min
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


# Will try and stitch the final product together as a combination of 'smart' sub stitched images
if __name__ == '__main__':
	# Display info
	print("ATTEMPTING TO SMART STITCH A TOTAL OF " + str(NUM_IMAGES) + " INPUT IMAGES.")
	print("Each substitched image will be composed of " + str(BATCH_MIN) + "-" + str(BATCH_BOUND) +
			 " images.\nThe substitched images will be at least " + str(STITCH_HEIGHT_MIN_RATIO) + 
			 "x the height of each input.\nEach input image will be scaled to " +str(IMAGE_SCALE_FACTOR) + 
			 "x its original size.\n\n")
	# Determine the maximum number of batches we would want to make based on the starting
	#	number of images
	batch_counter = 0 # We start having completed 0 batches
	images_in_batch = 0 # We start off with no images in our current batch
	for i in range(0, NUM_IMAGES + 1, 1): 
		imgPath = IMAGE_PATH_PREFIX+str(i + START_NUM)+IMAGE_PATH_SUFFIX
		img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
		# Scale to IMAGE_SCALE_FACTOR of original
		imgToAppend = cv2.resize(img,None,fx=IMAGE_SCALE_FACTOR,fy=IMAGE_SCALE_FACTOR) 
		images.append(imgToAppend)
		images_in_batch = len(images) 
		#images_in_batch += 1 # Increment the images in array counter
		print("Appended image #"+str(images_in_batch) + " (" + 
				imgPath + ") to batch: " + str(batch_counter))
		if images_in_batch >= BATCH_MIN: # If minimum number reached, try and stitch
			print("STITCHING BATCH " + str(batch_counter) + " W/ " + str(images_in_batch) + " IMAGES.")
			(status, stitched) = stitcher.stitch(images)
			if status == 0: # If stitching is successful
				# Write the resulting image with corresponding batch number
				cv2.imwrite('BATCH'+str(batch_counter)+'.JPG',stitched)
				# Find input image shape
				inputHeight, inputWidth, inputChannels = imgToAppend.shape
				#print("Input height " + str(inputHeight))
				# Find stitched image shape
				stitchedHeight, stitchedWidth, stitchedChannels = stitched.shape
				#print("Stitched height " + str(stitchedHeight))
				if images_in_batch == BATCH_MIN:
					# Save this stitch if its the first attemp or previous attempt failed
					batch_images[batch_counter] = stitched # Update array if empty
				if batch_images[batch_counter] is not None: # If there is a previous image
					prevHeight, prevWidth, prevChannels = batch_images[batch_counter].shape
					if stitchedHeight > prevHeight:
				 		batch_images[batch_counter] = stitched
					else:
						print("Stitched image is shrank with the newest addition!")
				else:
					print("Previous stitch resulted in an error. No comparison can be made.")

				# Check ratio criteria
				if(stitchedHeight/inputHeight >= STITCH_HEIGHT_MIN_RATIO) or (i >= NUM_IMAGES): # If the stitch is valid
					if (i >= NUM_IMAGES):
						print("Stitched image does not meet criteria, but will be used. Last image of input.")
					print("UPDATING COMPOSITE IN ARRAY LOCATION " + str(batch_counter))
					images = [] # clear the input array
					batch_counter += 1 # move to the next batch
				else:
					print("Stitch not valid because scale factor is " + str(stitchedHeight/inputHeight))
			else:
				print("ERROR STITCHING BATCH " + str(batch_counter) + " W/ " + str(images_in_batch) + " IMAGES.")

		if images_in_batch > BATCH_BOUND: # Check if more are allowed to be added.
			# If the upper bound has been reached. Abandon batch and move on
			print("MAX IMAGES FOR BATCH INPUT (" + str(BATCH_BOUND)
			 	+ "). ABANDONING BATCH " + str(batch_counter))
			images = [] # clear the input array
			batch_counter += 1 # move to the next batch


	print("STITCHING " + str(batch_counter - 1) + " BATCH STITCHES")
	 # Only use the first 'batch_counter' images
	(status, stitched) = stitcher.stitch(batch_images[0:batch_counter - 1])
	#cv2.imshow('Stitched Image', stitched)
	if status == 0:
		cv2.imwrite('FINAL_BATCH_COMPOSITE.JPG',stitched)
	else:
		print("ERROR ON FINAL STITCH")
	cv2.waitKey(0)
	cv2.destroyAllWindows()
