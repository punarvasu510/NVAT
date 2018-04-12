from flask import Flask,render_template,json, request,redirect,url_for, jsonify
import userQuery.py

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
    t1 = request.values.get("t1")
    t2 = request.values.get("t2")
    count = getTotalCount(t1,t2)
    return "The total count of intruders in range " + t1 + " and " + t2 + " is " + count

@app.route('/getIntrudersNext')
def getIntrudersNext():
     t1 = request.values.get("t1")
     t2 = request.values.get("t2")
     intruder_list  = getIntruders(t1,t2)
     return "The list of intruders in the range " + t1 + " and " + t2 + " is :"

if __name__ == '__main__':
   app.run()
