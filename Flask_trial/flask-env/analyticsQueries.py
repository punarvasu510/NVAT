import logging
from db2 import Db
from intruder_in_action_data import IntruderInActionData
from video_data import VideoData
import datetime
import generateTapestry

class UserQuery:


	@staticmethod
	def day_wise_intruder_distribution(t1, t2):
		conn = None

		count = 0

		try:
			conn = Db.get_connection()

			#selectQuery2 = "select count(distinct common_id) as count from intruder_in_action where {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)
			#selectQuery3 = "select count(intruder_id) as count from intruder_in_action where common_id is null and {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)"

			data = []

			ttemp1 = datetime.datetime.combine(t1.date(),datetime.time.min)
			ttemp2 = ttemp1 + datetime.timedelta(days=1)

			while (ttemp2 < t2):

				query = "select count(distinct common_id) as count from intruder_in_action \
							where start_time >= '{}' and end_time <= '{}'".format(ttemp1, ttemp2, ttemp1, ttemp2)

				query2 = "select count(distinct intruder_id) as count from intruder_in_action \
							where common_id is null and start_time >= '{}' and end_time <= '{}'".format(ttemp1, ttemp2, ttemp1, ttemp2)

				cursor = conn.cursor()
				cursor.execute(query)

				results = cursor.fetchall()
				for row in results:
					count += row[0]

				cursor.execute(query2)

				results = cursor.fetchall()
				for row in results:
					count += row[0]

				data.append({"date":ttemp1,"count":count})
				ttemp1 = ttemp2
				ttemp2 = ttemp2 + datetime.timedelta(days=1)

		except Exception as e:
			logging.exception("Error while retrieving statistics from table")

		Db.disconnect(conn)

		return data

if __name__ == '__main__':
	# Get total intruders in the given time range
	total_intruders = UserQuery.day_wise_intruder_distribution(
						datetime.strptime("2018-02-02 01:50:00", "%Y-%m-%d %I:%M:%S"),
						datetime.strptime("2018-02-02 02:50:00", "%Y-%m-%d %I:%M:%S")
					  )

	print "Total unique intruders in the time range given: {}".format(total_intruders)
