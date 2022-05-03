import os
from pathlib import Path
import cv2 as cv
import numpy as np
from firebase_admin import initialize_app
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import random
import PySimpleGUI as sg
from datetime import date
import time
import automatic

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
top_left_x = []
top_left_y = []
top_rights_x = []
top_rights_y = []
bottom_lefts_x = []
bottom_lefts_y = []
bottom_rights_x = []
bottom_rights_y = []
coordinates_temp=[]
cycles=[]
parking_lot_dict=dict()
editing=False
editing_row=0
editing_index=0
row_edit=False
row_was_edited=False


confidence_threshold = 0.2
nms_threshold = 0.3  # originally set to 0.3

# FIREBASE CONFIGURATION SETUP - DO NOT TOUCH
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
def definePoints(events, x, y, flags, params):
    global cycles
    if events == cv.EVENT_LBUTTONDOWN:
        coordinates_temp.append((x,y))
    if events==cv.EVENT_RBUTTONDOWN:
        for i, cycle in enumerate(cycles):
            print(cycle)
            tl, tr, br, bl = cycle
            if tl[0]< x<tr[0] and tr[1] <y < br[1]:
                cycles.pop(i)

def changeOutlineLayout(events, x,y,flags, params):
    global editing, imgCopy, coordinates_temp, editing_row, editing_index, row_edit
    global parking_lot_dict
    if events == cv.EVENT_LBUTTONDBLCLK and editing==False and row_edit==False:
        print('editing enabled')
        editing=True
        for row in parking_lot_dict.keys():
            for i,points in enumerate(parking_lot_dict[row]):
                tl, tr, br, bl = points
                if tl[0]< x<tr[0] and tr[1] <y < br[1]:
                    editing_row=row
                    editing_index=i
                    print('editing {} index {}'.format(editing_row, editing_index))
    elif events == cv.EVENT_LBUTTONDBLCLK and editing==True and row_edit==False:
        editing=False
        coordinates_temp=[]
    if events ==cv.EVENT_LBUTTONDOWN and editing==True:
        coordinates_temp.append((x,y))
        print('appending')
    if events ==cv.EVENT_RBUTTONDBLCLK and row_edit==False and editing==False:
        row_edit=True
        for row in parking_lot_dict.keys():
            for i,points in enumerate(parking_lot_dict[row]):
                tl, tr, br, bl = points
                if tl[0]< x<tr[0] and tr[1] <y < br[1]:
                    editing_row=row
    elif events ==cv.EVENT_RBUTTONDBLCLK and row_edit==True and editing==False:
        row_edit=False
        coordinates_temp=[]
    if events ==cv.EVENT_LBUTTONDOWN and row_edit==True:
        coordinates_temp.append((x,y))



def drawSample(selected):
    global imgCopy
    sg.popup_ok(
        'Drag over 1 parking space to collect a sample. Press \'s\' to save the sample and \'r\' to redo it.')
    print("Drag the mouse over the area of 1 parking space.")
    print("If you are satisfied, press \'s\' to save sample.")
    print("if you want to redo, press \'r\'.")
    imgCopy = cv.imread('./ParkingLotManager/Samples/{}'.format(selected), 1)
    # imgCopy = cv.resize(imgCopy, (640, 480))
    # imgCopy = cv.imread(selected, 1)
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
            imgCopy = cv.resize(imgCopy, (640, 480))
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


def checkParkingSpacesAutomatic(image, points, confident_boxes, coll, doc):
    global previous_list, vacant_lots
    previous_list = vacant_lots.copy()
    db_ref = database.collection(coll).document(doc)
    for i, point in enumerate(points):
        topLeft, topRight, bottomRight, bottomLeft=point 
        vacant_lots[i]=True
        color=(0,255,0)
        for box in confident_boxes:
            if topLeft[0] < box[0] < topRight[0] and topLeft[1] < box[1] < bottomLeft[1]:
                color = (0, 0, 255)
                vacant_lots[i] = False
        cv.polylines(image,[point],True,color,2)

        if vacant_lots != previous_list:
            previous_list = vacant_lots.copy()
            db_ref.update({'lot': vacant_lots})
            print("updated")


