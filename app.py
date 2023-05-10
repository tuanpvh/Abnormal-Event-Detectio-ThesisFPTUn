# app.py
from flask import (Flask, flash, Response, render_template, request, redirect, session, url_for)
from camera import VideoCamera
from flask_socketio import SocketIO, emit
from flask_mail import Mail, Message

import cv2
import os
from werkzeug.utils import secure_filename
import sqlite3
from model import dao
from random import randint
from datetime import datetime
from Abnormal_Event_Detection.model import load_model
from Abnormal_Event_Detection.start_live_feed import abnomaly_detect
from pred_upload import predict
import numpy as np 
from keras.models import load_model
app = Flask(__name__)
app.secret_key = 'ItShouldBeAnythingButSecret'     #you can set any secret key but remember it should be secret
socketio = SocketIO(app, cors_allowed_origins='*')
UPLOAD_FOLDER = 'static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'noreply.anocam@gmail.com'
app.config['MAIL_PASSWORD'] = 'bmauoewbrcndnuqt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def send_email(message, user_id):
    con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
    emails = dao.EmailDAO(con).get_email_by_user_id(user_id)
    emails_list = []
    for eml in emails:
        emails_list.append(eml['Email'])
        
    msg = Message('[Anocam] Automatic Warning', sender = 'noreply.anocam@gmail.com', recipients = emails_list)
    msg.body = message
    mail.send(msg)
    return 1

#step – 3 (creating a dictionary to store information about users)
def gen(camera, cam_id):
    modelpath="D:/Hoc tap/Do an/thesis_2023_fptu/Abnormal_Event_Detection/AnomalyDetector.h5"
    model=load_model(modelpath)
    frames = []
    saved_frames = []
    j = 0
    frameSize = (1280, 720)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    
    while True:
        frame, pframe = camera.get_frame()
        frames.append(pframe)
        saved_frames.append(pframe)        
        if len(saved_frames)==1000:
            out = cv2.VideoWriter('static/history/{}_{}.mp4'.format(cam_id, randint(0, 1000000)),
                            fourcc, float(20), frameSize)
            
            for fr in saved_frames:
                out.write(fr)    
            j+=1
            saved_frames=[]
            out.release()
        
        if len(frames) == 10:

            abn = abnomaly_detect(frames, model)
            if abn:
                con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
                cam_id = request.form['selected_cam']
                message = "Watch out! An abnormal event occurred"
                check = dao.EventDao(con).insert_event(cam_id, message)
                send_email(message, session['user']['user_id'])
            frames = []
            channel = "event_{}".format(cam_id)
            print(channel)
            socketio.emit(channel, {"time": str(datetime.now()), "anomaly": abn})
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/", methods = ['GET','POST'])
def blank():
    if 'user' in session:
        return redirect(url_for('home', cameras = session['cameras']))
    return redirect(url_for('login'))

@app.route("/home", methods = ['GET','POST'])
def home():
    con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
    if 'user' in session:
        user = session['user']
        print(session['cameras'])
        if 'camera' not in session:
            session['cameras'] = dao.CameraDao(con).get_camera_by_userid(user['user_id'])
            
        all_events = dao.EventDao(con).get_all_events(user['user_id'])
        session['all_events'] = all_events
        session['num_event'] = len(sum(all_events, [])) if all_events is not None else 0
        
        all_wrong_events = dao.EventDao(con).get_all_wrong_events(user['user_id'])
        print(all_wrong_events)
        session['num_wrong_event'] = len(sum(all_wrong_events, [])) if all_wrong_events is not None else 0
            
        print(session['user'])
        return render_template("home.html", cameras = session['cameras'])
    return redirect(url_for('login'))

@app.route("/login", methods = ['GET','POST'])
def login():
    con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)

    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')    
        user = dao.UserDao(con).get_user_by_email(username, password) 
        if user == None:
            return redirect(url_for('login'))
        else:
            session['user'] = user
            session['cameras'] = dao.CameraDao(con).get_camera_by_userid(user['user_id'])
            all_events = dao.EventDao(con).get_all_events(user['user_id'])
            session['events'] = all_events
            session['num_event'] = len(sum(all_events, [])) if all_events is not None else 0
            
            all_wrong_events = dao.EventDao(con).get_all_wrong_events(user['user_id'])
            session['num_wrong_event'] = len(sum(all_wrong_events, [])) if all_wrong_events is not None else 0
            return redirect(url_for('home', cameras = session['cameras']))    #if the username or password does not matches 

    session.clear()
    return render_template("login.html")

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        check_email = dao.EmailDAO(con).checkEmail(email)
        if check_email:
            return render_template("register.html", check_email=1)
        pwd = request.form.get('pwd')
        check = dao.UserDao(con).insert_new_user( email, pwd, first_name, last_name)
        user = dao.UserDao(con).get_user_by_email(email, pwd)
        user_id = user['user_id']
        insert_email = dao.EmailDAO(con).insert_email(user_id, email)
        if check:
            return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/add_camera", methods = ['POST'])
