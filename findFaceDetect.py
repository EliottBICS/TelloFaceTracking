import cv2

def findFaceDetect(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #loads the Classifier, which will detect faces facing the camera
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converts img to gray img - needed for faces detection
    faces = faceCascade.detectMultiScale(imgGray, 1.05, 5) #scalefactor = 1.1 minimum neighbor = 4

    myFaceListC = [] #we create a list that will store the center of the faces
    myFaceListArea = [] #in detect approach, we will use the area of the faces to treat the situations where multiple faces are detected

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2) #draws a rectangle around recognized faces (x, y) is the top left corner
        #(0, 0, 255) is the color of the rectangle, 2 is the width of the rectangle's lines
        cx = (x + w)//2 #center of face x axis
        cy = (y + h)//2 #center of face y axis
        area = w*h #area of face
        myFaceListArea.append(area) #we store the area of the faces
        myFaceListC.append([cx, cy]) #we store center of the faces

    if len(myFaceListArea) != 0: #check if at least a face is detected

        i = myFaceListArea.index(max(myFaceListArea)) #find the index of the largest face
        return img, [myFaceListC[i], myFaceListArea[i]] #return ing and tuple containing center of the closest face and its area
    else :
        return img, [[0, 0], 0] #if there is no face detected, we return 0 values for center and area
