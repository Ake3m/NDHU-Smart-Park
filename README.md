# NDHU Smart Park
![smartparklogo_300x350](https://user-images.githubusercontent.com/25711110/184541676-4995be97-b415-47d6-90a3-60ae2853f5c8.png)


## Dependencies needed:
  1. pip install google-cloud-storage
  2. pip install opencv-python
  3. pip install numpy
  4. pip install firebase-admin
  5. pip install firebase
  6. pip install PySimpleGUI
  
## Introduction
NDHU Smart Park is smart parking project which makes use of obect detection and image processing techniques. It was made as a submission for the National Dong Hwa University's 3rd Year Project Exhibition.
## Motivation and Aim
The National Dong Hwa University is among one of the largest universities in Taiwan.  The University campus allows for two vehicular types on the premises; four (4) wheelers and two (2) wheelers. Two wheelers such as scooters and motorcycles have restrictions on the roads that they are allowed to ride on. As a result, it takes them longer to get to the main campus area where classes take place. On top of that, they are not allowed to park in the same parking spaces as cars and other four wheel vehicles and their parking spaces are severely limited, resulting in students taking forever to find parking and often being late to class.

The goal of NDHU Smart Park is to solve the issue of vehicular parking within the campus. It does so by providing the following:
- A mobile application students can use to check parking lot vacancies around campus.
- A flexible expandable administator program that can be used by administrators to create, edit and monitor various parking lots.
 
## Mobile Application
The mobile application was developed using the Flutter Framework and utilized Firebase for the backend. The application allows for real time checking of various parking lots on campus with the main goal being  students not having to drive to these parking lots only to find them full. 
The Firebase Firestore real-time database was used in order to provide the data shown in the application. Images of the application are shown below.
 ### Screenshots 

![image](https://user-images.githubusercontent.com/25711110/184539125-6520c316-2ae9-40fc-9f85-2a8ed218b79b.png)

*Start screen*

![image](https://user-images.githubusercontent.com/25711110/184539197-7e355339-ee8f-476a-a378-9843aef823ca.png)

*Vehicle type selector*


![image](https://user-images.githubusercontent.com/25711110/184539235-fbeb42ef-b6f3-4da9-b63c-ac19cacf9e1a.png)

*Select Parking Lot*

![image](https://user-images.githubusercontent.com/25711110/184539256-e6563e0f-a60b-4464-b71e-3b239745e82d.png)

*Parking lot viewer*

## Admin Program
The Admin Program was created in [Python](https://www.python.org/downloads/) and made use of various libraries and technologies such as [OpenCV](https://opencv.org/), [Firebase](https://firebase.google.com/?gclid=Cj0KCQjwuuKXBhCRARIsAC-gM0gyVX8AhCkz3S1fLaFDMK8ExsCTbXCrmgKYHFh8Ha2gD34GG2ah01QaAq0rEALw_wcB&gclsrc=aw.ds) and [Yolov3](https://viso.ai/deep-learning/yolov3-overview/#:~:text=YOLOv3%20AI%20models-,What%20is%20YOLOv3%3F,network%20to%20detect%20an%20object.). It allowed for authorized users to create/add new parking lots to the firestore database, edit the entries in the firestore databasse and enable live monitoring of the parking lot through OpenCV and YOLOv3. 
Screenshots can be found below.
### Screenshots

![image](https://user-images.githubusercontent.com/25711110/184539967-86314eb7-bea6-4467-b114-2c5aa4030727.png)

*Main Menu*
#### Creation Process
In order to create a parking lot, a picture of the parking lot must first be obtained. (The program relies on the use of a static camera to ensure that the placements of the lot in the imge also match the placement of lots in the video feed)


![image](https://user-images.githubusercontent.com/25711110/184540035-472ea33e-c762-428d-b1f9-dbf91ef5d048.png)

*Image Capture*

Once captured and saved, the admin can then go into the create menu and fill in the relevant information.
 

![image](https://user-images.githubusercontent.com/25711110/184540102-fd800a1e-cbec-4fef-8000-7bc3523b2d47.png)

*Create Menu*

What happens next differs on whether or not the admin selected manual selection or automatic selection.
(For simplicity of this readme I'll only show the automatic process in action)
With manual selection, the admin would have to outline the lots one by one using either a rectanle method or a flexible method which involves selecting the four (4) corner points of the parking spaces.

With the Automatic selection, the image is fed into a python program which automatically detects the parking spaces in the image.
Example

![image](https://user-images.githubusercontent.com/25711110/184540174-b21a7128-1604-42ee-9e65-28798fb0e90f.png)

The image on the left is a query screen for the admin to either keep the found parking space or discard it. The image on the right shows the confirmed parking spaces.

Once completed, a popup dialog appears informing the admin that the parking lot was successfully created.

### Monitoring Process
The monitoring process involves selecting the parking lot type the admin wishes to monitor and then the actual location. (The type determines the locations that appear)

![image](https://user-images.githubusercontent.com/25711110/184541461-4ac3e4d5-6b8c-4202-b9ff-1ecfa9dd385c.png)

![image](https://user-images.githubusercontent.com/25711110/184541483-3a6f97c0-0344-4e55-b1fe-fb1d01ad3751.png)



*Selection screens.*

The monitor feed will then appear. With the help of YOLOV3, any vehicle that is detected within the parking spaces will trigger an event; updating the database and the mobile application instantly. An example of this is shown below.

![image](https://user-images.githubusercontent.com/25711110/184541501-2e4a261d-aa80-4c15-88bd-764e5118b202.png)

![image](https://user-images.githubusercontent.com/25711110/184541521-1fd4c5b2-6d36-4cf9-a930-9ecc8de3dea3.png)


### Editing Process

The editing proocess provides two options:
 - Recapture-Best suited for if the camera was moved.
 - Editing a single parking space - Best suited for small modifications to the outline of the parking lot.

 ![image](https://user-images.githubusercontent.com/25711110/184540913-a641050e-03f9-4d12-b03b-8c9d53675a42.png)


 



