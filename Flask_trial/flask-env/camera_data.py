import mysql.connector
from mysql.connector import Error
from db2 import Db
import logging

class CameraData:
	camera_list = None
	
	def __init__(self,row):
		self.id = row[0]
		self.location = row[1]
		self.description = row[2]
	
	@staticmethod
	def get_by_id(id):
		try:
		
			if (CameraData.camera_list is None):
				CameraData.load_all()
			
			if (CameraData.camera_list.has_key(id)):
				print "camera list: {}".format(CameraData.camera_list[id])
				return CameraData.camera_list[id]
		except Exception as e:
			logging.exception("Error in get_by_id")
			
		return None
		
	@staticmethod
	def insert(description):
		camera = None
		try:
			conn = Db.get_connection()
			print description
			insertQuery = "insert into camera_data(description) values('{}')".format(description)
			cursor = conn.cursor()
			cursor.execute(insertQuery)
			conn.commit()
			
			id = cursor.lastrowid
			camera = CameraData.load_by_id(id)
			print "Id in insert: {}".format(id)
			
			#print id
			
		except Exception as e:
			logging.exception("Error while inserting camera description")
			
		Db.disconnect(conn)
		
		return camera 
		
	@staticmethod
	def load_all():
		conn = None
		try:
			CameraData.camera_list  = dict()
			
			conn = Db.get_connection()
			
			selectQuery = "SELECT id, location, description FROM camera_data"
			cursor = conn.cursor()
			cursor.execute(selectQuery)
			results = cursor.fetchall()
			
			for row in results:
				camera = CameraData(row)
				print "Loaded camera: %d" % camera.id
				CameraData.camera_list[camera.id] = camera
				
		except Exception as e:
			logging.exception("Error while loading camera list from database.")
			#print "Error while loading camera list from database. Error: %s" % str(e)
			
		Db.disconnect(conn)
		
		
	@staticmethod
	def load_by_id(id):
		conn = None
		camera = None 
		try:
			if CameraData.camera_list is None:
				CameraData.load_all()
			
			conn = Db.get_connection()
			
			selectQuery = "SELECT id, location, description FROM camera_data where id = {}".format(id)
			cursor = conn.cursor()
			cursor.execute(selectQuery)
			results = cursor.fetchall()
			
			for row in results:
				camera = CameraData(row)
				print "Loaded camera: %d" % camera.id
				CameraData.camera_list[camera.id] = camera
				
		except Exception as e:
			logging.exception("Error while loading camera list from database.")
			#print "Error while loading camera list from database. Error: %s" % str(e)
			
		Db.disconnect(conn)
        
		return camera
