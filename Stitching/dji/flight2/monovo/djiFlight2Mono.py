import numpy as np 
import cv2

from visual_odometry import PinholeCamera, VisualOdometry

# Focal length = (width/2)/tan(fov/2)
# For mavic (fov 78.8): (4000/2)/tan(78.8/2) == (4000/2)/0.82140888325 == ~2434.841
# ORIGINAL CAM
#cam = PinholeCamera(4000.0, 3000.0, 2434.841, 2434.841, 2000.0, 1500.0)
# SCALED CAM TO 30%
cam = PinholeCamera(1200.0, 1000.0, 730.4523, 730.4523, 600.0, 500.0)
# SCALED CAM TO 10%
#cam = PinholeCamera(400.0, 300.0, 243.4841, 243.4841, 200.0, 150.0)

vo = VisualOdometry(cam)

traj = np.zeros((600,600,3), dtype=np.uint8)

for img_id in range(438, 910):
	img = cv2.imread('../DJI_0'+str(img_id)+'.JPG', 0)
	#print('flight6/output-'+str(img_id).zfill(4)+'.png')
	# Resize image
	img = cv2.resize(img,(1200,1000))
	#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	vo.update(img, img_id)

	cur_t = vo.cur_t
	if(img_id > 439): # Starting at the second input image
		x, y, z = cur_t[0], cur_t[1], cur_t[2]
	else:
		x, y, z = 0., 0., 0.
	draw_x, draw_y = int(x)+290, int(z)+450
	true_x, true_y = int(vo.trueX)+290, int(vo.trueZ)+450

	cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)
	cv2.circle(traj, (true_x,true_y), 1, (0,0,255), 2)
	cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
	text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
	cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)

	#cv2.imshow('Road facing camera', img)
	cv2.imshow('Trajectory', traj)
	cv2.waitKey(1)

cv2.imwrite('map.png', traj)
