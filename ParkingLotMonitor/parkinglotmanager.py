import cv2 as cv
import numpy as np
import pyrebase
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

width = 120
height = 265

#firebase setup section
firebaseConfig={
    "apiKey": "AIzaSyAlrU3HO6rLkpp2e8miG3MUkklVfH0y1GU",
  "authDomain": "smart-park-13acd.firebaseapp.com",
  "databaseURL": "https://smart-park-13acd-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "smart-park-13acd",
  "storageBucket": "smart-park-13acd.appspot.com",
  "messagingSenderId": "524600567382",
  "appId": "1:524600567382:web:448bc11ef6b98106d33df7",
  "measurementId": "G-TVB91EHSG8"
}

firebase = pyrebase.initialize_app(firebaseConfig)


#setting up storage
storage = firebase.storage() 

#setting up firebase admin
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

def checkParkingSpaces(processed_image):
    spaceCounter = 0

    for i,position in enumerate(position_list):
        x,y = position
        cropped_img = processed_image[y:y+height, x:x+width]
        count = cv.countNonZero(cropped_img)

        if count < 2000:
            color = (0,255,0)
            thickness = 5
            spaceCounter+=1
            vacant_lots[i]=True
        else:
            color = (0,0,255)
            thickness = 5
            vacant_lots[i] = False
            print(vacant_lots)
        cv.rectangle(img, position, (position[0]+width, position[1]+height), color, thickness)
        db_ref.update({'lots': vacant_lots})

if __name__ == '__main__':
    try:
        print("Hello")
        storage.child("parkinglots.json").download("./ParkingLotMonitor/positionlist.json")
        # time.delay(5) #wait for 5 seconds then open the file
        with open('./ParkingLotMonitor/positionlist.json','r') as infile:
            position_list = json.load(infile)
            vacant_lots = [True for lot in position_list]
            print(vacant_lots)
        db_ref = db.collection('test').document('BoTkaJw3GdL7rdkusTRR')

        db_ref.update({'lots': vacant_lots})
    except:
        print("OOF")
        position_list=[]

    cap = cv.VideoCapture(1) #gets access to webcam -- change to 0 for onboard camera
    if not cap.isOpened():
        print("Error opening camera")
        exit()
    while True:
        flag, img = cap.read()
        grayscaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgBlur = cv.GaussianBlur(grayscaleImg, (3,3),1)
        imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25,16)
        imgMedian = cv.medianBlur(imgThreshold, 5)
        kernel = np.ones((3,3), np.uint8)
        imgDilate = cv.dilate(imgMedian, kernel, iterations=1)
        checkParkingSpaces(imgDilate)

        cv.imshow("FeeD", img)
        cv.waitKey(10)

