from flask import Flask,render_template,json, request,redirect,url_for, jsonify
from another import foo

app = Flask(__name__)

list1 = [1,2,3,4,5,6,7,8]


@app.route('/',methods=['GET'])         # '/' is the first page of your website
def index():
    another = foo()
    return render_template('index.html',l1 = list1,string=another)     

"""
app.route specifies what URL the person has to go to use that functionality
'/' means first page tarun.com/ 
'/trial' is another page @ tarun.com/trial
"""

@app.route('/saveVideo',methods=['POST'])            # '/<insert anything>/' is to direct to another page of your website
def video_save():                                    # function name for each app.route has to be unique
    return render_template('video.html',play=False)

@app.route('/playVideo',methods=['POST'])         # '/<insert anything>/' is to direct to another page of your website
def video_play():                                # function name for each app.route has to be unique
    video_name = request.form["filename"]
    print(video_name)
    if video_name=="":
        return render_template('video.html',play=True,error=True)    
    return render_template('video.html',play=True,error=False,vname=video_name)


if __name__ == "__main__":
	app.run(debug=True)