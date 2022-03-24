import os
from pathlib import Path
import cv2 as cv
import json
from cv2 import EVENT_LBUTTONDOWN
from firebase_admin import credentials, initialize_app, storage

drawing = False
ix = 0
iy = 0
sample_img = ""
sample_points = []
position_list = []
width=0
height=0


def draw(event, x, y, flags, parameters):
    global ix, iy, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y
    if event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.rectangle(sample_img, (ix, iy), (x, y), (0, 255, 0), -1)
    if event == cv.EVENT_LBUTTONUP:
        drawing = False
        sample_points.append(ix)
        sample_points.append(iy)
        sample_points.append(x)
        sample_points.append(y)


def outlineParkingSpace(events, x, y, flags, parameters):
    if events == cv.EVENT_LBUTTONDOWN:  # if left click area, add that point to the list
        position_list.append((x, y))
    if events == cv.EVENT_RBUTTONDOWN:  # if right click, remove point from list
        for i, position in enumerate(position_list):
            x1, y1 = position
            if x1 < x < x1+width and y1 < y < y1+height:
                position_list.pop(i)


def drawSample(img):
    print("Drag the mouse over the area of 1 parking space.")
    while True:
        cv.imshow("Draw sample", img)
        cv.setMouseCallback("Draw sample", draw)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()


def monitor():
    pass


def edit():
    pass


def create():
    global sample_img
    global width
    global height
    print("What would you like to name this parking lot?")
    parking_lot_name = input()
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
        sample_img = cv.imread(
            "./ParkingLotMonitor/Samples/{}".format(selected_img))
        drawSample(sample_img)
        width = sample_points[2]-sample_points[0]
        height = sample_points[3]-sample_points[1]
        print("Select the top left corner of each lot")
        while True:
            for position in position_list:
                cv.rectangle(sample_img, tuple(position), (position[0]+width, position[1]+height), (0,255,0),3)
            cv.imshow("Outline Parking Lot", sample_img)
            cv.setMouseCallback("Outline Parking Lot", outlineParkingSpace)
            k=cv.waitKey(1)
            if k ==ord('q'):
                break


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
