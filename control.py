import pickle
import tkinter as tk
from tkinter import simpledialog
import cv2
import face_recognition
import os
import pandas as pd
from imutils import paths


def savefaceimg():
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

    # '0' is used for my webcam
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)

    # The program loops until it has 20 images of the face.
    count = 1
    while count < 21:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 2)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 255), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width + 10, height + 10))
            cv2.imwrite('% s/% s.png' % (path, count), face_resize)
        count += 1

        cv2.imshow('recognizing your face', im)
        key = cv2.waitKey(10)
        if key == 27:
            break


def savefaceencode():
    # get paths of each file in folder named Images
    # Images here contains my data(folders of various persons)
    image_paths = list(paths.list_images('faces'))
    known_encodings = []
    known_names = []
    knownNamesGoogle = []
    # loop over the image paths
    for (i, imagePath) in enumerate(image_paths):
        # extract the person name from the image path
        name = imagePath.split(os.path.sep)[-2]
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Use Face_recognition to locate faces
        boxes = face_recognition.face_locations(rgb, model='hog')
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name)
            if name not in knownNamesGoogle:
                knownNamesGoogle.append(name)
    # save emcodings along with their names in dictionary data
    data = {"encodings": known_encodings, "names": known_names}
    # use pickle to save data into a file for later use
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()

    dataframe = {'names': knownNamesGoogle, 'status': 0, 'timein': 0, 'timeout': 0}
    df = pd.DataFrame(dataframe)
