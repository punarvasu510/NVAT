import math
import os
import numpy as np
from intruder_data import IntruderData
from intruder_in_action_data import IntruderInActionData

class Intruder:
	current_list = []	# current active intruders
	
	def __init__(self, x, y, w, h, frame_num, start_time, camera_id, video_id):
		self.center_x = x
		self.center_y  = y
		self.start_frame_num = frame_num
		self.last_frame_num = frame_num
		self.start_time = start_time
		self.end_time = start_time
		self.camera_id = camera_id
		self.video_id = video_id
		self.color = np.random.randint(0,255,(100,3))
		self.new = True
		self.first_x = x
		self.first_y = y
		self.removed = False
		self.data = None
		
		
	@staticmethod
	def get_count():
		#return len(Intruder.current_list)
		# return active count only
		count = 0
		
		for intruder in Intruder.current_list:
			if (intruder.removed):
				continue
			count += 1
			
		return count
		
	def check(self, x, y, w, h, frame_num):
		new_center_x = x+w/2
		new_center_y = y+h/2
		
		distance = math.sqrt((new_center_x-self.center_x)**2 + (new_center_y-self.center_y)**2)

		#print "Intruder distnace: %s" %  distance
		
		if (frame_num - self.last_frame_num < 25*10 and abs(self.center_x - x) < 50 and abs(self.center_y - y) < 50 and distance < 200):
			# check if it moved at all
			if (frame_num - self.start_frame_num > 15*25 and (abs(self.first_x - self.center_x) < 10 or abs(self.first_y - self.center_y) < 10)):
				#print "This intruder is not moving"
				self.removed = True
				
			# update self data
			self.center_x = x
			self.center_y = y
			self.last_frame_num = frame_num
			self.new = False
			
			return True
			
		return False
		
	def insert_in_db(self):
		self.data = IntruderData(None, None,self.camera_id)
		self.data.insert()
		
	def update_action(self):
		action = IntruderInActionData(None,None,self.data.id, self.camera_id, self.video_id,  self.start_time, self.end_time, self.start_frame_num, self.last_frame_num)
		action.insert()
		
		
	@staticmethod
	def check_intruders(x, y, w, h, frame_num, start_time, camera_id):
		for intruder in Intruder.current_list:
			if (intruder.check(x, y, w, h, frame_num)):
				return intruder
				
		intruder = Intruder(x, y, w, h, frame_num, start_time, camera_id, -1)
		
		Intruder.current_list.append(intruder)
		
		# Save it in db
		intruder.insert_in_db()
		
		print "Found new intruder: %s" % frame_num 
		
		return intruder
		
	@staticmethod
	def check_active(current_frame_num, current_time, video_id):
		# Checks each active intruder is still active
		
		for intruder in reversed(Intruder.current_list):
			if (current_frame_num - intruder.last_frame_num > 10*25):
				print "This intruder is no more active xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
				Intruder.current_list.remove(intruder)
				
				if (intruder.removed):
					# remove the profile file
					file_path = "intruder_profiles/cropFrame_{}.jpg".format(intruder.data.id)
					os.remove(file_path)
					print "Removed file {} KKKKKKKKKKKKKKKKKKKKKKKKKK".format(file_path)
					#remove from db
					intruder.data.delete()
					continue
				
				# Update the intruder in action in db				
				intruder.end_time = current_time
				intruder.last_frame_num = current_frame_num
				intruder.video_id = video_id
				intruder.update_action()
				
				
			
				
				