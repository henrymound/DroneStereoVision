import sys
import traceback
import threading
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np
import imutils
import math


LAST_INDEX = 530
FIRST_INDEX = 485

IMAGE_PATH_PREFIX = "DJI_0"
IMAGE_PATH_SUFFIX = ".JPG"

NO_SHRINK = True # When true, doesn't allow batches to shrink in size as more images are added
MATCH_RATIOS = False # When true, program aims to create substitches of similar size
CHECK_PROGRESS = False # When true, smart stitch will check each time a batch stitch
#	is assigned to make sure it works with the finished batches

IMAGE_SCALE_FACTOR = 1
# STITCH_HEIGHT_MIN_RATIO: A scale factor applied to input image height to determine 
# 	the minimum stitched height for a 'valid' batch result.
STITCH_HEIGHT_MIN_RATIO = 2

NUM_IMAGES = LAST_INDEX-FIRST_INDEX
START_NUM = FIRST_INDEX
BATCH_BOUND = 20 # The maximum images allowed in a batch
BATCH_MIN = 3 # The minimum number of photos to fill a batch

#images = [None] * BATCH_BOUND # Empty array bound by the maximum batch size
images = [] # Images is a list of dynamic size
batch_images = [None] * int(NUM_IMAGES/BATCH_MIN) # Empty array with size bound by batch min
stitch_in_progress = None # Stores image of current progress 
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)


