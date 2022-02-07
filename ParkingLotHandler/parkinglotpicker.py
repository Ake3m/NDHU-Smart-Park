from ast import Break
import cv2 as cv
import json
import pyrebase

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


width = 120  # sets width of 1 parking space
height = 265  # sets height of 1 parking space



# function responsible for drawing parking space on mouse click
def outlineParkingSpace(events, x, y, flags, parameters):
    if events == cv.EVENT_LBUTTONDOWN:  # if left click area, add that point to the list
        position_list.append((x, y))
    if events == cv.EVENT_RBUTTONDOWN:  # if right click, remove point from list
        for i, position in enumerate(position_list):
            x1, y1 = position
            if x1 < x < x1+width and y1 < y < y1+height:
                position_list.pop(i)
    with open("parkinglots.json", "w") as outfile:
        json.dump(position_list, outfile)

    

if __name__ == '__main__':
    try:
        #tries to load the data from a json file
        with open("parkinglots.json", 'r') as infile: 
            position_list = json.load(infile)
    except:
        # initializes empty position list for parking spaces if no such json file exists
        position_list = []
    while True:
        img = cv.imread("./sample4.jpg")  # open sample
        # cv.rectangle(img, (110,160), (110 + 120, 160 + 270), (0,255,0))
        # draw initial retangle to first rest how to set up the width and height
        for position in position_list:  # draws all the rectangles
            cv.rectangle(img, tuple(position), (position[0] + width, position[1]+height), (0, 255, 0), 2)
        cv.imshow("Test", img)
        cv.setMouseCallback("Test", outlineParkingSpace)
        k=cv.waitKey(1)
        if k == ord('q'):
            break
    storage.child("parkinglots.json").put("parkinglots.json")
