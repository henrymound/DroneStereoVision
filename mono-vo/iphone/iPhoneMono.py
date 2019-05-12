import numpy as np 
import cv2

from visual_odometry import PinholeCamera, VisualOdometry


cam = PinholeCamera(960.0, 540.0, 911.53, 909.47, 482.79, 345.40)
vo = VisualOdometry(cam)

traj = np.zeros((600,600,3), dtype=np.uint8)

for img_id in range(1, 181):
	img = cv2.imread('frames/'+str(img_id).zfill(4)+'.jpg', 0)
	#print('flight6/output-'+str(img_id).zfill(4)+'.png')
	# Resize image
	#img = cv2.resize(img,(960,720))
	#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	vo.update(img, img_id)

	cur_t = vo.cur_t
	if(img_id > 2):
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

	cv2.imshow('Road facing camera', img)
	cv2.imshow('Trajectory', traj)
	cv2.waitKey(1)

cv2.imwrite('map.png', traj)
