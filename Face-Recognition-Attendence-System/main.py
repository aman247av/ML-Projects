import os
import cv2
import cvzone
import pickle
import numpy as np
import face_recognition
from variables import *
from datetime import datetime
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage
cred = credentials.Certificate("db-key.json")
firebase_admin.initialize_app(cred,{
    "databaseURL" : "https://face-attendance-system-e4038-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket" : "face-attendance-system-e4038.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,WIN_WIDTH)
cap.set(4,WIN_HEIGHT)

window_name = "Face Attendence System"  
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)  
cv2.moveWindow(window_name, X_POS, Y_POS) 

bg = cv2.imread('Resources/background.png')

modePath = 'Resources/Modes'
modeList = os.listdir(modePath)
imgModeList = []
for path in modeList:
    imgModeList.append(cv2.imread(os.path.join(modePath,path)))



modeType = 0

print('Loading Encode File...')
file = open('encodeFile.p','rb')
encodeListWithIds = pickle.load(file)
file.close()
encodedList, ids = encodeListWithIds
print('Loading Completed...')

counter = 0
id = -1
imgEmp = []


while True:
    success, frame = cap.read()

#model
    imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)


    bg[162:162+WIN_HEIGHT, 55:55+WIN_WIDTH] = frame
    bg[X_PANEL:X_PANEL + 633, Y_PANEL:Y_PANEL + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodedList, encodeFace)
            faceDis = face_recognition.face_distance(encodedList, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(ids[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBG = cvzone.cornerRect(bg, bbox, rt=0)
                id = ids[matchIndex]
                if key == 13:
                    cvzone.putTextRect(imgBG, "Loading", (275, 400))
                    cv2.imshow(window_name, imgBG)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 2

        if counter != 0:

            if counter == 1:
                # Get the Data
                info = db.reference(f'Employees/{id}').get()
                print(info)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(info['last_login'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Employees/{id}')
                    info['total_attendance'] += 1
                    ref.child('total_attendance').set(info['total_attendance'])
                    ref.child('last_login').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 1
                    counter = 0
                    imgBG[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    


            if modeType != 1:

                if 30 < counter < 40:
                    modeType = 3

                imgBG[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 30:
                    cv2.putText(imgBG, str(info['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBG, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBG, str(info['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBG, str(info['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBG[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 30:
                    counter = 0
                    modeType = 0
                    info = []
                    imgStudent = []
                    imgBG[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    
    
    cv2.imshow(window_name, bg)
    # time.sleep(2)


    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
