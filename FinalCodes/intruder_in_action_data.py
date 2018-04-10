import mysql.connector
from mysql.connector import Error
from db2 import Db
import logging
class IntruderInActionData:
    	
	def __init__(self,id,common_id,intruder_id, camera_id, video_id, start_time, end_time, start_frame, end_frame):
		self.id = id
		self.intruder_id = intruder_id
		self.camera_id = camera_id
		self.video_id = video_id
		self.start_time = start_time
		self.end_time = end_time
		self.start_frame = start_frame
		self.end_frame = end_frame
		self.common_id = common_id
		
		
	def insert(self):
		conn = None
		
		try:
			conn = Db.get_connection()
			insertQuery = "insert into intruder_in_action(intruder_id,camera_id,video_id,start_time,end_time,start_frame,end_frame) values( \
							{},{},{},'{}','{}','{}','{}')".format(	\
								self.intruder_id, self.camera_id, self.video_id, self.start_time, self.end_time, self.start_frame, self.end_frame)
			print insertQuery
			cursor = conn.cursor()
			cursor.execute(insertQuery)
			conn.commit()
			
			self.id = cursor.lastrowid
		
		except Exception as e:
			logging.exception("Error while saving video clip")
			
			
		Db.disconnect(conn)
 
	@staticmethod
	def select_recent_actions():
		'''
		for (intruder_id,camera_id, video_id,start_time,end_time,start_frame,end_frame) in cursor:
			print("intruder_id: {}, camera_id: {}, video_id{}, start_time: {}, end_time{}, start_frame{}, end_frame{} ".format(
				intruder_id,camera_id, video_id,start_time, end_time,start_frame,end_frame))
		'''
		conn = None
		actions = {}
		try:
			
			conn = Db.get_connection()
			
			selectQuery = "SELECT id,common_id,intruder_id,camera_id, video_id,start_time,end_time,start_frame,end_frame FROM intruder_in_action "
			
			cursor = conn.cursor()
			cursor.execute(selectQuery) 
			results = cursor.fetchall()
			
			for row in results:
				#print row
				action = IntruderInActionData(row[0],row[1],row[2], row[3],row[4],row[5],row[6],row[7],row[8])
				if actions.has_key(action.camera_id):
					list = actions[action.camera_id]
					list.append(action)
				else:
					list = []
					list.append(action)
					actions[action.camera_id] = list
				
		except Exception as e:
			logging.exception("Error while reading from database.")
		
		return actions
			
	@staticmethod
	def update(conn,id, new_id):
		updateQuery = ("UPDATE intruder_in_action set intruder_id = '"+str(new_id)+"' where id='"+str(id)+"'")
		cursor = conn.cursor()
		cursor.execute(updateQuery)
		conn.commit()
