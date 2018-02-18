import cv2
import numpy as np
from datetime import datetime

# Create a VideoCapture object
cap = cv2.VideoCapture('Thursday5.mp4')
 
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

date = datetime(2018,2,15,22,15);

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
if datetime.now().time() > date.time():
	out = cv2.VideoWriter('outpy2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))



while(True):
  ret, frame = cap.read()
 
  if ret == True: 
	if datetime.now().time() > date.time():
		out.write(frame)
		
	cv2.imshow('frame',frame)
 
    # Press Q on keyboard to stop recording
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break	
    
 
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
out.release()
 
# Closes all the frames
cv2.destroyAllWindows() 