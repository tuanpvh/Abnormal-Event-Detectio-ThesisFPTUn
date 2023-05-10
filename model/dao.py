import sqlite3
import json
from model import model
from datetime import datetime
# con.commit()

class UserDao:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def get_user_by_email(self, email, password):
        ems = self.cur.execute("SELECT * FROM User WHERE email = '{}' and pwd='{}' and dl_fg = 0".format(email, password))
        ems = ems.fetchall()
        if len(ems)!=1:
            return None
        print(ems[0])
        return model.User(ems[0][0], ems[0][1], ems[0][2], ems[0][3], ems[0][4], ems[0][5]).__dict__

    def insert_new_user(self, email, pwd, first_name, last_name):
        sql_query = "INSERT INTO User(email, pwd, first_name, last_name, dl_fg) VALUES('{}', '{}', '{}', '{}', 0)".format(
                                                                                    email, pwd, first_name, last_name)
        self.cur.execute(sql_query)
        self.con.commit()
        return True

class CameraDao:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def get_camera_by_userid(self, user_id):
        cams = self.cur.execute("SELECT * FROM Camera WHERE UserID = '{}' and dl_fg = 0".format(user_id))
        cams = cams.fetchall()
        list_cam = []
        if len(cams)==0:
            return None
        for cam in cams:
            list_cam.append(model.Camera(cam[0], cam[1], cam[2], cam[3], cam[4], cam[5]))
        
        return [ob.__dict__ for ob in list_cam]
    
    def get_camera_name_by_camid(self, camid):
        cams = self.cur.execute("SELECT * FROM Camera WHERE CameraID = '{}' and dl_fg = 0".format(camid))
        cams = cams.fetchall()
        list_cam = []
        if len(cams)==0:
            return None
        for cam in cams:
            list_cam.append(model.Camera(cam[0], cam[1], cam[2], cam[3], cam[4], cam[5]))
        
        return [ob.__dict__ for ob in list_cam]

    def get_user_id_by_camid(self, camid):
        user_id = self.cur.execute("SELECT UserID FROM Camera WHERE CameraID = '{}' and dl_fg = 0".format(camid))
        user_id = user_id.fetchall()
        if user_id is None:
            return None
        
        return user_id[0]

    def insert_new_camera(self, user_id, ip_address, cam_pwd, camera_name):
        sql_query = "INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES('{}', '{}', '{}', '{}', 0)".format(
                                                                                    user_id, ip_address, cam_pwd, camera_name)
        self.cur.execute(sql_query)
        self.con.commit()
        return True
    
    def remove_camera(self, cam_id):
        sql_query = "UPDATE Camera SET dl_fg=1 WHERE CameraID='{}'".format(cam_id)
        self.cur.execute(sql_query)
        self.con.commit()
        return True

class EventDao:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()
    
    def get_events_by_camid(self, cam_id, wrong = 0):
        if not wrong:
            events = self.cur.execute("SELECT * FROM Event WHERE cam_id = '{}'".format(cam_id))
        else:
            events = self.cur.execute("SELECT * FROM Event WHERE cam_id = '{}' and true_predict=0".format(cam_id))
            
        events = events.fetchall()
        list_events = []
        if len(events)==0:
            return None
        for evt in events:
            list_events.append(model.Event(evt[0], evt[1], evt[2], evt[3], evt[4], evt[5]))

        return [ob.__dict__ for ob in list_events]

    def get_all_events(self, user_id):
        cam_dao = CameraDao(self.con)
        print(user_id)
        cams = cam_dao.get_camera_by_userid(int(user_id))
        print(cams)
        all_events = []
        if cams is None:
            return None
        for cam in cams:
            list_events = self.get_events_by_camid(cam['cam_id'])
            if list_events is not None:
                all_events.append(list_events)
        
        return all_events

    def get_all_wrong_events(self, user_id):
        cam_dao = CameraDao(self.con)
        print(user_id)
        cams = cam_dao.get_camera_by_userid(int(user_id))
        print(cams)
        all_events = []
        if cams is None:
            return None
        for cam in cams:
            list_events = self.get_events_by_camid(cam['cam_id'], wrong = 1)
            if list_events is not None:
                all_events.append(list_events)
        
        return all_events
    
    def insert_event(self, cam_id, message, video_path=None):
        sql_query = "INSERT INTO Event(cam_id, message, datetime, video_path) VALUES('{}', '{}', '{}', '{}')".format(
                                                                                    cam_id, message, str(datetime.now()), video_path)
        self.cur.execute(sql_query)
        self.con.commit()
        return True

    def update_true_pred(self, event_id, result):
        sql_query = "UPDATE Event SET true_predict={} WHERE event_id='{}'".format(result, event_id)
        self.cur.execute(sql_query)
        self.con.commit()
        return True

