import math
import pypot.dynamixel as pdn

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
        dt = 0.1
        pos1 = dxl_io.get_present_position([self.id])
        time.sleep(dt)
        pos2 = dxl_io.get_present_position([self.id])
        delta_ang = (pos2-pos1)*math.pi/180
        self.w = delta_ang/dt