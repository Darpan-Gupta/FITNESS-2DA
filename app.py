from flask import Flask, render_template, Response, request, send_file, redirect, url_for
from flask_socketio import SocketIO, emit
# import cv2
# import mediapipe as mp
# import numpy as np
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

pose = 'left_tree'
import pose_detection


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/', methods = ['GET', 'POST'])
def home():

  return render_template('index.html')



@app.route('/description', methods = ['GET', 'POST'])
def description():


  if request.method == 'POST':
    global pose
    try:
      pose = request.json['pose']
    except:
      print('##################   error in getting pose from home')


  return render_template('description.html')


@app.route('/pose-detection', methods = ['GET', 'POST'])
def posedetection():

  return render_template('pose-detection.html')
  
  # else:
    



# @app.route('/video', methods = ['GET', 'POST'])
# def video():

#   if request.method == 'POST':
#     global pose
#     try:
#       pose = request.json['pose']
#     except:
#       print('##################   error in getting pose from home')

#   return render_template('video_stream.html')



@app.route('/video_feed')
def video_feed():
  
  if pose == None:
    print("################## error, pose not defined in video_feed")

  return Response(pose_detection.video_stream(app, pose),
    mimetype='multipart/x-mixed-replace; boundary=frame'
    )




if __name__ == '__main__':
  app.run(debug=True)
  # socketio.run(app, debug=True)
