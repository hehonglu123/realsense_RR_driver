#Simple example Robot Raconteur webcam client
#This program will show a live streamed image from
#the webcams.  Because Python is a slow language
#the framerate is low...

from RobotRaconteur.Client import *

import time, math
import numpy as np
import cv2
import sys, traceback
import matplotlib.pyplot as plt


#Function to take the data structure returned from the Webcam service
#and convert it to an OpenCV array
def ImageToMat(image):

	frame2=image.data.reshape([image.image_info.height, image.image_info.width, int(len(image.data)/(image.image_info.height*image.image_info.width))], order='C')
	return frame2


def deform_pc(RR_pc):
	return RR_pc.points.view((float, len(RR_pc.points.dtype.names)))

current_frame=None
image_type='depth'
#This function is called when a new pipe packet arrives
def new_frame(pipe_ep):
	global current_frame, image_type

	#Loop to get the newest frame
	while (pipe_ep.Available > 0):
		#Receive the packet
		
		image=pipe_ep.ReceivePacket()
		#Convert the packet to an image and set the global variable
		if image_type=='color':
			current_frame=ImageToMat(image)
		else:
			current_frame=ImageToMat(image.depth_image)

		return

def main():

	url='rr+tcp://localhost:25415?service=RS_Service'
	if (len(sys.argv)>=2):
		url=sys.argv[1]

	#Startup, connect, and pull out the camera from the objref    
	rs_obj=RRN.ConnectService(url)

	#Connect the pipe FrameStream to get the PipeEndpoint p
	p=rs_obj.depth_image_stream.Connect(-1)
	# p=rs_obj.depth_image_stream.Connect(-1)

	#Set the callback for when a new pipe packet is received to the
	#new_frame function
	p.PacketReceivedEvent+=new_frame


	try:
		rs_obj.StartStreaming()
	except: pass

	cv2.namedWindow("Image")

	while True:
		#Just loop resetting the frame
		#This is not ideal but good enough for demonstration

		if (not current_frame is None):
			cv2.imshow("Image",current_frame)
		if cv2.waitKey(50)!=-1:
			break
	cv2.destroyAllWindows()

	p.Close()
	rs_obj.StopStreaming()



if __name__ == '__main__':
	main()
