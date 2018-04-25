import logging
from db2 import Db
from intruder_in_action_data import IntruderInActionData
from video_data import VideoData
import datetime
import generateTapestry

class AnalyticsQuery:

	@staticmethod
	def day_wise_distribution(d1, d2):
		conn = None

		count = 0

		try:
			conn = Db.get_connection()

			#selectQuery2 = "select count(distinct common_id) as count from intruder_in_action where {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)
			#selectQuery3 = "select count(intruder_id) as count from intruder_in_action where common_id is null and {} >= {} and {} <= {}".format(start_time, t1,end_time,t2)"

			data = []

			dtemp1 = d1
			dtemp2 = dtemp1 + datetime.timedelta(days=1)

			while (dtemp2 <= d2):
				count = 0

				query = "select count(distinct common_id) as count from intruder_in_action \
							where start_time >= '{}' and end_time <= '{}'".format(dtemp1, dtemp2, dtemp1, dtemp2)

				query2 = "select count(distinct intruder_id) as count from intruder_in_action \
							where common_id is null and start_time >= '{}' and end_time <= '{}'".format(dtemp1, dtemp2, dtemp1, dtemp2)

				cursor = conn.cursor()
				cursor.execute(query)

				results = cursor.fetchall()
				for row in results:
					count += row[0]

				cursor.execute(query2)

				results = cursor.fetchall()
				for row in results:
					count += row[0]

				data.append({"date":str(dtemp1.date()),"count":count})
				dtemp1 = dtemp2
				dtemp2 = dtemp2 + datetime.timedelta(days=1)

		except Exception as e:
			logging.exception("Error while retrieving statistics from table")

		Db.disconnect(conn)

		return data
	@staticmethod
	def camera_wise_distribution(date):
		"""
		conn = None

		count = 0

		try:
			conn = Db.get_connection()
			data=[]
		"""

		return ""





if __name__ == '__main__':
	# Get total intruders in the given time range
	total_intruders = UserQuery.day_wise_intruder_distribution(
						datetime.strptime("2018-02-02 01:50:00", "%Y-%m-%d %I:%M:%S"),
						datetime.strptime("2018-02-02 02:50:00", "%Y-%m-%d %I:%M:%S")
					  )

	print "Total unique intruders in the time range given: {}".format(total_intruders)
