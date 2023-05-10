class Camera:
    def __init__(self, cam_id, user_id, ip_address, cam_pwd, cam_name, dl_fg):
        self.cam_id = cam_id
        self.user_id = user_id
        self.ip_address = ip_address
        self.cam_pwd = cam_pwd
        self.cam_name = cam_name
        self.dl_fg = dl_fg
    
class Email:
    def __init__(self, EmailID, UserID, Email, dl_fg):
        self.EmailID = EmailID
        self.UserID = UserID
        self.Email = Email
        self.dl_fg = dl_fg
    
class Event:
    def __init__(self, event_id, cam_id, message, datetime, true_predict, video_path):
        self.event_id = event_id
        self.cam_id = cam_id
        self.message = message
        self.datetime = datetime
        self.true_predict = true_predict
        self.video_path = video_path


class Help:
    def __init__(self, help_id, answer, question):
        self.help_id = help_id
        self.answer = answer
        self.question = question

class HistoryCamera:
    def __init__(self, CameraHistoryID, CameraID, FilePath, datetime):
        self.CameraHistoryID = CameraHistoryID
        self.CameraID = CameraID
        self.FilePath = FilePath
        self.datetime = datetime


class Notification:
    def __init__(self, notification_id, cam_id, emailList_id, message):
        self.notification_id = notification_id
        self.cam_id = cam_id
        self.emailList_id = emailList_id
        self.message = message

class User:
    def __init__(self, user_id, email, pwd, dl_fg, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.pwd = pwd
        self.dl_fg = dl_fg
        self.first_name = first_name
        self.last_mame = last_name
        