def checkParkingSpaces(image, width, height, position_list, confident_boxes, coll, doc):
    global previous_list, vacant_lots
    previous_list = vacant_lots.copy()
    db_ref = database.collection(coll).document(doc)
    for i, position in enumerate(position_list):
        x, y = position
        color = (0, 255, 0)
        thickness = 2
        vacant_lots[i] = True
        # cropped_img = image[y:y+height, x:x+width]
        # add detection code here
        for box in confident_boxes:
            if x < box[0] < x+width and y < box[1] < y+height:
                color = (0, 0, 255)
                thickness = 1
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
    global top_left_x
    global top_left_y
    global top_rights_x
    global top_rights_y
    global bottom_lefts_x
    global bottom_lefts_y
    global bottom_rights_x
    global bottom_rights_y

    close = False
    collections = database.collections()
    lot_types = [collection.id for collection in collections]
    print(collections)
    monitor_layout1 = [[sg.Text('Which parking Lot Type would you like to monitor?')], [
        sg.Combo(lot_types, key='choice'), sg.Button('Next', key='next')]]
    monitorWindow = sg.Window('Select lot type', monitor_layout1)
    while True:
        event, values = monitorWindow.read()
        if event == sg.WIN_CLOSED:
            close = True
            break
        if event == 'next' and values['choice'] != '':
            collection_choice = values['choice']
            break
        else:
            sg.popup_error('Please select a type')
    monitorWindow.close()
    if close == True:
        return
    documents = database.collection(collection_choice).stream()
    lot_names = [doc.id for doc in documents]
    monitor_layout2 = [[sg.Text('Select the parking lot you wish to monitor')], [sg.Listbox(
        lot_names, size=(50, 6), key='lot')], [sg.Button('Next', key='Next')]]
    monitorWindow = sg.Window('Select Parking Lot', monitor_layout2)
    while True:
        events, values = monitorWindow.read()
        if events == sg.WIN_CLOSED:
            break
        if events == 'Next':
            doc_choice = values['lot'][0]
            break
    monitorWindow.close()
    parking_lot_info = database.collection(collection_choice).document(
        doc_choice).get().to_dict()  # gets the data from database and converts to dictionary
    uses_points = parking_lot_info['uses_points']
    if uses_points == True:
        points = []
        top_left_x = parking_lot_info['top_left_x']
        top_left_y = parking_lot_info['top_left_y']
        top_rights_x = parking_lot_info['top_rights_x']
        top_rights_y = parking_lot_info['top_rights_y']
        bottom_lefts_x = parking_lot_info['bottom_lefts_x']
        bottom_lefts_y = parking_lot_info['bottom_lefts_y']
        bottom_rights_x = parking_lot_info['bottom_rights_x']
        bottom_rights_y = parking_lot_info['bottom_rights_y']

        for i in range(len(top_left_x)):
            points.append([[top_left_x[i], top_left_y[i]], [top_rights_x[i], top_rights_y[i]], [
                            bottom_rights_x[i], bottom_rights_y[i]], [bottom_lefts_x[i], bottom_lefts_y[i]]])
        
        print(len(points))
        print(points)
        points=np.array(points, dtype=np.int32)
    else:
        for i in range(len(parking_lot_info["x"])):
            position_list.append(
                [parking_lot_info["x"][i], parking_lot_info["y"][i]])
    vacant_lots = parking_lot_info["lot"]
    width = parking_lot_info["width"]
    height = parking_lot_info["height"]
    sg.popup_ok(
        'The monitor feed will appear. Click \'q\' in order to end monitor session.')
    # access camera and check lot
    # change to 0 for laptop webcam, 1 for external webcam
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    # cap.set(3, 640)
    # cap.set(4, 480)
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
        if uses_points == True:
            checkParkingSpacesAutomatic(img, points, conf_box, collection_choice, doc_choice)
        else:
            checkParkingSpaces(img, width, height, position_list,
                               conf_box, collection_choice, doc_choice)
        cv.imshow("Monitor feed", img)

        k = cv.waitKey(10)
        if k == ord('q'):
            cv.destroyAllWindows()
            break


