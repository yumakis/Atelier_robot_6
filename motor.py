import math

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