from intruder_in_action_data import IntruderInActionData
from FLANN import Flann
import time
import datetime

class Matcher:
	
	@staticmethod
	def run():
		actions = {}
		action_map = IntruderInActionData.select_recent_actions()
		#print action_map
		for camera_id, action_list in action_map.items():
			for action1 in action_list:
				for camera2_id, action2_list in action_map.items():
					if (camera2_id == camera_id):	# ignore same camera actions
						continue
					print "camera1: {} camera2: {}".format(camera_id,camera2_id)
					for action2 in action2_list:
						
						# compare the end time of action1 and start time of action 2
						var1 = time.mktime(action1.end_time.timetuple())
						var2 = time.mktime(action2.start_time.timetuple())
						
						
						if((action1.end_time <= action2.start_time) and (action1.end_time.time() < action2.start_time.time()) and ((var1-var2)/60 < 5)):
							print "action1 : {} endtime: {} , action2: {} starttime{} ".format(action1.id,action1.end_time,action2.id,action2.start_time)
							print action1.intruder_id
							print action2.intruder_id
							f = Flann(action1,action2)
							f.match()
							
						else:
							print "Skipped"
if __name__ == '__main__':
	Matcher.run()
		