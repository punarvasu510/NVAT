from flask import Flask,render_template,json, request,redirect,url_for, jsonify, send_file
from userQuery import UserQuery
from datetime import datetime
import logging
import os, io

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')
   #return "Novel Video Analytics and Tapestry"

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/getTotalCount')
def getTotalCount():
    t1 = str(request.values.get("t1"))
    t2 = str(request.values.get("t2"))

    t1 = t1.replace("T"," ") + ":00"
    t1 = datetime.strptime(t1, "%Y-%m-%d %I:%M:%S")

    t2 = t2.replace("T"," ") + ":00"
    t2 = datetime.strptime(t2, "%Y-%m-%d %I:%M:%S")

    count = UserQuery.get_intruder_count(t1,t2)
    return render_template('TotalCount.html', t1=str(t1), t2=str(t2), count=count)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/getIntruderProfiles')
def getIntruderProfiles():
    t1 = str(request.values.get("t1"))
    t2 = str(request.values.get("t2"))

    t1 = t1.replace("T"," ") + ":00"
    t1 = datetime.strptime(t1, "%Y-%m-%d %I:%M:%S")

    t2 = t2.replace("T"," ") + ":00"
    t2 = datetime.strptime(t2, "%Y-%m-%d %I:%M:%S")

    intruder_id_list = UserQuery.get_intruders(t1,t2)

    return render_template('IntruderProfiles.html', idlist=intruder_id_list, t1=t1, t2=t2)

@app.route('/getTapestry')
def getTapestry():
    t1 = str(request.values.get("t1"))
    t2 = str(request.values.get("t2"))
    intruderid = request.values.get("intid")

    video_clips_list = UserQuery.get_intruder_video_clips(intruderid,t1,t2)

    #print str(video_clips_list)

    return render_template('Tapestry.html', t1=t1, t2=t2, intid=intruderid, video_list = video_clips_list)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/getVideoClips')
def getVideoClips():
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

		for clip in clips:
			path = clip.file_path
			clip.file_path = path.replace("avi","mp4")
			print "The video clip id: {} start time: {} end time: {} ".format(clip.file_path,clip.start_time,clip.end_time)


		return render_template('displayVideoClips.html', list=True, idlist=clips)

	except Exception as e:
		logging.exception("Error while processing")

@app.route('/playVideo')
def playVideo():
	path = str(request.values.get("path"))
	return render_template('playVid.html', path=path)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
   app.run()
