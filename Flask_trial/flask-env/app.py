from flask import Flask,render_template,json, request,redirect,url_for, jsonify
from userQuery import UserQuery
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def test():
   return "Novel Video Analytics and Tapestry"

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/getTotalCount')
def getTotalCountFirst():
    return render_template('getTotalCount.html')

@app.route('/getIntruders')
def getIntrudersFirst():
    return render_template('getIntruders.html')

@app.route('/getVideoClips')
def getVideoClipsFirst():
    t1 = str(request.values.get("t1"))
    t2 = str(request.values.get("t2"))
    intruderid = request.values.get("intid")

    video_clips_list = UserQuery.get_intruder_video_clips(intruderid,t1,t2)

    #print str(video_clips_list)

    return render_template('getVideoClips.html', t1=t1, t2=t2, intid=intruderid, video_list = video_clips_list)

@app.route('/intruderClips')
def intruderClipsFirst():
    return render_template('intruderClips.html')

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


if __name__ == '__main__':
   app.run()
