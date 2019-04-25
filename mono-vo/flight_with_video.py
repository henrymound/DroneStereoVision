from tello import Tello
import threading

import numpy as np
import cv2

def plannedRoute():
	"""
	This function executes the planned route. Particularly, in this
	case, the drone will fly in a 100cm square. This program executes as 
	a thread so that video processing can continue in the main program
	"""
	global tello, mission_complete

	tello.send("takeoff", 3)

	for ii in range(36):
		tello.send("forward 30",3)
		tello.send("cw 10",3)

	tello.send("land", 3)

	# Notify the program that the flight mission is complete
	mission_complete = True

# Create a new instance of the Tello.
tello = Tello()
mission_complete = False

# Turn on the video
tello.startVideo()

# Start the Tello mission
route_thread = threading.Thread(target=plannedRoute)
route_thread.start()

# Display the video frames until a user presses
# the 'q' key or the mission is complete
count = 0
while not mission_complete:
  if tello.hasFrame:
    
    # Display the image with the bounding boxes
    cv2.imshow('frame',tello.frame)

    # Save the image to a subdirectory
    cv2.imwrite('flight4/tello'+str(count)+'.png',tello.frame)

    # inserts a small millisecond delay to render
    # the video frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    count = count + 1

# Turn off the video stream
tello.stopVideo()

cv2.destroyAllWindows()