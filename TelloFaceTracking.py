from utilis import *
import cv2

w,h = 360,240


myDrone = initializeTello()

while True:
    #step 1
    img = telloGetFrame(myDrone,w,h)

    #step 2
    img, info = findFace(img)
    print(info[0][0])

    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
