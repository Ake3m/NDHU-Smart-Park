import cv2 as cv
import json
from firebase_admin import credentials, initialize_app, storage


def monitor():
    pass


def edit():
    pass


def create():
    print("What would you like to name this parking lot?")
    parking_lot_name = input()
    print("In order to create a parking lot, perform the following steps.")
    print("1. Place a sample image of the parking lot in the \"Samples\" folder.\n2. Take a sample of one of the parking spaces.\n3. Outline the parking lot by clicking the top left of each lot.\n\t -Left click to add\n\t -Right click to remove\n4. Press \"s\" to save, \"q\" to quit.")
    print("Is the sample image already in the folder? (Y/N)")
    selectPhoto=True
    while(True)
    ans=input()
    if ans =='N' or ans=='n' or ans=='No' or ans=='no':
        pass
    elif ans =='Y' or ans=='y' or ans=='Yes' or ans=='yes':
        pass



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
