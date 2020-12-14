import cv2


def getFrame(drone, w, h):  # w is width of image, h is height of image
    droneFrame = drone.get_frame_read()  # reads to feed sent by drone
    droneFrame = droneFrame.frame  # converts it to a frame object
    img = cv2.resize(droneFrame, (w, h))  # resizes the frame to take in the set width and height
    return img