def add_camera():
    con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)

    ip_address = request.form.get('ip_address')
    cam_pwd = request.form.get('cam_pwd')
    camera_name = request.form.get('camera_name')
    check = dao.CameraDao(con).insert_new_camera(session['user']['user_id'], ip_address, cam_pwd, camera_name)
    if check:
        return redirect(url_for('home'))


@app.route("/events", methods=['GET','POST'])
def events():
    con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
    if 'user' in session:
        all_events = dao.EventDao(con).get_all_events(session['user']['user_id'])
        session['all_events'] = all_events
        return render_template("events.html", cameras = session['cameras'])
    return redirect(url_for('login'))

@app.route("/history", methods=['GET','POST'])
def history():
    con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
    if 'user' in session:
        history_vids = os.listdir('static/history')
        for vid in history_vids:
            create_time = os.path.getctime(os.path.join('static/history', vid))
            create_time = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
            FilePath = vid
            if ".mp4" in vid and dao.HistoryDAO(con).get_history_by_path(FilePath) is None:
                vid=vid.split('_')
                dao.HistoryDAO(con).insert_history(vid[1], FilePath, create_time)
                
        history_videos = dao.HistoryDAO(con).get_all_history(session['user']['user_id'])
        print(history_videos)
        
        return render_template("history.html", cameras = session['cameras'], history_videos=history_videos)
    return redirect(url_for('login'))

@app.route("/remove_camera", methods=['POST'])
def remove_camera():
    if 'user' in session:
        con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
        cam_id = request.form.get('cam_id')
        dao.CameraDao(con).remove_camera(cam_id)
        return redirect(url_for('home'))

    return redirect(url_for('home'))

@app.route("/update_true_pred", methods=['POST'])
def update_true_pred():
    if 'user' in session:
        con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
        event_id = request.form.get('event_id')
        true_pred = request.form.get('result')
        result = 0
        if true_pred == "Yes":
            result = 1
        dao.EventDao(con).update_true_pred(event_id, result)
        return redirect(url_for('events'))

    return redirect(url_for('events'))

@app.route("/upload", methods=['GET','POST'])
def upload():
    if 'user' in session:
        return render_template("upload.html", cameras=session['cameras'])

    return redirect(url_for('login'))


@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
        print(request.form['selected_cam'])
        filename = secure_filename(file.filename)

        saved_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(saved_filename)
        video_name = saved_filename.split("/")[-1].replace(".mp4", "")
        start_frame, end_frame = predict(video_name)
        
        if start_frame!=0:
            con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
            cam_id = request.form['selected_cam']
            message = """Watch out! An abnormal event occurred. Camera:{}.
            Time: {}
            """.format(cam_id, str(datetime.now()))
            check = dao.EventDao(con).insert_event(cam_id, message, video_name)
            send_email(message, session['user']['user_id'])
        #print('upload_video filename: ' + filename)
        flash('Video successfully analyzed, the abnormal event appeared: {}ms - {}ms'.format(start_frame, end_frame))
        return render_template('upload.html', filename=filename, cameras=session['cameras'], selected_cam=request.form['selected_cam'])

@app.route('/display/<filename>', methods=["POST", "GET"])
def display_video(filename):
    #print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display_history/<filename>', methods=["POST", "GET"])
def display_history_video(filename):
    #print('display_video filename: ' + filename)
    if 'user' in session:
        cam_id = filename.split("_")[1]
        con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
        user_id = dao.CameraDao(con).get_user_id_by_camid(cam_id)
        if user_id[0] == session['user']['user_id']:   
            return redirect(url_for('static', filename='history/' + filename), code=301)
        
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/setting", methods=['GET', 'POST'])
def setting():
    if 'user' in session:
        con = sqlite3.connect("Db_Doan1.db", check_same_thread=False)
        emails = dao.EmailDAO(con).get_email_by_user_id(
            session['user']['user_id'])
        if request.method == "POST":
            send_email = request.form['send_email']
            if not send_email:
                return render_template("setting.html", emails=emails, alert="Email not empty!")
            else:
                get_email = dao.EmailDAO(con).get_email(
                    send_email, session['user']['user_id'])
                if get_email is not None:
                    return render_template("setting.html", emails=emails, alert="Email is exists!")
                else:
                    check = dao.EmailDAO(con).insert_email(
                        session['user']['user_id'], send_email)
                    emails = dao.EmailDAO(con).get_email_by_user_id(
                        session['user']['user_id'])
                    return render_template("setting.html", emails=emails, alert="Add Email sucsess!")
        return render_template("setting.html", emails=emails)
    return redirect(url_for('login'))

@app.route('/video_feed/<cam_id>', methods = ['GET','POST'])
def video_feed(cam_id):
    video_stream = VideoCamera()
    return Response(gen(video_stream, cam_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.modified = True
    return redirect(url_for('login'))

if __name__ == "__main__":
    socketio.run(app, debug=True)