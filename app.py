from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import pose_correction
# import logging

# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
socketio = SocketIO(app)

def cal_angle(a,b,c):
    radians = np.arctan2(c.y-b.y, c.x-b.x) - np.arctan2(a.y-b.y, a.x-b.x)
    angle = np.abs(radians*180.0/np.pi)
    if angle>180.0:
        angle = 360-angle
    return angle




@socketio.on('update_text')
def update_text():
    # Receive data from the client
    # new_text = data['text']

    # Broadcast the new text to all connected clients
    socketio.emit('text-update', {'text': (correctness_checklist)})

# scheduler.add_interval_job(update_text, seconds=5)


correctness_checklist = []

def video_stream():
  cap = cv2.VideoCapture(0)  # Use 0 for default camera

  pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

  global correctness_checklist

  while True:
      ret, frame = cap.read()
      if not ret:
          break


      # Recolor image to RGB
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      frame.flags.writeable = False

      try:
      # Perform pose detection here using MediaPipe
        results = pose.process(frame)

        landmarks = results.pose_landmarks.landmark
        # print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
        # break


        # Recolor back to BGR
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # print('something', end='')
        try:
            landmarks = results.pose_landmarks.landmark

            correctness_checklist = pose_correction.generate_remarks(landmarks)
            try:
              socketio.emit('text-update', {'text': (correctness_checklist)})
            except Exception as e:
              # Handle other types of exceptions
              print(f"An error occurred: {e}")

            # print("correctness_checklist : ", correctness_checklist)
            # handle_update_text(str(correctness_checklist))
            # print("naa : ", correctness_checklist)
            
            # logging.debug('correctness_checklist: ', correctness_checklist)

            shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

            # calculate angle
            angle = cal_angle(shoulder, elbow, wrist)
            
            # print(elbow[:2])

            elbow = [ landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            # print('el', elbow)

            # visualize
            cv2.putText(frame, str(angle), 
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
        except:
          pass

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  # mp_drawing.DrawingSpec(color=(245,0,0), thickness=2, circle_radius=2), 
                                  # mp_drawing.DrawingSpec(color=(0,66,0), thickness=2, circle_radius=2) 
                                  ) 
      except:
        pass

      # Display the frame
      ret, jpeg = cv2.imencode('.jpg', frame)
      frame = jpeg.tobytes()
      yield (b'--frame\r\n'
             b'Content-Type: frame/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
      

  cap.release()





@app.route('/')
def home_page():
  return render_template('home.html')


@app.route('/video')
def video():
   return render_template('video_stream.html')


@app.route('/video_feed')
def video_feed():
  # print("correctness_checklist 2: ", correctness_checklist)
  # print("hey", correctness_checklist)
  return Response(video_stream(),
    mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
  # app.run(debug=True)
  socketio.run(app, debug=True)