def edit(collection_choice, doc_choice,parking_lot_info):
    global width, height, position_list
    close = False
   
    for i in range(len(parking_lot_info["x"])):
        position_list.append(
            (parking_lot_info["x"][i], parking_lot_info["y"][i]))
    vacant_lots = parking_lot_info["lot"]
    print(vacant_lots)
    width = parking_lot_info["width"]
    height = parking_lot_info["height"]
    sg.popup_ok('After making the appropriate changes, press \'s\' to save')
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
    lotsPerRow = int(sg.popup_get_text('Lastly, how many rows per lot?'))
    parking_lot_updated_info.update({
        "x": x_positions,
        "y": y_positions,
        "lot": vacant_lots,
        "lotsPerRow": lotsPerRow
    })
    sg.popup_ok('Information successfully updated')


def create():
    global sample_img
    global imgCopy
    global width
    global height
    global position_list
    global sample_points
    global top_left_x
    global top_left_y
    global top_rights_x
    global top_rights_y
    global bottom_lefts_x
    global bottom_lefts_y
    global bottom_rights_x
    global bottom_rights_y
    global coordinates_temp
    global cycles
    global parking_lot_dict
    parkinglot_type = ''
    parkinglot_name = ''
    x_positions = []
    y_positions = []
    automatic_selection = False
    close = False
    usesPoints=True
    create_layout = [[sg.Text('What type of parking lot do you want to create?')],
                     [sg.Radio('Car', 'TYPE', default=True, key='car'),
                      sg.Radio('Scooter', 'TYPE', key='scooter')],
                     [sg.Text('Parking Lot Name:'),
                      sg.Input(key='lot_name')], [sg.Text('In order to create a parking lot, perform the following steps:')],
                     [sg.Text('Manual Method:\n1. Place a sample image of the parking lot in the \"Samples\" folder.\n2. Take a sample of one of the parking spaces.\n3. Outline the parking lot by clicking the top left of each lot.\n\t -Left click to add\n\t -Right click to remove\n4. Press \"s\" to save, \"q\" to quit.')],
                     [sg.Text('Would you like to try automatic outlining?')],
                     [sg.Radio('Yes', 'OUTLINE', key='yes'),
                      sg.Radio('No', 'OUTLINE', default=True, key='no')],
                     [sg.Text('Select the sample image of the parking lot')],
                     [sg.Input(key='image_path'), sg.FileBrowse()],
                     [sg.Button('Cancel', key='cancel'),
                      sg.Button('Next', key='next')]]
    createWindow = sg.Window('Create Parking Lot', layout=create_layout)

    while True:
        event, values = createWindow.read()
        if event == 'cancel' or event == sg.WIN_CLOSED:
            close = True
            break
        if event == 'next' and values['lot_name'] != '' and values['image_path'] != '':
            selected_img = str(Path(values['image_path']).name)
            print(selected_img)
            parkinglot_name = values['lot_name']
            if values['car'] == True:
                parkinglot_type = 'Car'
            elif values['scooter'] == True:
                parkinglot_type = "Scooter"
            if values['yes'] == True:
                uses_points = True
            elif values['no'] == True:
                uses_points = False
            break
        else:
            sg.popup_ok('Please ensure that Name and Image Path are filled.')

    createWindow.close()
    if close == True:
        return
    print(uses_points)
    if uses_points == False:  # MANUAL SELECTION CODE
        img = cv.imread("./ParkingLotManager/Samples/{}".format(selected_img))
        # img = cv.resize(img, (900, 600))
        manual_mode_method=''
        manual_select_layout = [[sg.Text('Select Manual Mode outline method:')], [
        sg.Combo(['Rectangles', 'Flexible'], key='choice'), sg.Button('Next', key='next')]]
        manual_select_window=sg.Window('Manual Mode Selection', manual_select_layout)
        while True:
            event, values=manual_select_window.read()
            if event==sg.WIN_CLOSED:
                return
            if event == 'next' and values['choice']!='':
                manual_mode_method=values['choice']
                break
            if event =='next' and values['choice']=='':
                sg.popup('Please select a type')
        manual_select_window.close()
        if manual_mode_method=='Rectangles':
        
            # print(position_list)
            drawSample(selected_img)
            createWindow = sg.popup_ok(
                'Left click the top left corner of each lot to outline\nRight click anywhere in the outline to remove it.\nPress \'s\' to save.')
            width = sample_points[2]-sample_points[0]
            height = sample_points[3]-sample_points[1]
            while True:
               
                sample_img = cv.imread(
                    "./ParkingLotManager/Samples/{}".format(selected_img))
                # sample_img = cv.resize(sample_img, (650, 480))
                for position in position_list:
                    cv.rectangle(sample_img, tuple(
                        position), (position[0]+width, position[1]+height), (0, 255, 0), 3)
                cv.imshow("Outline Parking Lot", sample_img)
                cv.setMouseCallback("Outline Parking Lot", outlineParkingSpace)
                k = cv.waitKey(1)
                if k == ord('s'):
                    cv.destroyAllWindows()
                    break
            lots_per_row = int(sg.popup_get_text(title='Almost Done',
                                                message='Lastly, how many lots per row are there?'))
            x_positions = [position[0] for position in position_list]
            y_positions = [position[1] for position in position_list]
            vacant_lots = [True for lot in position_list]
        else:
            print('Flexible')
            uses_points=True
            lots_per_row=1
            row_count=1
            row=[]
            sg.popup_ok('Be sure to select the points in a clockwise  order. Starting from top-left')
            while True:
                sample_img = cv.imread(
                    "./ParkingLotManager/Samples/{}".format(selected_img))
                if len(coordinates_temp)==4:
                    cycles.append(np.array(coordinates_temp))
                    row.append(np.array(coordinates_temp))
                    coordinates_temp=[]
                
                for cycle in cycles:
                     cv.polylines(sample_img,[cycle],True,(0,255,0),2)
                for c in coordinates_temp:
                    cv.rectangle(sample_img, (c),(c[0]+10, c[1]+10),(0,0,255), -1)
                cv.imshow('Select the points', sample_img)
                cv.setMouseCallback('Select the points', definePoints)
                k=cv.waitKey(1)
                if k==ord('s'):
                    cv.destroyAllWindows()
                    parking_lot_dict['row_{}'.format(row_count)]=row
                    break
                if k==ord('c'):
                    parking_lot_dict['row_{}'.format(row_count)]=row
                    lots_per_row=len(row)
                    row=[]
                    row_count+=1

    else:  # AUTOMATIC DETECTION
        parking_lot_dict, lots_per_row = automatic.outline(selected_img)
    top_left_x = []
    top_left_y = []
    top_rights_x = []
    top_rights_y = []
    bottom_lefts_x = []
    bottom_lefts_y = []
    bottom_rights_x = []
    bottom_rights_y = []
    for rows in parking_lot_dict.keys():
        for k in parking_lot_dict[rows]:
            top_left_x.append(float(k[0][0]))
            top_left_y.append(float(k[0][1]))
            top_rights_x.append(float(k[1][0]))
            top_rights_y.append(float(k[1][1]))
            bottom_rights_x.append(float(k[2][0]))
            bottom_rights_y.append(float(k[2][1]))
            bottom_lefts_x.append(float(k[3][0]))
            bottom_lefts_y.append(float(k[3][1]))
    if uses_points==True:
        vacant_lots = [True for points in top_left_x]

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
        "top_left_x": top_left_x,
        "top_left_y": top_left_y,
        "top_rights_x": top_rights_x,
        "top_rights_y": top_rights_y,
        "bottom_lefts_x": bottom_lefts_x,
        "bottom_lefts_y": bottom_lefts_y,
        "bottom_rights_x": bottom_rights_x,
        "bottom_rights_y": bottom_rights_y,
        "uses_points": uses_points
    }

    db_ref = database.collection(parkinglot_type).document(
        parkinglot_name).set(data)
    sg.popup_ok('Parking lot successfully created.')


