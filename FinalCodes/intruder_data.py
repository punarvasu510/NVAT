import mysql.connector
from mysql.connector import Error
from db2 import Db
import logging

class IntruderData:
    
	def __init__(self, id, frame, camera_id):
		self.id = id
		self.frame = frame
		self.camera_id = camera_id
	
	def delete(self):
		conn = None
		try:
			conn = Db.get_connection()
			
			deleteQuery = ("delete from intruder_data where id = {}".format(self.id))
			cursor = conn.cursor()
			cursor.execute(deleteQuery)
			conn.commit()
		except Exception as e:
			logging.exception("Error while deleting intruder data from db: %d" % self.id)
			
		Db.disconnect(conn)
	
	def insert(self):
		conn = None
		
		try:
			conn = Db.get_connection()
			
			frame_file = ""
			if (self.frame is not None):
				frame_file = self.frame
				
			insertQuery = ("insert into intruder_data(frame,camera_id) values('{}', {})".format(frame_file,self.camera_id))
			cursor = conn.cursor()
			cursor.execute(insertQuery)
			
			# Fetch the auto increment id
			self.id = cursor.lastrowid  # conn.insert_id()
			print "Intruder ID: %d" %(self.id)
			conn.commit()
		except Exception as e:
			logging.exception("Error while saving intruder data into db")
			
		Db.disconnect(conn)
		
	@staticmethod
	def get_by_id(id):
		conn = None
		intruder = None
		
		try:
			conn = Db.get_connection()
			
			selectQuery = ("SELECT id,frame,start_time FROM intruder_data where id = {}".format(id))
			
			cursor = conn.cursor()
			cursor.execute(selectQuery)
			row = cursor.fetchone()
			
			if (row is not None):
				intruder = IntruderData(row[0], row[1])

		except Exception as e:
			logging.exception("Error while loading intruder data from db: %s" % id)
			
		
		Db.disconnect(conn)
		
		return intruder
		