class EmailDAO:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def insert_email(self, UserID, Email, dl_fg=0):
        sql_query = "INSERT INTO Email(UserID, Email, dl_fg) VALUES('{}', '{}', '{}')".format(
                                                UserID, Email, dl_fg)
        self.cur.execute(sql_query)
        self.con.commit()
        return True
    
    def get_email_by_user_id(self, user_id):
        emails = self.cur.execute("SELECT * FROM Email WHERE UserID = '{}'".format(user_id))
        emails = emails.fetchall()
        list_emails = []
        if len(emails)==0:
            return None
        for eml in emails:
            list_emails.append(model.Email(eml[0], eml[1], eml[2], eml[3]))

        return [ob.__dict__ for ob in list_emails]
    
    def get_email(self, email, user_id):
        emails = self.cur.execute("SELECT Email FROM Email WHERE Email = '{}' and UserID = '{}'".format(email, user_id))
        emails = emails.fetchall()
        list_emails = []
        if len(emails)==0:
            return None
       
        return [ob.__dict__ for ob in list_emails]
    
    def checkEmail(self, email):
        email = self.cur.execute("SELECT * FROM Email WHERE Email = '{}'".format(email))
        email = email.fetchall()
        if email is None:
            return 0
        if len(email) == 0:
            return 0
        else:
            return 1

class HistoryDAO:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()
    
    def get_history_by_path(self, FilePath):
        history_videos = self.cur.execute("SELECT * FROM CameraHistory WHERE FilePath = '{}'".format(FilePath))
        history_videos = history_videos.fetchall()
        list_history_videos = []
        if len(history_videos)==0:
            return None
        for his in history_videos:
            list_history_videos.append(model.HistoryCamera(his[0], his[1], his[2], his[3]))

        return [ob.__dict__ for ob in list_history_videos]
    
    def get_history_by_cam_id(self, cam_id):
        history_videos = self.cur.execute("SELECT * FROM CameraHistory WHERE CameraID = '{}'".format(cam_id))
        history_videos = history_videos.fetchall()
        list_history_videos = []
        if len(history_videos)==0:
            return None
        for his in history_videos:
            list_history_videos.append(model.HistoryCamera(his[0], his[1], his[2], his[3]))

        return [ob.__dict__ for ob in list_history_videos]
    
    def get_all_history(self, user_id):
        cam_dao = CameraDao(self.con)
        print(user_id)
        cams = cam_dao.get_camera_by_userid(int(user_id))
        print(cams)
        all_his = []
        if cams is None:
            return None
        for cam in cams:
            list_his = self.get_history_by_cam_id(cam['cam_id'])
            print(list_his)
            all_his.append(list_his)
        
        return all_his        
        #     self.CameraHistoryID = CameraHistoryID
        # self.CameraID = CameraID
        # self.FilePath = FilePath
        # self.datetime = datetime
    def insert_history(self, CameraID, FilePath, create_time):
        sql_query = "INSERT INTO CameraHistory(CameraID, FilePath, datetime) VALUES('{}', '{}', '{}')".format(
                                                CameraID, FilePath, create_time)
        self.cur.execute(sql_query)
        self.con.commit()
        return True
