from utilis import *
import cv2

w,h = 360,240


myDrone = initializeTello() #it initialises the drone, meaning we now have a drone with its feed perceived, a set speed (0) and a battery level

while True:
    #step 1
    img = telloGetFrame(myDrone,w,h)

    #step 2
    img, info = findFace(img)
    print(info[0][0]) #prints the first element of the tuple representing the center of the face (it will be its cx value)

    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'): #if the Q key is pressed
        myDrone.land()                    #we make the drone land
        break
