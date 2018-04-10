import mysql.connector
from mysql.connector import Error
 	
class Db:
    
    @staticmethod
    def get_connection():
        """ Connect to MySQL database """
        try:
            conn = mysql.connector.connect(host='localhost',
                                           database='project',
                                           user='root',
                                           password='root123')
            if conn.is_connected():
                print('Connected to MySQL database')
		
                return conn
            else:	
			    return None
        except Error as e:
            print(e)
	
	'''	
    @staticmethod		
    def insert(conn):
        insertQuery = ("insert into videos(id,intruder_id,vdate,vtime) values(6, 201, '18-02-10', '22:50:10')")
        cursor = conn.cursor()
        cursor.execute(insertQuery)
        conn.commit()
	'''
    @staticmethod
    def disconnect(conn):
		if (conn is not None):
			conn.close()
    
'''
    @staticmethod
    def select(conn):
        selectQuery = ("SELECT id, intruder_id, vdate, vtime FROM videos ")
        cursor = conn.cursor()
        cursor.execute(selectQuery)
        for (id, intruder_id, vdate, vtime) in cursor:
            print("id: {}, intruder_id: {}, date: {:%d %b %Y}, time: {}".format(
                id, intruder_id, vdate, vtime))
    '''
