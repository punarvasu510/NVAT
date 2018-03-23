import datetime
import sys
import time
import cv2
import imutils
import numpy as np
from datetime import datetime
import ffmpy
from datetime import timedelta
from ffprobe import FFProbe

# python3 DetectIntruder.py
if len(sys.argv) == 1:
	camera = cv2.VideoCapture('bus.mp4')
	time.sleep(0.25)
# python3 DetectIntruder.py videos/example_1.mp4
else:
	camera = cv2.VideoCapture(sys.argv[1])

frame_width = int(camera.get(3))
frame_height = int(camera.get(4))

flag=0 
flag1=0 


#metadata=FFProbe('example_1.mp4')
# initialize the first frame in the video stream
firstFrame = None
i=0
t1 = timedelta(hours=11, minutes=14)

a = camera.get(cv2.CAP_PROP_FRAME_COUNT)

#print a
out = cv2.VideoWriter('outpyt%d.avi' % flag1,cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

# loop over the frames of the video
while True:
	# grab the current frame and initialize the status
	(grabbed, frame) = camera.read()
	text = " "
	
	#i=i+1
	#print("Frame"+str(i)+":\t"+str(camera.get(cv2.CAP_PROP_POS_MSEC)))
	

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	#frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	#(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	#	cv2.CHAIN_APPROX_SIMPLE)
	(_,cnts,_) = cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	count=0
	# loop over the contours
	
	t1 = timedelta(hours=11, minutes=14)
	t3 = timedelta(hours=1, minutes=30)
	
	date=datetime(2018,2,22,5,00)
	
	flag1=0
	for c in cnts:
		
		
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		'''
		dur = str(camera.get(cv2.CAP_PROP_POS_MSEC))
		for stream in metadata.streams:
			if stream.isVideo():
				a = round(float(stream.start_time),0)
		m, s = divmod(a, 60)
		h, m = divmod(m, 60)
		t2 = timedelta(hours=h, minutes=m)
		a1 = round(float(dur),0)
		m1,s1 = divmod(a1,60)
		h1, m1 = divmod(m1, 60)
		t4 = timedelta(hours=h1, minutes=m1)
		time = t2 - t1
		time = time + t4
		print time
		'''
        count=0
        if datetime.now().time() > date.time():
			
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            success,image = camera.read()
			#if flag1==0:
				#cv2.imwrite("frame%d%d.jpg" % (flag,count), image)
			#	flag1=1
            crop_img = image[y:y+h, x:x+w]
            #if count==0:
            cv2.imwrite("cropFrame%d.jpg" % count, crop_img)
            count += 1
            text = "DETECTED!!!"    
            flag=flag+1
            out.write(frame)
	
	# draw the text and timestamp on the frame
	#print str(camera.get(cv2.CAP_PROP_POS_MSEC)
	cv2.putText(frame, text , (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1.0 , (0, 0, 255), 2)
	#cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()