# Will try and stitch the final product together as a combination of 'smart' sub stitched images
if __name__ == '__main__':
	# Display info
	print("\n\nATTEMPTING TO SMART STITCH A TOTAL OF " + str(NUM_IMAGES) + " INPUT IMAGES.")
	print("Each substitched image will be composed of " + str(BATCH_MIN) + "-" + str(BATCH_BOUND) +
			 " images.\nThe substitched images will be at least " + str(STITCH_HEIGHT_MIN_RATIO) + 
			 "x the height of each input.\nEach input image will be scaled to " +str(IMAGE_SCALE_FACTOR) + 
			 "x its original size.\nNo shrinking batches: " + str(NO_SHRINK) + "\n" +
			 "Trying to match batch sizes: " + str(MATCH_RATIOS) + "\n" +
			 "Checking whole stitch progress: " + str(CHECK_PROGRESS) +
			 "\n\n")
	# Determine the maximum number of batches we would want to make based on the starting
	#	number of images
	batch_counter = 0 # We start having completed 0 batches
	images_in_batch = 0 # We start off with no images in our current batch
	average_batch_height = 0
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
			Stitch_Shrank = False # Tracks if this batch attempt is smaller than last
			print("STITCHING BATCH " + str(batch_counter) + " W/ " + str(images_in_batch) + " IMAGES.")
			(status, stitched) = stitcher.stitch(images)
			if status == 0: # If stitching is successful
				# Find input image shape
				inputHeight, inputWidth, inputChannels = imgToAppend.shape
				#print("Input height " + str(inputHeight))
				# Find stitched image shape
				stitchedHeight, stitchedWidth, stitchedChannels = stitched.shape
				#print("Stitched height " + str(stitchedHeight))
				if images_in_batch == BATCH_MIN and batch_counter == 0:
					# If first stitch, set stitch_in_progress
					stitch_in_progress = stitched
				if images_in_batch == BATCH_MIN or batch_images[batch_counter] is None:
					print("Saving first attempt of batch " + str(batch_counter))
					# Save this stitch if its the first attemp or previous attempt failed
					batch_images[batch_counter] = stitched # Update array
					# Write the resulting image with corresponding batch number
					cv2.imwrite('BATCH'+str(batch_counter)+'.JPG',stitched)
				if batch_images[batch_counter] is not None: # If there is a previous image
					prevHeight, prevWidth, prevChannels = batch_images[batch_counter].shape
					if stitchedHeight > prevHeight and images_in_batch > BATCH_MIN:
						# If this stitch is larger than previous (and not the first), update
						if batch_counter >= 1 and CHECK_PROGRESS: # If not first batch and set to check
							print("Checking result will work with overall stitch")
							toStitch = []
							toStitch.append(stitch_in_progress)
							toStitch.append(img)
							(status1, stitched1) = stitcher.stitch(toStitch)
							if status1 == 0: # If success
								print("Success!")
								cv2.imwrite('progress.JPG',stitched1)
							else:
								print("Fail!")
						print("Updating Batch Array Index " + str(batch_counter))
						batch_images[batch_counter] = stitched
						# Write the resulting image with corresponding batch number
						cv2.imwrite('BATCH'+str(batch_counter)+'.JPG',stitched)
					elif images_in_batch > BATCH_MIN: # Record that current stitch is smaller than previous
						#print("Stitched image shrank with the newest addition!")
						Stitch_Shrank = True
				elif images_in_batch > BATCH_MIN:
					print("All previous stitches resulted in an error. No comparison can be made.")


				# Check ratio criteria
				if(
					(stitchedHeight/inputHeight >= STITCH_HEIGHT_MIN_RATIO) or # Ratio requirement met
					(i >= NUM_IMAGES) or # Last image
					(Stitch_Shrank and NO_SHRINK) or # Image shrank and not allowed
					(images_in_batch >= BATCH_BOUND) or # Reached max batch size
					(MATCH_RATIOS and stitchedHeight > average_batch_height and average_batch_height > 0) # Trying to match ratios
					): # If the stitch is valid for any reason
					if (i >= NUM_IMAGES):
						print("Last image of input.")
					if (Stitch_Shrank and NO_SHRINK): # If stitch shrank is true and not allowed
						print("Shrinking is not allowed.")
					if (stitchedHeight/inputHeight >= STITCH_HEIGHT_MIN_RATIO):
						print("Ratio requirement met.")
					if (images_in_batch >= BATCH_BOUND):
						print("Batch limit met.")
					if (MATCH_RATIOS and stitchedHeight > average_batch_height and average_batch_height > 0):
						print("Matching ratios. Current height is " + str(stitchedHeight) + " and " +
							"average is " + str(average_batch_height) + "\n")
					# Update average batch height
					average_batch_height *= batch_counter # Restore sum of composite heights
					if average_batch_height == 0: # Average is only entry
						average_batch_height = stitchedHeight
					else: # Add height of this batch and recalculate
						average_batch_height += stitchedHeight
						average_batch_height /= batch_counter

					images = [] # clear the input array
					batch_counter += 1 # move to the next batch
					print("ENDING BATCH " + str(batch_counter - 1))
				#else:
					#print("Stitch not valid because scale factor is " + str(stitchedHeight/inputHeight))
			else:
				print("ERROR STITCHING BATCH " + str(batch_counter) + " W/ " + str(images_in_batch) + " IMAGES.")


	# Get valid batch results
	final_images = []
	counter = 0
	for image in batch_images:
		if image is not None: # If valid image
			final_images.append(image)
			if len(final_images) >= 2: # Attempt in-progress stitch
				(progstatus, progstitched) = stitcher.stitch(final_images)
				if progstatus == 0: # If progress array succesfully stitched
					print("Saving Progress " + str(counter))
					cv2.imwrite('Progress'+str(counter)+'.JPG',progstitched)
					counter+=1

	print("STITCHING " + str(len(final_images)) + " VALID SUB-STITCHED IMAGES")
	

	 # Only use the first 'batch_counter' images
	(status, stitched) = stitcher.stitch(final_images)
	#cv2.imshow('Stitched Image', stitched)
	if status == 0:
		cv2.imwrite('FINAL_BATCH_COMPOSITE.JPG',stitched)
	else:
		print("ERROR ON FINAL STITCH")
	cv2.waitKey(0)
	cv2.destroyAllWindows()