def singleSpaceOutline(parking_lot_info):
    global parking_lot_dict
    global imgCopy
    global coordinates_temp
    global editing
    global row_edit
    global row_was_edited
    img_name=parking_lot_info['imgURL']
    lots_per_row=parking_lot_info['lotsPerRow']
    capacity=parking_lot_info['capacity']
    rows=capacity/lots_per_row
    row_count=1
    points=[]
    top_left_x = parking_lot_info['top_left_x']
    top_left_y = parking_lot_info['top_left_y']
    top_rights_x = parking_lot_info['top_rights_x']
    top_rights_y = parking_lot_info['top_rights_y']
    bottom_lefts_x = parking_lot_info['bottom_lefts_x']
    bottom_lefts_y = parking_lot_info['bottom_lefts_y']
    bottom_rights_x = parking_lot_info['bottom_rights_x']
    bottom_rights_y = parking_lot_info['bottom_rights_y']
    for i in range(capacity):
        print(i)
        points.append([[top_left_x[i], top_left_y[i]], [top_rights_x[i], top_rights_y[i]], [
                        bottom_rights_x[i], bottom_rights_y[i]], [bottom_lefts_x[i], bottom_lefts_y[i]]])
        if (i+1) % lots_per_row == 0:
            parking_lot_dict['row_{}'.format(row_count)]=np.array(points, np.int32)
            points=[]
            row_count+=1
    while True:
        
        img=cv.imread('./ParkingLotManager/Samples/{}'.format(img_name))
        if len(coordinates_temp) == 4 and editing==True:
            parking_lot_dict[editing_row][editing_index]=np.array(coordinates_temp, np.int32)
            coordinates_temp=[]
            editing=False
        elif len(coordinates_temp)==4 and row_edit==True:
            temp=parking_lot_dict[editing_row].tolist()
            temp.append(coordinates_temp)
            
            temp=np.array(temp, np.int32)
            print('Before:{}'.format(temp))
            temp=automatic.sortRow(temp, len(temp))
            print('After {}'.format(temp))
            
            parking_lot_dict[editing_row]=temp.copy()
            coordinates_temp=[]
            row_edit=False
            
        
        for row in parking_lot_dict.keys():
            for i,points in enumerate(parking_lot_dict[row]):
                if editing==True and i==editing_index and row ==editing_row or row_edit==True and row==editing_row:
                    color=(255,255,0)
                else:
                    color=(0,255,0)
                # print(type(points))
                cv.polylines(img,[points],True,color,2)
        for points in coordinates_temp:
            cv.rectangle(img, points, (points[0], points[1]), (0,0,255), 5)
        cv.imshow('Edit Lot Outline', img)
        cv.setMouseCallback('Edit Lot Outline',changeOutlineLayout)
        k=cv.waitKey(1)
        if k==ord('q'):
            cv.destroyAllWindows()
            return
        if k==ord('s'):
            cv.destroyAllWindows()
            for rows in parking_lot_dict.keys():
                for k in parking_lot_dict[rows]:
                    top_left_x.append(float(k[0][0]))
                    top_left_y.append(float(k[0][1]))
                    top_rights_x.append(float(k[1][0]))
                    top_rights_y.append(float(k[1][1]))
                    bottom_rights_x.append(float(k[2][0]))
                    bottom_rights_y.append(float(k[2][1]))
                    bottom_lefts_x.append(float(k[3][0]))
                    bottom_lefts_y.append(float(k[3][1]))
                    vacant_lots = [True for points in top_left_x]
                lots_per_row=len(parking_lot_dict[rows])
            
            
            parking_lot_info.update({
            "top_left_x": top_left_x,
            "top_left_y": top_left_y,
            "top_rights_x": top_rights_x,
            "top_rights_y": top_rights_y,
            "bottom_lefts_x": bottom_lefts_x,
            "bottom_lefts_y": bottom_lefts_y,
            "bottom_rights_x": bottom_rights_x,
            "bottom_rights_y": bottom_rights_y,
            "lotsPerRow": lots_per_row
            })
            break
        

    
