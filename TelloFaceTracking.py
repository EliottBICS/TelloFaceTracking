from utilis import *
import cv2

w,h = 360,240
pid = [0.5,0.5,0] # [kp, kd, ki]
pError = 0
startCounter = 0 #To stay on ground set to 1, to take off, set to 0


myDrone = initializeTello() #it initialises the drone, meaning we now have a drone with its feed perceived, a set speed (0) and a battery level

while True:
    
    #Take off
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1
        
    #step 1
    img = telloGetFrame(myDrone,w,h)

    #step 2
    img, info = findFace(img)
    
    #step 3
    pError = trackFace(myDrone, info,w,pid,pError)
    print(info[0][0]) #prints the first element of the tuple representing the center of the face (it will be its cx value)

    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'): #if the Q key is pressed
        myDrone.land()                    #we make the drone land
        break
