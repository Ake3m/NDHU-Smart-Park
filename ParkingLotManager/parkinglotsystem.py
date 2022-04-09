import os
from pathlib import Path
from charset_normalizer import detect
import cv2 as cv
import numpy as np
from firebase_admin import initialize_app
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import random
import PySimpleGUI as sg


# GLOBAL VARIABLES SECTION
drawing = False
ix = 0  # initial x
iy = 0  # initial y
ex = 0  # ending x
ey = 0  # ending y
sample_img = ""
imgCopy = ""
sample_points = []  # list holding the sample points
position_list = []  # list holding the position of each lot
width = 0
height = 0
lot_names = []
lot_types = []
vacant_lots = []
previous_list = []
clas_names = []


confidence_threshold = 0.2
nms_threshold = 0.3

# FIREBASE CONFIGURATION SETUP
cred = credentials.Certificate("./serviceAccountKey.json")
initialize_app(cred, {'storageBucket': 'smart-park-13acd.appspot.com'})
database = firestore.client()


def generateHexColor():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '0xFF' + hex_number[2:]
    return hex_number


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
        ex = x
        ey = y
        # sample_points.extend([ix,iy,x,y])


def outlineParkingSpace(events, x, y, flags, parameters):
    if events == cv.EVENT_LBUTTONDOWN:  # if left click area, add that point to the list
        position_list.append((x, y))
        print("Adding...")
        print(position_list)
    if events == cv.EVENT_RBUTTONDOWN:  # if right click, remove point from list
        print("Removing...")
        print(position_list)
        for i, position in enumerate(position_list):
            x1, y1 = position
            if x1 < x < x1+width and y1 < y < y1+height:
                print("Yes")
                position_list.pop(i)


def drawSample(selected):
    global imgCopy
    print("Drag the mouse over the area of 1 parking space.")
    print("If you are satisfied, press \'s\' to save sample.")
    print("if you want to redo, press \'r\'.")
    # imgCopy = cv.imread('./ParkingLotManager/Samples/{}'.format(selected), 1)
    imgCopy=cv.imread(selected, 1)
    while True:
        cv.imshow("Draw sample", imgCopy)
        cv.setMouseCallback("Draw sample", draw)
        k = cv.waitKey(1)
        if k == ord('s'):
            sample_points.extend([ix, iy, ex, ey])
            break
        elif k == ord('r'):
            imgCopy = cv.imread(
                './ParkingLotManager/Samples/{}'.format(selected), 1)
    cv.destroyAllWindows()


