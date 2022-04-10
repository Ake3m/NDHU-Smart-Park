from turtle import home
import PySimpleGUI as sg
import cv2 as cv
from numpy import size


theme_data = {'BACKGROUND': '#4CC18A',
              'TEXT': '#fff',
              'INPUT': '#c7e78b',
              'TEXT_INPUT': '#000000',
              'SCROLL': '#c7e78b',
              'BUTTON': ('white', '#12A460',),
              'PROGRESS': ('#01826B', '#D0D0D0'),
              'BORDER': 2,
              'SLIDER_DEPTH': 0,
              'PROGRESS_DEPTH': 0}

# Add your dictionary to the PySimpleGUI themes
sg.theme_add_new('MyNewTheme', theme_data)

# Switch your theme to use the newly added one. You can add spaces to make it more readable
sg.theme('Dark')

img_path = './ParkingLotManager/assets/smartparklogo_300x350.png'



home_layout = [[sg.Image(img_path, )], [sg.Text('Welcome to NDHU Smart Park', size=(35, 1), justification='center')], [
    sg.Text('What would you like to do?', size=(35, 1), justification='center')],[sg.Button('Monitor Parking Lot')]]


window = sg.Window('NDHU SMART PARK', [home_layout])

event, values = window.read()
window.close()
