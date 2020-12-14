from getFrame import *
from getDrone import *
from findFaceDetect import *
from trackFaceDetect import *
import cv2
import timeit

w, h = 720, 720 #input here the size of the window that opencv will display tello streams 720p
pid = [0.3, 0, 0.1]  # proportional, integral, derivative actions - We can change here those settings to manipulate
#the way the drone compensates errors - I choose to let ki to 0 to prevent oscillation and because speed is already
#satisfactory
previousCorrection = 0
startCounter = 0  # To stay on ground set to 0, to take off, set to 1
detect = True #true means in detect mode, false in tracking mode
previousTime = 0

drone = getDrone()

# Take off
if startCounter == 1:
    drone.takeoff()
    startCounter = 1

while True:
    time = timeit.default_timer()
    dtime = time - previousTime
    previousTime = time

    img = getFrame(drone, w, h)

    img, info = findFaceDetect(img)

    previousCorrection = trackFaceDetect(drone, info, w, pid, previousCorrection, dtime)
    print(info[0][0]) #prints cx value for testing



    cv2.imshow('Image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # if the Q key is pressed
        drone.land()  # we make the drone land
        break