import numpy as np
import cv2
import sys

myFrameNumber = int(sys.argv[1])
cap = cv2.VideoCapture("example_1.mp4")

# get total number of frames
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# check for valid frame number

if myFrameNumber >= 0 and myFrameNumber <= totalFrames:
	# set frame position
	cap.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)

	print("Timestamp:----------------"+str(cap.get(cv2.CAP_PROP_POS_MSEC)))	
	ret, frame = cap.read()
	
	name = 'Frame_'+ str(myFrameNumber) + '.jpg'
	cv2.imwrite(name, frame)	

cv2.destroyAllWindows()



