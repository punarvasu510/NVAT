import cv2
import numpy as np
from datetime import datetime
import ffmpy
import datetime
from datetime import timedelta
from ffprobe import FFProbe

# Create a VideoCapture object
cap = cv2.VideoCapture('Thursday5.mp4')
 
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#date = datetime(2018,2,20,8,15);


metadata=FFProbe("Thursday5.mp4")

t1 = timedelta(hours=11, minutes=14)
t3 = timedelta(hours=5, minutes=30)

for stream in metadata.streams:
    if stream.isVideo():
		a = round(float(stream.start_time),0)
		m, s = divmod(a, 60)
		h, m = divmod(m, 60)
		t2 = timedelta(hours=h, minutes=m)
		start = t2 - t1
		print start
		
		

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
if start > t3:
	out = cv2.VideoWriter('outpy2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))



while(True):
  ret, frame = cap.read()
 
  if ret == True: 
	if start > t3:
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