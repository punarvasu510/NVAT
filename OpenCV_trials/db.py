import mysql.connector
from mysql.connector import Error
 
 
def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='project',
                                       user='root',
                                       password='root123')
        if conn.is_connected():
            print('Connected to MySQL database')
		
        cursor = conn.cursor()

        query = ("SELECT id, intruder_id, vdate, vtime FROM videos ")
        insertQuery = ("insert into videos(id,intruder_id,vdate,vtime) values(4, 201, '18-02-10', '22:50:10')")
        cursor.execute(insertQuery)
        conn.commit()
        cursor.execute(query)
        
		
        for (id, intruder_id, vdate, vtime) in cursor:
            print("id: {}, intruder_id: {}, date: {:%d %b %Y}, time: {}".format(
                id, intruder_id, vdate, vtime))
    
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 
 
if __name__ == '__main__':
    connect()