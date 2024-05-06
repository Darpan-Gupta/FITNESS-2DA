import pose_detection
from flask import Flask, render_template, Response, request, send_file, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_mysqldb import MySQL
import authorization
from db import get_db
import pose_data


# import cv2
# import mediapipe as mp
# import numpy as np
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# pose = 'left_tree'


app = Flask(__name__)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.secret_key = "new_secret_key"
app.debug = True

db = get_db()


class User(UserMixin):
    def __init__(self, email):
        self.email = email

    def get_id(self):
        return self.email


@login_manager.user_loader
def load_user(email):
    user = db.users.find_one({"email": email})

    if not user:
        return None
    return User(email=user['email'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # print(request.args.to_dict())

        print("login: ",  email, password)

        message = authorization.login(email, password)
        flash(message)
        print(message)

        if message == "Successfully logged in":
            user = User(email=email)
            login_user(user, remember=True)
            print("logiin successssss")

            print(request.form.get("next"))
            next_page = request.form.get('next')
            print(next_page, " adsffa ")

            return redirect(next_page or url_for('home'))

        else:
            return render_template("login.html")

    return render_template('login.html')


@app.route('/register', methods=['GET', "POST"])
def register():
    # if "email" in session:
    #     return "allready logged in"

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        age = request.form.get("age")
        weight = request.form.get("weight")

        print(name, email, password, confirm_password, age, weight)

        message = authorization.register(
            name, email, password, confirm_password, age, weight)
        print(message)
        flash(message)

        if message == "Successfuly registered":
            user = User(email=email)
            login_user(user, remember=True)
            return url_for("home")

        else:
            return render_template("register.html")

    return render_template("register.html")


@app.route('/logout', methods=['GET', "POST"])
@login_required
def logout():
    # if "email" in session:
    #     session.pop("email", None)
    logout_user()

    return "logged out"


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/description', methods=['GET', 'POST'])
def description():

    if request.method == 'POST':
        global pose
        try:
            pose = request.json['pose']
        except:
            print('##################   error in getting pose from home')

    return render_template('description.html')


@app.route('/pose-detection', methods=['GET', 'POST'])
@login_required
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


@app.route('/video_feed', methods=['GET', 'POST'])
@login_required
def video_feed():

    if pose == None:
        print("################## error, pose not defined in video_feed")

    # camera = None
    # if request.method == 'POST':

    side_faced_pose = False

    if pose in pose_data.side_faced_poses:
        side_faced_pose = True

    return Response(pose_detection.video_stream(app, pose, side_faced_pose),
                    mimetype='multipart/x-mixed-replace; boundary=frame'
                    )


if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)
