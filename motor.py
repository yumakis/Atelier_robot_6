import math
import pypot.dynamixel as pdn
import time

class Motor():
    #la vitesse en rpm des moteurs est un multiple de ce coeff
    COEFF = 1.339
    #rayon de la roue du robot en metres
    R = 0.026

    dxl_io = pdn.DxlIO(pdn.get_available_ports()[0])

    def __init__(self, id):
        self.id = id
        #vitesse angulaire du robot en rad/s
        self.w = 0

    def rpmToRps(self,rpm):
        #rpm = round per minute to rps = rad per second
        return rpm*Motor.COEFF*2*math.pi / 60

    def rpsToRpm(self, rps):
        #rps = rad per second to rpm = round per minute
        return rps*60 / 2*math.pi

    def calc_speed_motor(self):
        dt = 0.05
        pos1 = Motor.dxl_io.get_present_position([self.id])
        time.sleep(dt)
        pos2 = Motor.dxl_io.get_present_position([self.id])
        delta_ang = (pos2[0]-pos1[0])*math.pi/180
        if(abs(delta_ang) > 300):
            deltaPos1 = 0
            deltaPos2 = 0
            if(pos1[0] < 0):
                deltaPos1 = -180 - pos1[0]
                deltaPos2 = 180 - pos2[0]
            else: #if(pos1[0] >= 0)
                deltaPos1 = 180 - pos1[0]
                deltaPos2 = -180 - pos2[0]
            if(delta_ang > 0):
                delta_ang = deltaPos1 + deltaPos2
            else:
                delta_ang = - deltaPos1 - deltaPos2
        print(self.id," en rad ",pos1[0])
        print(self.id," en rad ",pos2[0])
        print(self.id," delta angle ",delta_ang)
        self.w = - delta_ang/dt
        print(self.id," vit angulaire ",self.w)