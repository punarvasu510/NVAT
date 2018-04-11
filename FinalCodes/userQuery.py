from db2 import Db
from intruder_in_action_data import IntruderInActionData

class userQuery:

	intruder_list  = []
	video_list = []
	intruderClips_list = []
	
	@staticmethod
	def getTotalCount(t1,t2)
		conn = None
	
		
		try:
		
			selectQuery2 = "select count(distinct common_id) as count from intruder_in_action where {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)
			selectQuery3 = "select count(intruder_id) as count from intruder_in_action where common_id is null and {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)"
			cursor = conn.cursor()
			cursor.execute(selectQuery2)
			conn.commit()
		
			results = cursor.fetchall()
			for row in results
				count1 = row
			cursor = conn.cursor()
			cursor.execute(selectQuery3)
			conn.commit()
			
			results=cursor.fetchall
			for row in results
				count2 = row
			totalCount = count1+count2
			
			return totalCount
		
		except Exception as e:
			logging.exception("Error while retrieving statistics from table")
		
		Db.disconnect(conn)
	
	
	@staticmethod
	def getIntruders(t1,t2):
		conn = None
		
		try:
		
			conn = Db.get_connection()
			
			selectQuery = "SELECT intruder_id FROM intruder_in_action where {} >= {} and {} <= {}".format(start_time, end_time,t1,t2)
		
			cursor = conn.cursor()
			cursor.execute(selectQuery)
			conn.commit()
		
			results = cursor.fetchall()
			for row in results:
				userQuery.intruder_list.append(row)
			
			
			return intruder_list
		
		except Exception as e:
			logging.exception("Error while retrieving intruders from table")
		
		Db.disconnect(conn)
	
	@staticmethod
	def getVideoClips(t1,t2):
		conn = None
		try:
		
			conn = Db.get_connection()
			
			selectQuery = "SELECT file_path FROM video_clips where id in(select video_id from intruder_in_action where {} >= {} and {} <= {})".format(start_time, t1,end_time,t2)
		
			cursor = conn.cursor()
			cursor.execute(selectQuery)
			conn.commit()
		
			results = cursor.fetchall()
			
			for row in results:
				userQuery.video_list.append(row)
				
			
			return video_list
		
		except Exception as e:
			logging.exception("Error while retrieving videos from table")
		
		Db.disconnect(conn)
		
	@staticmethod
	def intruderClips(id):
		conn = None
		try:
		
			conn = Db.get_connection()
			
			selectQuery = "SELECT * FROM intruder_in_action where common_id in(select common_id from intruder_in_action \
			where intruder_id ={}  and {} >= {} and {} <= {}) \
			union \
			select * FROM intruder_in_action where {} >= {} and {} <= {} and {} is null \
			order by {}".format(id,start_time,t1, end_time,t2,start_time,t1,end_time,t2.common_id)
		
			cursor = conn.cursor()
			cursor.execute(selectQuery)
			conn.commit()
		
			results = cursor.fetchall()
			
			for row in results:
				intruder_clip = IntruderInActionData(row)
				intruderClips_list.append.intruder_clip
				
			return intruderClips_list
			
		except Exception as e:
			logging.exception("Error while retrieving videos from table")
		
		Db.disconnect(conn)