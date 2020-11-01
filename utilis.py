from djitellopy import Tello    #to access functions of the drone
import cv2                      #for image and video processing
import numpy as np


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
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #applies the classifier, which detect faces facing the camera
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                             #converts img to gray img
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)                      #scalefactor and minimum neighbors are parameters

    myFaceListC = []    #we create a list that will store the center of the faces
    myFaceListArea = [] #we create a list of the faces areas, because if the area of a face is the largest, we can conclude it is the closest (it's the best way for now with only
    # a camera

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)  #draws a rectangle around recogized faces (x,y) is starting corner of the rectangle (x+w,y+h) is the opposed corner
        # (0,0,255) is the color used for rectangle and 2 its thickness in pixels
        #return img #used to simply return simply the img to see faces in a picture, but now we want to detect te closest face
        cx = (x+w)//2 #center of x axis of face
        cy = (y+h)//2 #center of y axis of face
        area = w*h #area of face
        myFaceListArea.append(area) #we store the area of the face
        myFaceListC.append([cx,cy]) #we store the center of the face

    if len(myFaceListArea) !=0: #we check if any face is present, because some operations are impossible if the list of faces is empty

        i = myFaceListArea.index(max(myFaceListArea)) #we find the index of the closest face
        return img, [myFaceListC[i],myFaceListArea[i]] #if there is a face in the frame, we return the img and a tuple containing the center the closest face and its area
    else :
        return img,[[0,0],0] #if there is no face on the frame detected, we return 0 values for center and area
    
    def trackFace(myDrone,info,w,pid,pError):
        
        ##PID controller - helps smoothing movements as opposed to full correction movements
        error = info[0][0] - w//2 #we want the tracking to put the face in the center, so width divided by 2
        speed = pid[0]*error + pid[1]*(error-pError)
        speed = int(np.clip(speed, -100, 100)) #the speed will never go above or under 100
        print(speed) #for testing purposes
        
        if info[0][0] != 0: #if a face is detected
            myDrone.yaw_velocity = speed
        else :  #if no face is detected I would like the drone to not move or correct its orientation in any way
            myDrone.for_back_velocity = 0       #set velocity forward/backward to 0
            myDrone.left_right_velocity = 0     #set lateral velocity to 0
            myDrone.up_down_velocity = 0        #set vertical velocity to 0
            myDrone.yaw_velocity = 0
            error = 0
            
        if myDrone.send_rc_control : #sends the values of velocity to the computer
            myDrone.send_rc_control(myDrone.left_right_velocity,
                                   myDrone.for_back_velocity,
                                   myDrone.yaw_velocity)
            
        
        return error
            
