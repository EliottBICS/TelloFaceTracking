from djitellopy import Tello    #to access functions of the drone
import cv2                      #for image and video processing


def initializeTello():
    myDrone = Tello()           #define myDrone as a Tello object to apply specific functions to it
    myDrone.connect()
    myDrone.for_back_velocity = 0       #set velocity forward/backward to 0
    myDrone.left_right_velocity = 0     #set lateral velocity to 0
    myDrone.up_down_velocity = 0        #set vertical velocity to 0
    myDrone.yaw_velocity = 0            #set yaw (turning) velocity to 0
    myDrone.speed = 0                   
    print(myDrone.get_battery())        #displays current battery percentage of drone - usefull when testing
    myDrone.streamoff()                 #turns off the video feed sent by drone - Usefull if previous test's stream is still ongoing
    myDrone.streamon()                  #turns on the video feed - with last line, this effectively resets the stream
    return myDrone

def telloGetFrame(myDrone, w = 360, h = 240):   #w is width of image, h is height of image
    myFrame = myDrone.get_frame_read()          #reads to feed sent by drone
    myFrame = myFrame.frame                     #converts it to a frame object
    img = cv2.resize(myFrame,(w,h))             #resizes the frame to take in account the arguments of this function
    return img                                  

def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #applies the classifier
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                             #converts img to gray img
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)                      #scalefactor and minimum neighbors are parameters

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = (x+w)//2
        cy = (y+h)//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])

    if len(myFaceListArea) !=0:

        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]]
    else :
        return img,[[0,0],0]
