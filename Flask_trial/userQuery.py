import logging
from db2 import Db
from intruder_in_action_data import IntruderInActionData
from video_data import VideoData

class UserQuery:


	@staticmethod
	def get_intruder_count(t1, t2):
		conn = None

		count = 0

		try:
			conn = Db.get_connection()

			#selectQuery2 = "select count(distinct common_id) as count from intruder_in_action where {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)
			#selectQuery3 = "select count(intruder_id) as count from intruder_in_action where common_id is null and {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)"

			query = "select count(distinct common_id) as count from intruder_in_action \
						where start_time >= '{}' and end_time <= '{}'".format(t1, t2, t1, t2)

			query2 = "select count(distinct intruder_id) as count from intruder_in_action \
						where common_id is null and start_time >= '{}' and end_time <= '{}'".format(t1, t2, t1, t2)

			cursor = conn.cursor()
			cursor.execute(query)

			results = cursor.fetchall()
			for row in results:
				count += row[0]

			cursor.execute(query2)

			results = cursor.fetchall()
			for row in results:
				count += row[0]

		except Exception as e:
			logging.exception("Error while retrieving statistics from table")

		Db.disconnect(conn)

		return count

	@staticmethod
	def get_intruders(t1, t2):

		conn = None
		intruder_id_list  = []
		try:

			conn = Db.get_connection()

			selectQuery = "SELECT distinct(intruder_id) FROM intruder_in_action where start_time >= '{}' and end_time <= '{}'".format(t1, t2, t1, t2)

			cursor = conn.cursor()
			cursor.execute(selectQuery)

			results = cursor.fetchall()
			for row in results:
				intruder_id_list.append(row[0])

		except Exception as e:
			logging.exception("Error while retrieving intruders from table")

		Db.disconnect(conn)

		return intruder_id_list

	@staticmethod
	def get_video_clips(t1, t2):

		video_list = []
		conn = None
		try:

			conn = Db.get_connection()

			selectQuery = "SELECT id, camera_id, start_time, end_time, file_path FROM video_clips where id in(select video_id from intruder_in_action \
							where start_time >= '{}' and end_time <= '{}') order by start_time".format(t1, t2)

			cursor = conn.cursor()
			cursor.execute(selectQuery)

			results = cursor.fetchall()

			for row in results:
				video_list.append(VideoData(row[0], row[1], row[2], row[3], row[4]))

		except Exception as e:
			logging.exception("Error while retrieving videos from table")

		Db.disconnect(conn)

		return video_list

	@staticmethod
	def get_intruder_video_clips(id, t1, t2):
		conn = None
		video_clips = []

		try:

			conn = Db.get_connection()

			selectQuery = "select id, camera_id, start_time, end_time, file_path from video_clips where id in (	\
							SELECT distinct(video_id) FROM intruder_in_action where common_id in \
							(select common_id from intruder_in_action  \
								where intruder_id = {}  and start_time >= '{}' and end_time <= '{}') \
							union \
								select distinct(video_id) FROM intruder_in_action \
								where intruder_id={} and start_time >= '{}' and end_time <= '{}' and common_id is null \
								order by start_time)".format(id, t1, t2, id, t1, t2)

			cursor = conn.cursor()
			cursor.execute(selectQuery)

			results = cursor.fetchall()

			for row in results:
				video_clip = VideoData(row[0], row[1], row[2], row[3], row[4])
				video_clips.append(video_clip)

		except Exception as e:
			logging.exception("Error while retrieving videos from table")

		Db.disconnect(conn)

		return video_clips

if __name__ == '__main__':
	# Get total intruders in the given time range
	total_intruders = UserQuery.get_intruder_count("2018-02-02 01:50:00", "2018-02-02 02:50:00")

	print "Total unique intruders in the time range given: {}".format(total_intruders)

	# Get unique intruder ids in the given time
	intruder_id_list = UserQuery.get_intruders("2018-02-02 01:50:00", "2018-02-02 02:50:00")

	for intruder_id in intruder_id_list:
		print "Intruder id: {}, profile image: intruder_profiles\\cropFrame_{}.jpg".format(intruder_id, intruder_id)

	# Get unique video clips in the given time sorted by start_time
	video_list = UserQuery.get_video_clips("2018-02-02 01:50:00", "2018-02-02 02:50:00")

	for video_data in video_list:
		print "Video id: {}, camera id: {}, start time: {}, end time: {}, file_path: {}".format( \
				video_data.id, video_data.camera_id, video_data.start_time, video_data.end_time, video_data.file_path)

	# Get unique video clips of an intruders in the given time range sorted by start_time
	video_list = UserQuery.get_intruder_video_clips(1428, "2018-02-02 01:50:00", "2018-02-02 02:50:00")

	for video_data in video_list:
		print "Video id: {}, camera id: {}, start time: {}, end time: {}, file_path: {}".format( \
				video_data.id, video_data.camera_id, video_data.start_time, video_data.end_time, video_data.file_path)

	
