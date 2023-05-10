import cv2
import numpy as np
import glob



for filename in glob.glob('/Users/phanduchieu/Desktop/thesis_2023_fptu/static/history/cam_10_2023-04-11-01-34-08/*.jpg'):
    img = cv2.imread(filename)
    out.write(img)

out.release()