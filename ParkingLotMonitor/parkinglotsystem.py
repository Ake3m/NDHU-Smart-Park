import os
from pathlib import Path
import cv2 as cv
import numpy as np
from firebase_admin import initialize_app
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage


#GLOBAL VARIABLES SECTION
drawing = False
ix = 0 #initial x
iy = 0 #initial y
ex=0 #ending x
ey=0 #ending y
sample_img = ""
imgCopy=""
sample_points = [] #list holding the sample points 
position_list = [] #list holding the position of each lot
width=0
height=0

#FIREBASE CONFIGURATION SETUP
cred=credentials.Certificate("./serviceAccountKey.json")
initialize_app(cred, {'storageBucket': 'smart-park-13acd.appspot.com'})
database=firestore.client()

def draw(event, x, y, flags, parameters):
    global ix, iy, drawing, ex, ey
    if event == cv.EVENT_LBUTTONDOWN:
        ix = x
        iy = y
        drawing = True
    if event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.rectangle(imgCopy, (ix, iy), (x, y), (0, 255, 0), -1)
    if event == cv.EVENT_LBUTTONUP:
        drawing = False
        ex=x
        ey=y
        # sample_points.extend([ix,iy,x,y])
        


def outlineParkingSpace(events, x, y, flags, parameters):
    if events == cv.EVENT_LBUTTONDOWN:  # if left click area, add that point to the list
        position_list.append((x, y))
    if events == cv.EVENT_RBUTTONDOWN:  # if right click, remove point from list
        for i, position in enumerate(position_list):
            x1, y1 = position
            if x1 < x < x1+width and y1 < y < y1+height:
                position_list.pop(i)


def drawSample(selected):
    global imgCopy
    print("Drag the mouse over the area of 1 parking space.")
    print("If you are satisfied, press \'s\' to save sample.")
    print("if you want to redo, press \'r\'.")
    imgCopy=cv.imread('./ParkingLotMonitor/Samples/{}'.format(selected),1)
    while True:
        cv.imshow("Draw sample", imgCopy)
        cv.setMouseCallback("Draw sample", draw)
        k=cv.waitKey(1)
        if k==ord('s'):
            sample_points.extend([ix,iy,ex,ey])
            break
        elif k==ord('r'):
            imgCopy=cv.imread('./ParkingLotMonitor/Samples/{}'.format(selected),1)
    cv.destroyAllWindows()


def monitor():
    pass


def edit():
    pass


def create():
    global sample_img
    global imgCopy
    global width
    global height
    print("What type of parking lot do you want to create?")
    print("1.Car\n2.Motorcycle/Scooter")
    satisfied=False
    parkinglot_type=""
    while not satisfied:
        choice=int(input())
        if choice == 1 or choice==2:
            if choice==1:
                parkinglot_type="Car"
            else:
                parkinglot_type="Scooter"
            satisfied=True
        else:
            print("Invalid input. Please try again.")
    print("What would you like to name this parking lot?")
    parkinglot_name = input()
    print("In order to create a parking lot, perform the following steps.")
    print("1. Place a sample image of the parking lot in the \"Samples\" folder.\n2. Take a sample of one of the parking spaces.\n3. Outline the parking lot by clicking the top left of each lot.\n\t -Left click to add\n\t -Right click to remove\n4. Press \"s\" to save, \"q\" to quit.")
    print("Is the sample image already in the folder? (Y/N)")
    selectPhoto = True
    ans = input()
    if ans == 'N' or ans == 'n' or ans == 'No' or ans == 'no':
        print("Please place the sample image in the folder then try again.")
    elif ans == 'Y' or ans == 'y' or ans == 'Yes' or ans == 'yes':
        sample_images = os.listdir("./ParkingLotMonitor/Samples")
        print("Please select an image from the folder")
        counter = 1
        for sample in sample_images:
            print("{}.{}".format(counter, sample.capitalize()))
        selection = int(input())
        selected_img = sample_images[selection-1]
        drawSample(selected_img)
        width = sample_points[2]-sample_points[0]
        height = sample_points[3]-sample_points[1]
        print("Left click the top left corner of each lot to outline")
        print("Right click anywhere in the outline to remove it.")
        print("Press \'s\' to save.")
        while True:
            sample_img = cv.imread(
            "./ParkingLotMonitor/Samples/{}".format(selected_img))
            for position in position_list:
                cv.rectangle(sample_img, tuple(position), (position[0]+width, position[1]+height), (0,255,0),3)
            cv.imshow("Outline Parking Lot", sample_img)
            cv.setMouseCallback("Outline Parking Lot", outlineParkingSpace)
            k=cv.waitKey(1)
            if k ==ord('s'):
                cv.destroyAllWindows()
                break
        print("Lastly, how many lots per row are there?")
        lots_per_row=int(input())
        x_positions=[position[0] for position in position_list]
        y_positions=[position[1] for position in position_list]
        vacant_lots=[True for lot in position_list]
        data={
            "name": parkinglot_name,
            "capacity":len(vacant_lots),
            "x": x_positions,
            "y": y_positions,
            "lots": vacant_lots,
            "lotsPerRow": lots_per_row,
        }
        
        db_ref=database.collection(parkinglot_type).document(parkinglot_name).set(data)
        print("Parking lot sucessfully added to database.")
        


def main():
    exit_option = False
    while(not exit_option):
        print("Welcome to NDHU Smart-Park System.")
        print("What would you like to do?")
        print("1. Monitor A Parking Lot.\n2. Create Parking Lot.\n3. Edit Existing Parking Lot.\n4. Exit")
        choice = int(input())
        if choice == 1:
            pass
        elif choice == 2:
            create()
        elif choice == 3:
            pass
        elif choice == 4:
            print("Thank you. Have a nice day")
            exit_option = True
        else:
            print("Invalid input. Please try again")


if __name__ == '__main__':
    main()
