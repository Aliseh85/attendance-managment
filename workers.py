import cv2
import numpy as np
import face_recognition as face_rec
import os
import attendance


def resize(img, size):
    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)


def findencoding(images):
    img_encodings = []
    for img in images:
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = face_rec.face_encodings(img)[0]
        img_encodings.append(encodeimg)
    return img_encodings


def start():
    path = 'workers_images'
    employee_img = []
    employee_name = []
    my_list = os.listdir(path)
    for cl in my_list:
        curimg = cv2.imread(f'{path}/{cl}')
        employee_img.append(curimg)
        employee_name.append(os.path.splitext(cl)[0])
    encode_list = findencoding(employee_img)

    vid = cv2.VideoCapture(0)
    while True:
        success, frame = vid.read()
        smaller_frames = cv2.resize(frame, (0, 0), None, 0.25, 0.25)

        faces_in_frame = face_rec.face_locations(smaller_frames)
        encode_faces_in_frame = face_rec.face_encodings(smaller_frames, faces_in_frame)

        for encodeFace, faceloc in zip(encode_faces_in_frame, faces_in_frame):
            matches = face_rec.compare_faces(encode_list, encodeFace)
            facedis = face_rec.face_distance(encode_list, encodeFace)
            print(facedis)
            match_index = np.argmin(facedis)

            if matches[match_index]:
                name = employee_name[match_index].upper()
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.rectangle(frame, (x1, y2 - 25), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance.MarkAttendence(name)
        cv2.waitKey(1)