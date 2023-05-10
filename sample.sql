CREATE TABLE `Camera`(
	`CameraID` INTEGER PRIMARY KEY AUTOINCREMENT,
	`UserID` int NOT NULL,
	`ip_address` varchar(100) NOT NULL,
	`cam_pwd` varchar(100) NOT NULL,
    `camera_name` varchar(255) NOT NULL,
    `dl_fg` int NOT NULL
);
/****** Object:  Table `EmailList`    Script Date: 1/19/2023 1:01:23 AM ******/


CREATE TABLE `Email`(
	`EmailID` INTEGER PRIMARY KEY AUTOINCREMENT,
	`UserID` int NOT NULL,
	`Email` varchar(50) NULL,
    `dl_fg` int NOT NULL
);
/****** Object:  Table `Event`    Script Date: 1/19/2023 1:01:23 AM ******/
CREATE TABLE `Event`(
	`event_id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`cam_id` int NOT NULL,
	`message` varchar(255) NULL,
	`datetime` datetime NOT NULL,
    `true_predict` int NULL,
	`video_path` varchar(255) NULL
);
/****** Object:  Table `Help`    Script Date: 1/19/2023 1:01:23 AM ******/


CREATE TABLE `Help`(
	`HelpID` INTEGER PRIMARY KEY AUTOINCREMENT,
	`Answer` varchar(255) NULL,
	`Question` varchar(255) NULL
);
/****** Object:  Table `HistoryCamera`    Script Date: 1/19/2023 1:01:23 AM ******/


CREATE TABLE `CameraHistory`(
	`CameraHistoryID` INTEGER PRIMARY KEY AUTOINCREMENT,
	`CameraID` int NULL,
	`FilePath` varchar(255) NULL,
	datetime datetime NULL
);
/****** Object:  Table `User`    Script Date: 1/19/2023 1:01:23 AM ******/

CREATE TABLE `User`(
	`UserID` INTEGER PRIMARY KEY AUTOINCREMENT,
	`email` varchar(50) NOT NULL,
	`pwd` varchar(50) NOT NULL,
    `dl_fg` int NOT NULL,
	`first_name` varchar(50) NOT NULL,
	`last_name` varchar(50) NOT NULL
);

/****** End ******/

INSERT INTO User(email, pwd, dl_fg, first_name, last_name) VALUES('123@123.com', '1', 0, 'Hieu', 'Phan');
INSERT INTO User(email, pwd, dl_fg, first_name, last_name) VALUES('111@111.com', '1', 0, 'Ha', 'Pham');
INSERT INTO User(email, pwd, dl_fg, first_name, last_name) VALUES('121@212.com', '1', 0, 'Hieu', 'Phan');
INSERT INTO User(email, pwd, dl_fg, first_name, last_name) VALUES('ssa@123.com', '1', 0, 'Hieu', 'Phan');
INSERT INTO User(email, pwd, dl_fg, first_name, last_name) VALUES('vdss@123.com', '1', 0, 'Hieu', 'Phan');
INSERT INTO User(email, pwd, dl_fg, first_name, last_name) VALUES('6782@123.com', '1', 0, 'Hieu', 'Phan');
INSERT INTO User(email, pwd, dl_fg, first_name, last_name) VALUES('hka@123.com', '1', 0, 'Hieu', 'Phan');

INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES(0, '192.168.0.1','1', 'Yard', 0);
INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES(0, '192.168.0.1','1', 'Back Yard', 0);
INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES(0, '192.168.0.1','1', 'Living Room', 0);
INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES(0, '192.168.0.1','1', 'Roof Top', 0);
INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES(0, '192.168.0.1','1', 'Street', 0);
INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES(0, '192.168.0.1','1', 'Kitchen', 0);
INSERT INTO Camera(UserID, ip_address, cam_pwd, camera_name, dl_fg) VALUES(0, '192.168.0.1','1', 'Nothing', 0);

INSERT INTO Email(UserID, Email, dl_fg) VALUES('1', 'duchieuphan2k1@gmail.com', 0);
INSERT INTO Email(UserID, Email, dl_fg) VALUES('2', 'hieupndhe153303@fpt.edu.vn', 0);

INSERT INTO `Event`(`cam_id`, `message`, `datetime`, `true_predict`) VALUES(0, 'Warning: An Abnormal Event Occur', '2023-03-26 17:54:08.968915', NULL);
INSERT INTO `Event`(`cam_id`, `message`, `datetime`, `true_predict`) VALUES(1, 'Warning: An Abnormal Event Occur', '2023-03-26 18:54:08.968915', NULL);
INSERT INTO `Event`(`cam_id`, `message`, `datetime`, `true_predict`) VALUES(2, 'Warning: An Abnormal Event Occur', '2023-03-26 19:54:08.968915', NULL);
INSERT INTO `Event`(`cam_id`, `message`, `datetime`, `true_predict`) VALUES(3, 'Warning: An Abnormal Event Occur', '2023-03-26 20:54:08.968915', NULL);
INSERT INTO `Event`(`cam_id`, `message`, `datetime`, `true_predict`) VALUES(4, 'Warning: An Abnormal Event Occur', '2023-03-26 21:54:08.968915', NULL);

