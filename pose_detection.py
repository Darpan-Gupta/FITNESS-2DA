import pyttsx3
import pose_correction
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# initialisation
engine = pyttsx3.init()


# import logging


def cal_angle(a, b, c):
    radians = np.arctan2(c.y-b.y, c.x-b.x) - np.arctan2(a.y-b.y, a.x-b.x)
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle


def video_stream(app, pose_name, side_faced_pose):

    socketio = SocketIO(app)

    cap = cv2.VideoCapture(0)  # Use 0 for default camera

    pose = mp_pose.Pose(min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)

    global correctness_checklist

    while True:
        ret, frame = cap.read()
        if not ret:
            print('error in reading camera')
            break

        # Recolor image to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False

        try:
            # Perform pose detection here using MediaPipe
            results = pose.process(frame)

            # Recolor back to BGR
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # print('something', end='')
            try:
                landmarks = results.pose_landmarks.landmark

                try:
                    global correctness_checklist
                    correctness_checklist = pose_correction.generate_remarks(
                        landmarks, pose_name, side_faced_pose)
                except:
                    print(
                        '########### Error in genrating correctness checklist in pose_detection.py')
                try:
                    socketio.emit(
                        'text-update', {'text': (correctness_checklist)})
                    for i in correctness_checklist:
                        engine.say(i)
                        # engine.run
                except Exception as e:
                    # Handle other types of exceptions
                    print(f"An error occurred: {e}")

                {  # print("correctness_checklist : ", correctness_checklist)
                    # handle_update_text(str(correctness_checklist))
                    # print("naa : ", correctness_checklist)

                    # logging.debug('correctness_checklist: ', correctness_checklist)

                    # shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                    # elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
                    # wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

                    # # calculate angle
                    # angle = cal_angle(shoulder, elbow, wrist)

                    # # print(elbow[:2])

                    # elbow = [ landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    # # print('el', elbow)

                    # # visualize
                    # cv2.putText(frame, str(angle),
                    #             tuple(np.multiply(elbow, [640, 480]).astype(int)),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                }

            except:
                pass

            if correctness_checklist[0] == 'Correct Pose!!':
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(245, 0, 0), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(
                                              color=(0, 250, 0), thickness=5, circle_radius=2)
                                          )
            else:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          # mp_drawing.DrawingSpec(color=(245,0,0), thickness=2, circle_radius=2),
                                          # mp_drawing.DrawingSpec(color=(0,250,0), thickness=5, circle_radius=2)
                                          )
        except:
            pass

        # invert the frame
        frame = cv2.flip(frame, 1)

        # Display the frame
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: frame/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()
