import mysql.connector
from mysql.connector import Error
from db2 import Db
import logging

class VideoData:
    
	def __init__(self, id, camera_id, start_time, end_time, file_path):
		self.id = id
		self.camera_id = camera_id
		self.start_time = start_time
		self.end_time = end_time
		self.file_path = file_path
		
	def insert(self):
		conn = None
		
		try:
			conn = Db.get_connection()
			
			insertQuery = ("insert into video_clips(camera_id, start_time, file_path) values({},'{}','{}')".format(
							self.camera_id, self.start_time, self.file_path))
			cursor = conn.cursor()
			cursor.execute(insertQuery)
			
			self.id = cursor.lastrowid
			
			conn.commit()
		except Exception as e:
			logging.exception("Error while saving video clip")
			
		Db.disconnect(conn)
	
	def update(self):
		conn = None
		
		try:
			conn = Db.get_connection()
			
			updateQuery = ("update video_clips set end_time='{}' where id={}".format(self.end_time, self.id))
			cursor = conn.cursor()
			cursor.execute(updateQuery)
			
			conn.commit()
		except Exception as e:
			logging.exception("Error while updating video clip")
			
		Db.disconnect(conn)
		
	@staticmethod
	def select(conn):
		selectQuery = ("SELECT * FROM video_clips ")
		cursor = conn.cursor()
		cursor.execute(selectQuery)
		for (id,camera_id, start_time,end_time,file_path) in cursor:
			print("id: {}, camera_id: {}, start_time: {}, end_time{}, file_path{} ".format(
						id,camera_id, start_time, end_time,file_path))
	