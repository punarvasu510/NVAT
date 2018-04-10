import datetime
import sys
import time
import cv2
import imutils
import numpy as np
from datetime import datetime
#import ffmpy
from datetime import timedelta
from ffprobe import FFProbe
import intruderData
import db2
from PIL import Image
import imagehash
import argparse
import shelve
import copy
from intruder import Intruder
from intruder_data import IntruderData
from camera_data import CameraData
from video_data import VideoData

class DetectAndSave:

	def __init__(self):
		self.camera_data = None
		self.video_clip = None
		self.video_data = None
		self.frames_per_second = 25
		self.start_time = None
		self.current_time = None
		
	def create_video_clip(self, file_name, width, height):
		if (self.video_clip is not None):
			self.video_clip.release()
			
		file_path = "video_clips/{}".format(file_name.replace(':', '-'))
		
		self.video_clip = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc('M','J','P','G'), 25, (width, height))
		
		# Store it in db
		self.video_data = VideoData(None, self.camera_data.id, self.current_time, None, file_path)
		
		self.video_data.insert()
		
	def detect(self, camera, video, start_time):
		self.camera_data = camera
		self.start_time = start_time
		self.current_time = start_time
		
		frame_width = int(video.get(3))
		frame_height = int(video.get(4))
	
		# initialize the first frame in the video stream
		firstFrame = None
		i=0
		#t1 = timedelta(hours=11, minutes=14)
		
		#a = video.get(cv2.CAP_PROP_FRAME_COUNT)


		frame_count = 0
		
		# loop over the frames of the video
		while True:
			# grab the current frame and initialize the status
			(grabbed, frame) = video.read()
			text = " "
			orig_frame = copy.copy(frame)
			
			frame_count += 1
			
			#updates timer
			if (frame_count % self.frames_per_second == 0):
				self.current_time += timedelta(seconds=1)
				#print "Time: {}".format(self.current_time)
				
			#if video clip created
			if (self.video_clip is not None):
				self.video_clip.write(frame)
			
			#skips every other frame
			if (frame_count % 2 != 0):
				continue
				
			#every second check
			if (frame_count % 1*self.frames_per_second == 0):	
				video_id = -1
				if (self.video_data is not None):
					video_id = self.video_data.id
					
				#checks if intruder is active, calls function from intruder.py
				Intruder.check_active(frame_count, self.current_time, video_id)
				
				#if no more intruders in frame
				if Intruder.get_count() == 0:
					# stop recording
					if self.video_clip is not None:
						print "Closing the video clip ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
						self.video_clip.release()
						self.video_clip = None
						# Update end time of the video clip
						self.video_data.end_time = self.current_time
						self.video_data.update()
						

			# if the frame could not be grabbed, then we have reached the end of the video
			if not grabbed:
				break

			# convert it to grayscale, and blur it
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
			retval,thresh = cv2.threshold(frameDelta, 40, 255, cv2.THRESH_BINARY)
			#print thresh
			#print retval
			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			thresh = cv2.dilate(thresh, None, iterations=2)
			#(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			#	cv2.CHAIN_APPROX_SIMPLE)
			(_,cnts,_) = cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
			count=0
			
			if cnts is None or len(cnts) < 1:
				continue
			
			#t1 = timedelta(hours=11, minutes=14)
			#t3 = timedelta(hours=1, minutes=30)
			
			date=datetime(2018,2,22,18,00)
			date1=datetime(2018,2,22,23,59)
			date2=datetime(2018,2,22,00,00)
			date3=datetime(2018,2,22,06,00)
			
			#id = 1;
			#flag1=0
			flag = 0
			# loop over the contours
			for c in cnts:
				
				
				# compute the bounding box for the contour, draw it on the frame,
				# and update the text
				
				#count=0
				if (self.current_time.time() > date.time() and self.current_time.time() < date1.time()) \
					or (self.current_time.time() > date2.time() and self.current_time.time() < date3.time()):
					
					(x, y, w, h) = cv2.boundingRect(c)
					#print("position: x: %s, y: %s,  w: %s, h: %s" %  (x, y, w, h))
					
					# Ignore small objects
					#if h < 35 or w < 35:
						#continue
					
					if x > 35 and y > 56 and h > 20 and w > 20 and y < 500 and x < 700:
						#xCenter=x + w/2;
						#yCenter=y + h/2;
						
						video_id = None
						if (self.video_data is not None):
							video_id = self.video_data.id
						
						#check if intruder is present
						intruder = Intruder.check_intruders(x, y, w, h, frame_count, self.current_time, self.camera_data.id)
						print x
						print y
						if (intruder.removed):
							continue
							
						if (intruder.new and Intruder.get_count() == 1):
							# This is first intruder in this session
							# Start recording the video clip
							file_name = "Video_{}_{}.mp4".format(camera.id, self.current_time)
							self.create_video_clip(file_name, frame_width, frame_height)
							
						# Draw rectangle box around the intruder
						cv2.rectangle(frame, (x, y), (x + w, y + h), intruder.color[i], 2)
						
						crop_img = orig_frame[y-40:y+h+40, x-40:x+w+40]
					
						#query = Image.open("Image1.png")
						if (intruder.new  ):
							# Save the image of the intruder to file system
							
							frame_file = "intruder_profiles/cropFrame_{}.jpg".format(intruder.data.id)
							frame_file1 = "intruder_profiles/fullFrame_{}.jpg".format(intruder.data.id)
						
							cv2.imwrite(frame_file, crop_img)
							cv2.imwrite(frame_file1, orig_frame)
						
						#count += 1
						text = "DETECTED!!!"    
						
			# draw the text and timestamp on the frame
			#print str(camera.get(cv2.CAP_PROP_POS_MSEC)
			cv2.putText(frame, text , (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1.0 , (0, 0, 255), 2)
			#cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

			
			#flag1++;
			# show the frame and record if the user presses a key
			
			cv2.imshow("Frame Delta", frameDelta)
			cv2.imshow("Thresh", thresh)
			cv2.imshow("Security Feed", frame)
			
			key = cv2.waitKey(1) & 0xFF
			# if the `q` key is pressed, break from the loop
			if key == ord("q"):
				break
			if key == 112:  # 'p' has been pressed. this will pause/resume the code.
				pause = not pause
				if (pause is True):
					print("Code is paused. Press 'p' to resume..")
					while (pause is True):
					# stay in this loop until
						key = cv2.waitKey(30) & 0xff
					if key == 112:
						pause = False
						print("Resume code..!!")
						break
						
		# cleanup the camera and close any open windows
		video.release()
		cv2.destroyAllWindows()

if __name__ == '__main__':
			
	camera_id = sys.argv[2]
	camera = CameraData.get_by_id(int(camera_id))
	
	if (camera is None):
		print "Camera with id: %d not found" % camera_id
		exit(-1)
	
	d = DetectAndSave()
	#get images from db
	
	if len(sys.argv) == 1:
		file = 'Friday5_2018-02-02 06-36-24.mp4'
	else:
		file = sys.argv[1]
		
	# parse datetime from file name
	# format: Friday5_2018-02-02 06:36:24.mp4
	
	# get file name part by excluding the extension
	tokens = file.split(".")
	if (len(tokens) < 2):
		print "Invalid file format: datetime is missing"
		exit(-1)
	
	name = tokens[len(tokens) - 2]
	
	tokens = name.split("_")
	
	if (len(tokens) < 2):
		print "Invalid file format: date time is missing"
		exit(-1)
		
	#print "Datetime: %s" % tokens[len(tokens) - 1]
	
	start_time = datetime.strptime(tokens[len(tokens) - 1], "%Y-%m-%d %I-%M-%S")
	
	print "Datetime: {}".format(start_time)
	
	video = cv2.VideoCapture(file)
	
	#video='vid.mp4'
	d.detect(camera, video, start_time)