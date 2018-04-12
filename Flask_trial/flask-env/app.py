from flask import Flask,render_template,json, request,redirect,url_for, jsonify
<<<<<<< HEAD
from userQuery import UserQuery
from datetime import datetime
=======
from datetime import datetime
import logging

from userQuery import UserQuery
>>>>>>> a7ae82dac1ff1a878105103088b25013db65a4c7

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
    return render_template('getVideoClips.html')

@app.route('/intruderClips')
def intruderClipsFirst():
    return render_template('intruderClips.html')

@app.route('/getTotalCountNext')
def getTotalCountNext():
<<<<<<< HEAD
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

    intruder_list  = UserQuery.get_intruders(t1,t2)
    return "The list of intruders in the range " + str(t1) + " and " + str(t2) + " is :"
=======
	print "inside"
	
	print request.values
	
	print "after"
	t1 = request.values.get("t1")
	t2 = request.values.get("t2")
	
	print "T1: %s, T2: %s" % (t1,  t2)
	
	try:
		# Input format: YYYY-mm-DDTHH:MM
		t1 = t1.replace('T', ' ').replace('Z', '')
		t1 += ":00"
		
		t2 = t2.replace('T', ' ').replace('Z', '')
		t2 += ":00"
	
		count = UserQuery.get_intruder_count(t1,t2)
		return "The total count of intruders in range " + t1 + " and " + t2 + " is " + str(count)
	except Exception as e:
		logging.exception("Error while processing")

@app.route('/getIntrudersNext')
def getIntrudersNext():
     t1 = request.values.get(t1)
     t2 = request.values.get(t2)
     intruder_list  = getIntruders(t1,t2)
     return "The list of intruders in the range " + t1 + " and " + t2 + " is :"
>>>>>>> a7ae82dac1ff1a878105103088b25013db65a4c7

if __name__ == '__main__':
   app.run()
