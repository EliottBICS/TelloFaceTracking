from djitellopy import Tello  # to access functions of the drone


def getDrone():
    drone = Tello()  # define drone as a Tello object to apply specific functions to it
    drone.connect()
    drone.for_back_velocity = 0  # set velocity forward/backward to 0
    drone.left_right_velocity = 0  # set lateral velocity to 0
    drone.up_down_velocity = 0  # set vertical velocity to 0
    drone.yaw_velocity = 0  # set yaw (turning) velocity to 0
    drone.speed = 0
    print(f"Percentage of battery :{drone.get_battery()}")  # displays current battery percentage of drone - useful when testing
    drone.streamoff() # turns off the video feed sent by drone - Usefull if previous test's stream is still ongoing
    drone.streamon()  # turns on the video feed - with last line, this effectively resets the stream
    return drone