def recapture(parking_lot_info):
    img_name = time.ctime(time.time()).replace(" ", "_").replace(":", "_")
    print(img_name)
    cap = cv.VideoCapture(1, cv.CAP_DSHOW)
    # cap.set(3, 640)
    # cap.set(4, 480)
    if not cap.isOpened():
        sg.popup_error("Error opening camera")
        return
    sg.popup_ok('Press \'s\' to save the picture.')
    while True:
        flag, img = cap.read()
        cv.imshow('Take a picture', img)

        k = cv.waitKey(10)
        # TODO add a way to retry
        if k == ord('s'):
            cv.imwrite(
                "./ParkingLotManager/Samples/{}.jpg".format(img_name), img)
            cv.destroyAllWindows()
            break
    parking_lot_dict, lots_per_row = automatic.outline(img_name)
    top_left_x = []
    top_left_y = []
    top_rights_x = []
    top_rights_y = []
    bottom_lefts_x = []
    bottom_lefts_y = []
    bottom_rights_x = []
    bottom_rights_y = []
    for rows in parking_lot_dict.keys():
        for k in parking_lot_dict[rows]:
            top_left_x.append(float(k[0][0]))
            top_left_y.append(float(k[0][1]))
            top_rights_x.append(float(k[1][0]))
            top_rights_y.append(float(k[1][1]))
            bottom_rights_x.append(float(k[2][0]))
            bottom_rights_y.append(float(k[2][1]))
            bottom_lefts_x.append(float(k[3][0]))
            bottom_lefts_y.append(float(k[3][1]))
    vacant_lots = [True for points in top_left_x]
    parking_lot_info.update({
        "lot": vacant_lots,
        "lotsPerRow": lots_per_row,
        "imgURL": img_name,
        "top_left_x": top_left_x,
        "top_left_y": top_left_y,
        "top_rights_x": top_rights_x,
        "top_rights_y": top_rights_y,
        "bottom_lefts_x": bottom_lefts_x,
        "bottom_lefts_y": bottom_lefts_y,
        "bottom_rights_x": bottom_rights_x,
        "bottom_rights_y": bottom_rights_y,
    })
    sg.popup('Calibration complete.')
    

