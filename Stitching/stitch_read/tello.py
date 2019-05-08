# This class has been created to control the DJI Tello SDK 2.0
# TO create this class, material was taken from DroneBlocks and other 
# Stack Overflow forums. This class allows for real-time video processing
# of video from the drone. It has been tested with optical flow, Canny edge
# detection, and face detection using a Haar Cascade Classifier.

# Import the necessary modules
import socket
import threading
import numpy as np
import cv2
import time

class Tello:

    def __init__(self):

        # Variable that will contain the response from Tello
        self.response = None

        # Max time in seconds without a response after sending
        # a message before declaring an error in sendingg
        self.MSG_WAIT_TIME = 5

        # Boolean value that toggles whether when the response timer is done receiving
        self.timerIsComplete = False

        # IP and port of Tello
        self.tello_address = ('192.168.10.1', 8889)

        # IP and port of sending computer
        self.local_address = ('', 9000)

        # Create a UDP connection where we'll send commands
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the local address and port
        self.sock.bind(self.local_address)

        # Create and start a listening thread that runs in the background
        # This utilizes our receive function and will continuously monitor for incoming messages
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()


        # Variables for rendering video
        self.cap = None
        self.frame = None
        self.hasFrame = False
        self.video_thread_on = False

        # Places Tello drone in SDK mode
        self.send("command", 1)
        

    def startVideo(self):
        """
        This method initializes the video stream for the Tello.
        It begins by sending the 'streamon' command. Next, it
        opens a video capture stream using OpenCV. Video will
        be send on port 11111. 

        Next, the video thread is started. This thread continues
        to read from the capture source and store data into
        frames.
        """
        # Turns on the video stream
        self.send("streamon")
        
        # Open the video stream
        try:
            self.cap = cv2.VideoCapture("udp://localhost:11111")
        except Exception as e:
            print(e)

        # Creates a thread for the video. Thread is set as a daemon thread
        # This allows the program to end even if this thread is running.
        self.receive_video_thread = threading.Thread(target=self.receiveVideo)
        self.receive_video_thread.daemon = True
        
        self.video_thread_on = True
        self.receive_video_thread.start()

    def stopVideo(self):
        """
        Cancels the video thread and tells the Tello to
        turn off the video. The videocapture source is 
        also closed.
        """

        self.video_thread_on = False
        self.send("streamoff")
        self.cap.release()

    def receiveVideo(self):
        """
        Listens for video streaming (raw h264) from the Tello.
        Runs as a thread, sets self.frame to the most recent 
        frame Tello captured.
        """

        while(self.video_thread_on):
            # Reads the video frame and returns the
            # status of the read
            self.hasFrame, self.frame = self.cap.read()
      
    def cancelTimer(self):
        """
        Used to set the boolean flag when the send/receive
        timer is complete.
        """
        self.timerIsComplete = True

    def send(self, message, delay=0):
        """
        Takes in a string and a int as arguments. The string is 
        the message to be encoded. The number is the time in seconds
        to pause after the command is sent.

        This function will listen for a response. If a response is not
        received within so many seconds, as defined by the variable
        self.MSG_WAIT_TIME, then the function declares that there was
        an error sending the message.
        """

        # Clear the timer
        self.timerIsComplete = False

        # Create a timer that will run for X seconds and 
        # call cancelTimer when done
        timer = threading.Timer(self.MSG_WAIT_TIME, self.cancelTimer)

        # Begin the timer
        timer.start()

        # Try to send the message otherwise print the exception
        try:
            self.sock.sendto(message.encode(), self.tello_address)
            print("Sending message: " + message)
        except Exception as e:
            print("Error sending: " + str(e))

        # If there is no response, print a message
        while self.response is None:
            if self.timerIsComplete is True:
                print("There was no reply from Tello")
                break

        # End the timer thread
        timer.cancel()

        # If there was a response from the Tello, save the
        # message to a new variable and clear self.response
        # so that new messages do not overwrite the response
        if self.response is not None:
            data = self.response.decode(encoding='utf-8')
        else:
            data = "Timeout"

        # Reset response for the next time we read data
        self.response = None

        # If there is a wait, do it now
        time.sleep(delay)

        # Return the data to the caller
        return data

    def receive(self):
        # Continuously loop and listen for incoming messages
        while True:
            # Try to receive the message otherwise print the exception
            try:
                self.response, ip_address = self.sock.recvfrom(128)
                print("Received message: " + self.response.decode(encoding='utf-8'))
            except Exception as e:
                # If there's an error close the socket and break out of the loop
                self.sock.close()
                print("Error receiving: " + str(e))
                break

    def battery(self):
        """
        Returns the battery state the Tello. Value between 0 and 100
        """

        return self.send("battery?")

    def fwd(self, dist):
        """
        Moves the Tello forward by 'dist' centimeters
        """

        return self.send("forward " + str(dist))

    def back(self, dist):
        """
        Moves the Tello back by 'dist' centimeters
        """

        return self.send("back " + str(dist))

    def left(self, dist):
        """
        Moves the Tello to the left by 'dist' centimeters
        """

        return self.send("left " + str(dist))

    def right(self, dist):
        """
        Moves the Tello forward by 'dist' centimeters
        """

        return self.send("right " + str(dist))

    def up(self, dist):
        """
        Moves the Tello upward by 'dist' centimeters
        """

        return self.send("up " + str(dist))

    def down(self, dist):
        """
        Moves the Tello forward by 'dist' centimeters
        """

        return self.send("down " + str(dist))

    def flip(self, direction):
        """
        Flips the drone in the given direction. Valid 
        parameters are 'l' (left), 'r' (right), 'f' (forward)
        and 'b' (backward).
        """

        return self.send("flip " + direction)