def findObjects(outputs, img):
    global confidence_threshold, nms_threshold, class_names
    img_height, img_width, channels = img.shape
    bounding_box = []
    classIds = []
    confidence_list = []

    for output in outputs:
        for detection in output:
            # removes the first 5 entries in order to look at the probabilities
            scores = detection[5:]
            # finds the index with the heighest probability
            classId = np.argmax(scores)
            confidence = scores[classId]  # finds the confidence value
            if confidence > confidence_threshold:
                width, height = int(
                    detection[2]*img_width), int(detection[3]*img_height)
                # center_x, center_y=int((detection[0]*img_width)-width/2), int((detection[1]*img_height)-height/2) #changes center x and y to left most point
                # gets the center x and y
                center_x, center_y = int(
                    (detection[0]*img_width)), int((detection[1]*img_height))

                bounding_box.append([center_x, center_y, width, height])
                classIds.append(classId)
                confidence_list.append(float(confidence))
    print(len(bounding_box))
    indices = cv.dnn.NMSBoxes(
        bounding_box, confidence_list, confidence_threshold, nms_threshold)
    confident_boxes = []
    for i in indices:
        box = bounding_box[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv.rectangle(img, (x, y), (x+0, y+0), (255, 255, 255), 10)
        cv.putText(img, f'{class_names[classIds[i]]} {int(confidence_list[i]*100)}%',
                   (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        confident_boxes.append(box)

    return confident_boxes


def checkParkingSpaces(image, width, height, position_list, confident_boxes, coll, doc):
    global previous_list, vacant_lots
    previous_list = vacant_lots.copy()
    db_ref = database.collection(coll).document(doc)
    for i, position in enumerate(position_list):
        x, y = position
        color = (0, 255, 0)
        thickness = 3
        vacant_lots[i] = True
        # cropped_img = image[y:y+height, x:x+width]
        # add detection code here
        for box in confident_boxes:
            if x < box[0] < x+width and y < box[1] < y+height:
                color = (0, 0, 255)
                thickness = 3
                vacant_lots[i] = False
                # cv.rectangle(image, (x,y),(x,+),(255,0,0), 5)

        cv.rectangle(image, position,
                     (position[0]+width, position[1]+height), color, thickness)

        if vacant_lots != previous_list:
            previous_list = vacant_lots.copy()
            db_ref.update({'lot': vacant_lots})
            print("updated")


def monitor():
    global lot_types
    global lot_names
    global position_list
    global vacant_lots
    global width, height
    global class_names
    # retrieve values needed from database
    print("Which parking lot type would you like to monitor?")
    collections = database.collections()
    counter = 1
    lot_types = []
    for collection in collections:
        lot_types.append(collection.id)
        print("{}.{}".format(counter, collection.id))
        counter += 1
    collection_choice = lot_types[int(input())-1]
    print("Which Parking Lot would you like to monitor?")
    documents = database.collection(collection_choice).stream()
    counter = 1
    for doc in documents:
        lot_names.append(doc.id)
        print("{}.{}".format(counter, doc.id))
        counter += 1
    doc_choice = lot_names[int(input())-1]

    parking_lot_info = database.collection(collection_choice).document(
        doc_choice).get().to_dict()  # gets the data from database and converts to dictionary
    for i in range(len(parking_lot_info["x"])):
        position_list.append(
            [parking_lot_info["x"][i], parking_lot_info["y"][i]])
    vacant_lots = parking_lot_info["lot"]
    width = parking_lot_info["width"]
    height = parking_lot_info["height"]
    # access camera and check lot
    # change to 0 for laptop webcam, 1 for external webcam
    cap = cv.VideoCapture(1)
    wht = 320
    if not cap.isOpened():
        print("Error opening camera")
        exit()
    # yolov3 config
    class_names = ['Car', 'Motorcycle']
    modelConfiguration = './ParkingLotManager/yolov3/yolov3-custom.cfg'
    modelWeights = './ParkingLotManager/yolov3/yolov3-custom_last.weights'
    net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    # image needs to be converted to blob
    while True:
        flag, img = cap.read()

        # convert image to blob
        blob = cv.dnn.blobFromImage(
            img, 1/255, (wht, wht), [0, 0, 0], 1, crop=False)
        net.setInput(blob)

        layerNames = net.getLayerNames()

        outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]

        outputs = net.forward(outputNames)  # list of outputs
        # print(outputs[0].shape)
        # print(outputs[1].shape)
        # print(outputs[2].shape)

        conf_box = findObjects(outputs, img)
        checkParkingSpaces(img, width, height, position_list,
                           conf_box, collection_choice, doc_choice)
        cv.imshow("Monitor feed", img)

        k = cv.waitKey(10)
        if k == ord('q'):
            cv.destroyAllWindows()
            break


def edit():
    global width, height, position_list
    # retrieve values needed from database
    print("Which parking lot type would you like to edit?")
    collections = database.collections()
    counter = 1
    lot_types = []
    for collection in collections:
        lot_types.append(collection.id)
        print("{}.{}".format(counter, collection.id))
        counter += 1
    collection_choice = lot_types[int(input())-1]
    print("Which Parking Lot would you like to edit?")
    documents = database.collection(collection_choice).stream()
    counter = 1
    for doc in documents:
        lot_names.append(doc.id)
        print("{}.{}".format(counter, doc.id))
        counter += 1
    doc_choice = lot_names[int(input())-1]

    parking_lot_info = database.collection(collection_choice).document(
        doc_choice).get().to_dict()  # gets the data from database and converts to dictionary
    for i in range(len(parking_lot_info["x"])):
        position_list.append(
            (parking_lot_info["x"][i], parking_lot_info["y"][i]))
    vacant_lots = parking_lot_info["lot"]
    print(vacant_lots)
    width = parking_lot_info["width"]
    height = parking_lot_info["height"]
    sample_images = os.listdir("./ParkingLotManager/Samples")
    while True:
        sample_img = cv.imread(
            "./ParkingLotManager/Samples/{}".format(parking_lot_info["imgURL"]))
        for position in position_list:
            cv.rectangle(sample_img, tuple(
                position), (position[0]+width, position[1]+height), (0, 255, 0), 3)
        cv.imshow("Outline Parking Lot", sample_img)
        cv.setMouseCallback("Outline Parking Lot", outlineParkingSpace)
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.destroyAllWindows()
            break
    parking_lot_updated_info = database.collection(collection_choice).document(
        doc_choice)
    x_positions = [position[0] for position in position_list]
    y_positions = [position[1] for position in position_list]
    vacant_lots = [True for lot in position_list]
    print("Enter updated number of lots per row")
    lotsPerRow = int(input())
    parking_lot_updated_info.update({
        "x": x_positions,
        "y": y_positions,
        "lot": vacant_lots,
        "lotsPerRow": lotsPerRow
    })
    print("Information successfully updated")


def test():
    layout = [[sg.Text('Test')]]
    win2 = sg.Window('test', layout=layout).read()


def create2():
    global sample_img
    global imgCopy
    global width
    global height
    global position_list
    global sample_points
    parkinglot_type=''
    parkinglot_name=''
    create_layout = [[sg.Text('What type of parking lot do you want to create?')],
    [sg.Radio('Car', 'TYPE', default=True, key='car'),
        sg.Radio('Scooter', 'TYPE',key='scooter')],
        [sg.Text('Parking Lot Name:'),
        sg.Input(key='lot_name')], [sg.Text('In order to create a parking lot, perform the following steps:')],
        [sg.Text('1. Place a sample image of the parking lot in the \"Samples\" folder.\n2. Take a sample of one of the parking spaces.\n3. Outline the parking lot by clicking the top left of each lot.\n\t -Left click to add\n\t -Right click to remove\n4. Press \"s\" to save, \"q\" to quit.')],
        [sg.Text('Select the sample image of the parking lot')],
        [sg.Input(key='image_path'), sg.FileBrowse()],
        [sg.Button('Cancel', key='cancel'),
        sg.Button('Next', key='next')]]
    createWindow = sg.Window('Create Parking Lot', layout=create_layout)

    while True:
        event, values = createWindow.read()
        if event=='cancel'or event == sg.WIN_CLOSED:
            break
        if event=='next' and values['lot_name']!='' and values['image_path']!='':
            selected_img=values['image_path'];
            parkinglot_name=values['lot_name']
            if values['car']==True:
                parkinglot_type='Car'
            elif values['scooter']==True:
                parkinglot_type="Scooter"
            parkinglot_type
            print(parkinglot_type)
            drawSample(selected_img)
            break
        else:
            sg.popup_ok('Please ensure that Name and Image Path are filled.')

    createWindow.close()
    createWindow=sg.popup_ok('Left click the top left corner of each lot to outline\nRight click anywhere in the outline to remove it.\nPress \'s\' to save.')
    width = sample_points[2]-sample_points[0]
    height = sample_points[3]-sample_points[1]
    while True:
        sample_img = cv.imread(selected_img)
        for position in position_list:
            cv.rectangle(sample_img, tuple(
                position), (position[0]+width, position[1]+height), (0, 255, 0), 3)
        cv.imshow("Outline Parking Lot", sample_img)
        cv.setMouseCallback("Outline Parking Lot", outlineParkingSpace)
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.destroyAllWindows()
            break
    lots_per_row = int(sg.popup_get_text(title='Almost Done', message='Lastly, how many lots per row are there?'))
    x_positions = [position[0] for position in position_list]
    y_positions = [position[1] for position in position_list]
    vacant_lots = [True for lot in position_list]
    data = {
        "name": parkinglot_name,
        "capacity": len(vacant_lots),
        "x": x_positions,
        "y": y_positions,
        "lot": vacant_lots,
        "lotsPerRow": lots_per_row,
        "width": width,
        "height": height,
        "imgURL": selected_img,
        "tileColor": generateHexColor(),

    }

    db_ref = database.collection(parkinglot_type).document(
        parkinglot_name).set(data)
    sg.popup_ok('Parking lot successfully created.')
        



def create():
    global sample_img
    global imgCopy
    global width
    global height
    global position_list
    global sample_points
    position_list = []
    sample_points = []
    width = 0
    height = 0
    print("What type of parking lot do you want to create?")
    print("1.Car\n2.Motorcycle/Scooter")
    satisfied = False
    parkinglot_type = ""
    while not satisfied:
        choice = int(input())
        if choice == 1 or choice == 2:
            if choice == 1:
                parkinglot_type = "Car"
            else:
                parkinglot_type = "Scooter"
            satisfied = True
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
        sample_images = os.listdir("./ParkingLotManager/Samples")
        print("Please select an image from the folder")
        counter = 1
        for sample in sample_images:
            print("{}.{}".format(counter, sample.capitalize()))
            counter += 1
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
                "./ParkingLotManager/Samples/{}".format(selected_img))
            for position in position_list:
                cv.rectangle(sample_img, tuple(
                    position), (position[0]+width, position[1]+height), (0, 255, 0), 3)
            cv.imshow("Outline Parking Lot", sample_img)
            cv.setMouseCallback("Outline Parking Lot", outlineParkingSpace)
            k = cv.waitKey(1)
            if k == ord('s'):
                cv.destroyAllWindows()
                break
        print("Lastly, how many lots per row are there?")
        lots_per_row = int(input())
        x_positions = [position[0] for position in position_list]
        y_positions = [position[1] for position in position_list]
        vacant_lots = [True for lot in position_list]
        data = {
            "name": parkinglot_name,
            "capacity": len(vacant_lots),
            "x": x_positions,
            "y": y_positions,
            "lot": vacant_lots,
            "lotsPerRow": lots_per_row,
            "width": width,
            "height": height,
            "imgURL": selected_img,
            "tileColor": generateHexColor(),

        }

        db_ref = database.collection(parkinglot_type).document(
            parkinglot_name).set(data)
        print("Parking lot sucessfully added to database.")


def main():
    sg.theme('Green')
    img_path = './ParkingLotManager/assets/smartparklogo_300x350.png'
    home_layout = [[sg.Image(img_path, )], [sg.Text('Welcome to NDHU Smart Park', size=(35, 1), justification='center')], [
        sg.Text('What would you like to do?', size=(35, 1), justification='center')], [sg.Button('Monitor Parking Lot', key='Monitor')], [sg.Button('Create Parking Lot', key='Create')], [sg.Button('Edit Parking Lot', key='Edit')], [sg.Button('Exit')]]

    main_window = sg.Window(
        'NDHU Smart-Park', layout=[home_layout], margins=(100, 50), element_justification='c')

    while True:
        event, values = main_window.read()
        if event == 'Monitor':
            print('Monitor')
        elif event == 'Create':
            main_window.Hide()
            create2()
            main_window.un_hide()
        elif event == 'Edit':
            print('Edit')
        elif event == sg.WIN_CLOSED or event == 'Exit':
            break

    main_window.close()

    # exit_option = False
    # while(not exit_option):
    #     print("Welcome to NDHU Smart-Park System.")
    #     print("What would you like to do?")
    #     print("1. Monitor A Parking Lot.\n2. Create Parking Lot.\n3. Edit Existing Parking Lot.\n4. Exit")
    #     choice = int(input())
    #     if choice == 1:
    #         monitor()
    #     elif choice == 2:
    #         create()
    #     elif choice == 3:
    #         edit()
    #     elif choice == 4:
    #         print("Thank you. Have a nice day")
    #         exit_option = True
    #     else:
    #         print("Invalid input. Please try again")


if __name__ == '__main__':
    main()