def calibrate():
    global drawing
    global ix
    global iy
    global ex
    global ey
    global sample_img
    global imgCopy
    global sample_points
    global position_list
    global width
    global height
    global lot_names
    global lot_types
    global vacant_lots
    global previous_list
    global clas_names
    global top_left_x
    global top_left_y
    global top_rights_x
    global top_rights_y
    global bottom_lefts_x
    global bottom_lefts_y
    global bottom_rights_x
    global bottom_rights_y

    collections = database.collections()
    lot_types = [collection.id for collection in collections]
    edit_layout1 = [[sg.Text('Which parking Lot Type would you like to edit?')], [
        sg.Combo(lot_types, key='choice'), sg.Button('Next', key='next')]]
    editWindow = sg.Window('Select lot type', edit_layout1)
    while True:
        event, values = editWindow.read()
        if event == sg.WIN_CLOSED:
            return
        if event == 'next' and values['choice'] != '':
            collection_choice = values['choice']
            break
        else:
            sg.popup_error('Please select a type')
    editWindow.close()
    documents = database.collection(collection_choice).stream()
    lot_names = [doc.id for doc in documents]
    edit_layout2 = [[sg.Text('Select the parking lot you wish to edit')], [sg.Listbox(
        lot_names, size=(50, 6), key='lot')], [sg.Button('Next', key='Next')]]
    editWindow = sg.Window('Select Parking Lot', edit_layout2)
    while True:
        events, values = editWindow.read()
        if events == sg.WIN_CLOSED:
            return
        if events == 'Next':
            doc_choice = values['lot'][0]
            break
    editWindow.close()
    parking_lot_info = database.collection(collection_choice).document(
        doc_choice).get().to_dict()  # gets the data from database and converts to dictionary
    if parking_lot_info['uses_points']==True:
        calibrate_layout=[[sg.Text('What changes do you want to make?')],[sg.Button('Recapture', key='R'),sg.Button('Single Space Outline', key='S')]]
        calibrate_window =sg.Window('Please choose one', calibrate_layout)
        while True:
            events, values = calibrate_window.read()
            if events == sg.WIN_CLOSED:
                return
            if events == 'R':
                editWindow.close()
                recapture(parking_lot_info)
                break 
            if events=='S':
                editWindow.close()
                singleSpaceOutline(parking_lot_info)
                break
    else:
        edit(collection_choice, doc_choice,parking_lot_info)
