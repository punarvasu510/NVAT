import mysql.connector
from mysql.connector import Error
from subprocess import call


class Db:

    @staticmethod
    def connect():
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

    @staticmethod
    def insert(conn):
        insertQuery = ("insert into video(id,intruder_id,vdate,vtime) values(6, 201, '18-02-10', '22:50:10')")
        cursor = conn.cursor()
        cursor.execute(insertQuery)
        conn.commit()

    @staticmethod
    def disconnect(conn):
        conn.close()

    @staticmethod
    def select(conn):
        selectQuery = ("SELECT id, intruder_id, vdate, vtime FROM videos ")
        cursor = conn.cursor()
        cursor.execute(selectQuery)
        for (id, intruder_id, vdate, vtime) in cursor:
            print("id: {}, intruder_id: {}, date: {:%d %b %Y}, time: {}".format(
                id, intruder_id, vdate, vtime))


    @staticmethod
    # Fetch all videos of an intruder from database
    # Order them as per serial number ( which in determined by timestamp )
    # Loop through the result to add ffmpeg command ( which generates the intermediate file ) for each video
    # Loop through the result to add each intermediate file to input file (for concatenation)
    # Concatenate
    # Clear all intermediate files
    # The final tapestry is stored in output.mp4

    def generateTapestryByIntruder(conn, id):
        selectQuery = ("SELECT serial_number, video_id FROM tapestry where intruder_id = $id ORDER BY serial_number ASC");
        cursor = conn.cursor()
        cursor.execute(selectQuery)
        intermediate_dir = "/home/punarvasu510/Alekhya/FinalYearProject/GIT/NVAT/OpenCV_trials/"

        for (serial_number,video_id) in cursor:
            text_script = "ffmpeg -i " + str(video_id) + ".mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate_" + str(serial_number) + ".ts"
        #           ffmpeg -i     example_1   .mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate_          1          .ts
            comm = "echo " + text_script + " >> script_intermediate_test"
            call(comm, shell = True)

            text_input = "file " + intermediate_dir + "intermediate_" + str(serial_number) + ".ts"
            comm = "echo " + text_input + " >> input_test.txt"
            call(comm, shell = True)

        call("chmod 755 script_intermediate_test", shell = True)
        call("./script_intermediate_test", shell = True)
        call("ffmpeg -f concat -safe 0 -i input_test.txt -c copy output.mp4", shell = True)
        call("rm intermediate_*", shell = True)
        call("rm *_test*",shell = True)


if __name__ == '__main__':
    conn = Db.connect()

    Db.select(conn)
    Db.insert(conn)
	Db.disconnect(conn)
