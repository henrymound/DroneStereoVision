# DroneStereoVision
A repository of the work for my independent study project: implementing stereo vision with two DJI Tello EDU drones.

## Connecting to the two Tello EDUs

Router Configuration IP: 192.168.0.1

Tello 1: 192.168.0.101
Tello 2: 192.168.0.102

## Getting Video From a Single Tello
Open Tello3 smaple program
Send ```command```
Send ```streamon```

open terminal
```ffplay -probesize 32 -i udp://@:11111 -framerate 30```

---

### Sources

Some of the included code has been forked from the following repositories:
- https://github.com/dbaldwin/Tello-Python
- https://github.com/dbaldwin/droneblocks-telloedu-python

I also used information from the official Tello SDK
- https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf
