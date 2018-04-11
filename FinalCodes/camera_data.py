import mysql.connector
from mysql.connector import Error
from db2 import Db
import logging

class CameraData:
	camera_list = None
	
	def __init__(self, row):
		self.id = row[0]
		self.location = row[1]
		self.description = row[2]
	
	@staticmethod
	def get_by_id(id):
		if (CameraData.camera_list is None):
			CameraData.load_all()
			
		if (CameraData.camera_list.has_key(id)):
			return CameraData.camera_list[id]
			
		return None
		
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
            
