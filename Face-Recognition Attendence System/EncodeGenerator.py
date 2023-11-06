import cv2
import os
import face_recognition
import pickle
from AddDataToDB import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage


imgPath = 'Images'
imgPathList = os.listdir(imgPath)

imgList = []
ids=[]

for path in imgPathList:
    imgList.append(cv2.imread(os.path.join(imgPath,path)))
    ids.append(os.path.splitext(path)[0])

    fileName = f'{imgPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)



def findEncodings(imgList):
    encodeList = []

    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

print("Encoding Started...")
encodedList = findEncodings(imgList)
encodedListwithIds = [encodedList, ids]
print("Encoding Complete...")

file = open('encodeFile.p','wb')
pickle.dump(encodedListwithIds, file)
file.close()
print('File Saved...')