import math
import pypot.dynamixel as pdn

class Motor():
    #la vitesse en rpm des moteurs est un multiple de ce coeff
    COEFF = 1.339
    #rayon de la roue du robot en mètres
    R = 0.026

    def __init__(self, id):
        self.id = id
        #vitesse angulaire du robot en rad/s
        self.w = 0

    def rpmToRps(self,rpm):
        #rpm = round per minute to rps = rad per second
        return rpm*2*math.pi*Motor.R / 60

    def rpsToRpm(self, rps):
        #rps = rad per second to rpm = round per minute
        return rps*60 / 2*math.pi*Motor.R


#initiate dxl_io

ports = pdn.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pdn.DxlIO(ports[0])

def move_straight_forward(motorG, motorD, speed):
    motorG.w = speed
    motorD.w = -speed
    speed = motorG.rpsToRpm(speed)
    dxl_io.set_moving_speed({motorG.id : speed, motorD.id : -speed})


def move_straight_backward(motorG, motorD, speed):
    motorG.w = -speed
    motorD.w = speed
    speed = motorG.rpsToRpm(speed)
    dxl_io.set_moving_speed({motorG.id : -speed, motorD.id : speed})


#Convert linear speed and angular speed into speed for Left engine and Right engine
#d is the distance between the two wheels. It's given in the Robot class
#vLin, vTheta are linear speed and angular speed of the Robot. They are given in the Robot Class
#vG, vD are in radps
def IK(vLin, vTheta, d):
    (vG, vD) = (0, 0)

    vG = (vLin + vTheta*d/2) / Motor.R
    vD = (vLin - vTheta*d/2) / Motor.R

    return vG, vD

#Based on speeds given by IK we set the speed of each motor
def move(motorG, motorD, vG, vD):
    motorG.w = vG
    motorD.w = vD
    vG = Motor.rpsToRpm(vG)
    vD = Motor.rpsToRpm(vD)
    dxl_io.set_moving_speed({motorG.id : vG, motorD.id : vD})


def rotate(motorG, motorD, speed):
    dxl_io.set_moving_speed({motorG.id : speed, motorD.id : speed})

def stop(motorG, motorD):
    dxl_io.set_moving_speed({motorG.id : 0, motorD.id : 0})



def Test():
    print("test")
