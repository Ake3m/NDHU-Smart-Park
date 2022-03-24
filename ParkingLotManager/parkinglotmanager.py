import cv2 as cv
import numpy as np
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

#previous width and height
# width = 120
# height = 265
#new width and height
width = 110
height=230
previous_list=[]

# setting up firebase admin
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'smart-park-13acd.appspot.com'})
db = firestore.client()
bucket=storage.bucket()


def checkParkingSpaces(processed_image):
    spaceCounter = 0
    global previous_list
    previous_list=vacant_lots.copy()


    for i, position in enumerate(position_list):
        x, y = position
        cropped_img = processed_image[y:y+height, x:x+width]
        count = cv.countNonZero(cropped_img)

        if count < 2000:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            vacant_lots[i] = True
        else:
            color = (0, 0, 255)
            thickness = 5
            vacant_lots[i] = False
            print(vacant_lots)
        cv.rectangle(
            img, position, (position[0]+width, position[1]+height), color, thickness)
        if vacant_lots != previous_list:
            previous_list=vacant_lots.copy()
            db_ref.update({'lot': vacant_lots})
            print("Updated")


if __name__ == '__main__':
    try:
        blob = bucket.blob("parkinglots.json") #puts the file parkinglots.json as a blob
        blob.download_to_filename("./ParkingLotMonitor/positionlist.json") #downloads blob to filename
        with open('./ParkingLotMonitor/positionlist.json', 'r') as infile:
            position_list = json.load(infile)
            vacant_lots = [True for lot in position_list]
            print(vacant_lots)
        db_ref = db.collection('Car').document('test')
        # db_ref.update({'lots': vacant_lots})

    except:
        print("OOF")
        position_list = []
        
    # gets access to webcam -- change to 0 for onboard camera
    cap = cv.VideoCapture(1)
    if not cap.isOpened():
        print("Error opening camera")
        exit()
    while True:
        flag, img = cap.read()
        grayscaleImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgBlur = cv.GaussianBlur(grayscaleImg, (3, 3), 1)
        imgThreshold = cv.adaptiveThreshold(
            imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv.dilate(imgMedian, kernel, iterations=1)
        checkParkingSpaces(imgDilate)

        cv.imshow("Feed", img)
        k=cv.waitKey(100)
        if k==ord('q'): #press q to quit
            break
        