def capture():
    sg.popup_ok("Images are stored in the Samples folder.")
    img_name = time.ctime(time.time()).replace(" ", "_").replace(":", "_")
    print(img_name)
    cap = cv.VideoCapture(1, cv.CAP_DSHOW)
    # cap.set(3, 640)
    # cap.set(4, 480)
    if not cap.isOpened():
        sg.popup_error("Error opening camera")
        return
    sg.popup_ok('Press \'s\' to save the picture.')
    while True:
        flag, img = cap.read()
        cv.imshow('Take a picture', img)

        k = cv.waitKey(10)
        # TODO add a way to retry
        if k == ord('s'):
            cv.imwrite(
                "./ParkingLotManager/Samples/{}.jpg".format(img_name), img)
            cv.destroyAllWindows()
            break


def main():
    global drawing
    global ix
    global iy
    global ex
    global ey
    global sample_img
    global imgCopy
    global sample_points
    global position_list
    global width
    global height
    global lot_names
    global lot_types
    global vacant_lots
    global previous_list
    global clas_names
    global top_left_x
    global top_left_y
    global top_rights_x
    global top_rights_y
    global bottom_lefts_x
    global bottom_lefts_y
    global bottom_rights_x
    global bottom_rights_y
    # setting the theme
    sg.LOOK_AND_FEEL_TABLE['custom_theme'] = {'BACKGROUND': '#4CC18A',
                                              'TEXT': '#000',
                                              'INPUT': '#339966',
                                              'TEXT_INPUT': '#000000',
                                              'SCROLL': '#99CC99',
                                              'BUTTON': ('#000', '#12A460'),
                                              'PROGRESS': ('#D1826B', '#CC8019'),
                                              'BORDER': 2, 'SLIDER_DEPTH': 0,
                                              'PROGRESS_DEPTH': 0, }

    # sg.theme('Green')
    sg.theme('custom_theme')
    img_path = './ParkingLotManager/assets/smartparklogo_300x350.png'
    home_layout = [[sg.Image(img_path, )], [sg.Text('Welcome to NDHU Smart Park', size=(35, 1), justification='center')], [
        sg.Text('What would you like to do?', size=(35, 1), justification='center')], [sg.Button('Monitor Parking Lot', key='Monitor')], [sg.Button('Create Parking Lot', key='Create')],
        [sg.Button('Cailbrate Pakring Lot', key='Calibrate')],
        [sg.Button('Take a picture', key='Take')],
        [sg.Button('Exit')]]

    main_window = sg.Window(
        'NDHU Smart-Park', layout=[home_layout], margins=(200, 50), element_justification='c')

    while True:
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
        top_left_x = []
        top_left_y = []
        top_rights_x = []
        top_rights_y = []
        bottom_lefts_x = []
        bottom_lefts_y = []
        bottom_rights_x = []
        bottom_rights_y = []
        parking_lot_dict=dict()
        event, values = main_window.read()
        if event == 'Monitor':
            print('Monitor')
            main_window.Hide()
            monitor()
            main_window.un_hide()
        elif event == 'Create':
            main_window.Hide()
            create()
            main_window.un_hide()
        elif event == 'Calibrate':
            main_window.Hide()
            calibrate()
            main_window.un_hide()
        elif event == 'Take':
            main_window.Hide()
            capture()
            main_window.un_hide()
        elif event == sg.WIN_CLOSED or event == 'Exit':
            break

    main_window.close()


if __name__ == '__main__':
    main()
