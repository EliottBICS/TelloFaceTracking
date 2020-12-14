



def trackFaceDetect(drone, info, w, pid, previousCorrection, dtime):

    correction = info[0][0] - w//2 #correction is difference between x value of face and center of frame
    pid = [0.3, 0, 0.1] #proportional integral, derivative
    yaw = pid[0] * correction + pid[2] * (correction - previousCorrection) / dtime + 50 #we take into account the proportional action and derivative action
    #derivative action applies a degree of control on the drone (slower movements) while proportional action is more responsive
    #but could result into an overcorrecting situation where the drone moves too much and has to correct after.
    #for derivative, we take derivative of correction divided by time since last frame
    #yaw = int(np.clip(yaw, -75, 75)) #we control the yaw, we never want the drone to go faster than 1m/s
    if yaw > 75:
        yaw = 75
    elif yaw < -75:
        yaw = 75
    print("yaw", yaw) #testing purposes

    if info[0][0] != 0: #if a face is detected
        drone.yaw_velocity = yaw #drone rotates to follow it
    else : #if no face is detected
        drone.yaw_velocity = 0 #drone stops rotating
        correction=0

    #if drone.send_rc_control :
        #drone.send_rc_control(drone.yaw_velocity)

    return correction