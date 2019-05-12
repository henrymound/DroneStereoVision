# Topics Covered During the Process
1. Stereo Vision
	- Sending byte commands to the Tellos to put them into station mode (including SSID and password of local station).
	- Using Python to send commands to both drones at the same time. This was a different approach to the one I took over the summer, during which I connected each drone to a different antenna. With this new approach, however, I can control more than two Tellos at the same time - giving the swarm capability a lot more power.
	- Unfortunatly, in station mode, the Tellos do not accept the 'streamon' command that allows video data to be transfered.
	- Tried creating multiple virtual machines and using each VM to connect to a Tello and recieve video data that way. This proved impossible.
2. COLMAP 
	- Using drone photos from the Mavic around BiHall, I was able to generate a point cloud that was representative of the building. This was really encouraging. However, the algorithm to generate the results was too sophisticated for me to change/work with within this independent study process.
	- ![COLMAP Results](images/colmap.png)
3. monoVO
	- Next, with the guidance of Professor Grant, I started diving into visual odometry and its applications. Modifying the repository on GitHub, I started feeding in flight images from the Tello. Part of this process involved camera calibration. 


# Essay Structure
1. Introduction
2. Process/Work Done
3. Reflection
	1. Further work
	2. Difficulties/roadblocks