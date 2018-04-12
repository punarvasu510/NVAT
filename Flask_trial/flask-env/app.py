from flask import Flask,render_template,json, request,redirect,url_for, jsonify, send_file
from userQuery import UserQuery
from datetime import datetime
import logging
import os, io

app = Flask(__name__)

@app.route('/')
def test():
   return "Novel Video Analytics and Tapestry"

###### Home page
@app.route('/home')
def home():
    return render_template('home.html')
######

##### Rendered on home page as buttons
@app.route('/getTotalCount')
def getTotalCountFirst():
    return render_template('getTotalCount.html')

@app.route('/getIntruders')
def getIntrudersFirst():
    return render_template('getIntruders.html')

@app.route('/intruderClips')
def intruderClipsFirst():
    return render_template('intruderClips.html')
######

@app.route('/getTotalCountNext')
def getTotalCountNext():
    t1 = str(request.values.get("t1"))
    t2 = str(request.values.get("t2"))

    t1 = t1.replace("T"," ") + ":00"
    t1 = datetime.strptime(t1, "%Y-%m-%d %I:%M:%S")

    t2 = t2.replace("T"," ") + ":00"
    t2 = datetime.strptime(t2, "%Y-%m-%d %I:%M:%S")

    count = UserQuery.get_intruder_count(t1,t2)
    return "The total count of intruders in range " + str(t1) + " and " + str(t2) + " is " + str(count)

@app.route('/getIntrudersNext')
def getIntrudersNext():
    t1 = str(request.values.get("t1"))
    t2 = str(request.values.get("t2"))

    t1 = t1.replace("T"," ") + ":00"
    t1 = datetime.strptime(t1, "%Y-%m-%d %I:%M:%S")

    t2 = t2.replace("T"," ") + ":00"
    t2 = datetime.strptime(t2, "%Y-%m-%d %I:%M:%S")

    intruder_id_list = UserQuery.get_intruders(t1,t2)

    return render_template('getIntruders.html', list=True, idlist=intruder_id_list, t1=t1, t2=t2)

@app.route('/getVideoClips')
def getVideoClipsFirst():
    t1 = str(request.values.get("t1"))
    t2 = str(request.values.get("t2"))
    intruderid = request.values.get("intid")

    video_clips_list = UserQuery.get_intruder_video_clips(intruderid,t1,t2)

    #print str(video_clips_list)

    return render_template('getVideoClips.html', t1=t1, t2=t2, intid=intruderid, video_list = video_clips_list)

@app.route('/getVideoClipsNext')
def getVideoClipsNext():
	print "hello"
	print request.values

	t1 = request.values.get("t1")
	t2 = request.values.get("t2")

	print "inside"
	try:
		# Input format: YYYY-mm-DDTHH:MM
		t1 = t1.replace('T', ' ').replace('Z', '')
		t1 += ":00"

		t2 = t2.replace('T', ' ').replace('Z', '')
		t2 += ":00"

		clips = UserQuery.get_video_clips(t1,t2)
		''''
		for clip in clips:
			print "The video clip id: {} start time: {} end time: {} ".format(clip.file_path,clip.start_time,clip.end_time)
		'''

		return render_template('displayVideoClips.html', list=True, idlist=clips)

	except Exception as e:
		logging.exception("Error while processing")

@app.route('/displayImage')
def displayImage():
	id = request.values.get("path")
	file_path = "/intruder_profiles/cropFrame_{}.jpg".format(id)
	return render_template('displayImage.html',path=file_path)

@app.route('/playVideo')
def playVideo():
	path = str(request.values.get("path"))
	return render_template('playVid.html', path=path)

@app.route('/video_clips/<file>')
def send_video_file(file):
	print "Inside send_video_file"
	try:
		file_path = "static/video_clips/{}".format(file)

		with open(file_path, "rb") as bites:
			return send_file(io.BytesIO(bites.read()), mimetype="video/mp4")
		#return redirect("/static/video_clips/{}?adf=we".format(file))
	except Exception as e:
		logging.exception("Error while sending mp4 file")


if __name__ == '__main__':
   app.run()
