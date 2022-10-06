# Creating database
# It captures images and stores them in datasets
# folder under the folder name of sub_data
import tkinter as tk
from tkinter import simpledialog
import cv2, sys, numpy, os
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
haar_file = haar_model

# All the faces data will be
#  present this folder
datasets = 'faces'

# These are sub data sets of folder,
# for my faces I've used my name you can
# change the label here
ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
sub_data = simpledialog.askstring(title="loading new employee",
                                  prompt="What's your Name?:")

path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
    os.mkdir(path)

# defining the size of images
(width, height) = (180, 150)

# '0' is used for my webcam,
# if you've any other camera
#  attached use '1' like this
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)

# The program loops until it has 30 images of the face.
count = 1
while count < 21:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 2)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 255), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width+10, height+10))
        cv2.imwrite('% s/% s.png' % (path, count), face_resize)
    count += 1

    cv2.imshow('recognizing your face', im)
    key = cv2.waitKey(10)
    if key == 27:
        break

