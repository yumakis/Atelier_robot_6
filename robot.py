from motor import Motor
from math import *
import time

class Robot():
    #on analyse une image de la vidéo tous les dt (t+1 = t + dt)
    dt = 0,100 #en secondes
    baseSpeed = 10 #vitesse en rpm

    def __init__(self):
        #coordonnées du robot dans le repère du monde
        self.x = 0
        self.y = 0
        self.theta = 0

        #vitesse linéaire dans le repère du monde
        self.vLin = 0
        #vitesse angulaire dans le repère du monde
        self.vTheta = 0

        #coordonnées du robot dans le repère robot à l'instant t
        self.dx = 0
        self.dy = 0
        self.dTheta = 0

        #instanciation des 2 moteurs
        self.motorRight = Motor(2)
        self.motorLeft = Motor(1)

        #distance entre les 2 roues du robot en mètres
        self.d = 0.165

    def DK(self):
        #convertit les vitesses angulaires (rad/s) du moteur gauche vG et du moteur droit vD dans le repère monde
        #en vitesses linéaire (m/s) vLin et vitesse angulaire (rad/s) vTheta dans le repère monde
        vG = self.motorLeft.w
        vD = self.motorRight.w
        self.vLin = Motor.R*(vG + vD) / 2
        self.vTheta = Motor.R*(vG - vD) / (2 * self.d)

    def odom(self):
        #calcule les déplacements dX, dY, et dTheta entre les instants t et t + dt dans le repère du robot
        self.dTheta = self.vTheta * Robot.dt
        dL = self.vLin * Robot.dt
        #projection du déplacement dL dans le repère monde
        self.dx = dL * cos(self.theta + self.dTheta)
        self.dy = dL * sin(self.theta + self.dTheta)

    def tick_odom(self):
        #MAJ des paramètres dans le repère monde
        self.DK()
        self.odom()
        self.x += self.dx
        self.y += self.dy
        self.theta += self.dTheta
    
    def move_straight_forward(self, speed):
        motorG = self.motorLeft
        motorD = self.motorRight
        dxl_io.set_moving_speed({motorG.id : speed, motorD.id : -speed})
        motorG.w = speed
        motorD.w = -speed
    
    def move_straight_backward(self, speed):
        motorG = self.motorLeft
        motorD = self.motorRight
        dxl_io.set_moving_speed({motorG.id : -speed, motorD.id : speed})
        motorG.w = -speed
        motorD.w = speed
    
    
    #Convert linear speed and angular speed into speed for Left engine and Right engine
    #d is the distance between the two wheels. It's given in the Robot class
    #vLin, vTheta are linear speed and angular speed of the Robot. They are given in the Robot Class
    def IK(self):
        vLin = self.vLin
        vTheta = self.vTheta
        d = self.d
        self.motorLeft.w = (vLin + vTheta*d/2) / Motor.R
        self.motorRight.w  = (vLin - vTheta*d/2) / Motor.R
    
    #Based on speeds given by IK we set the speed of each motor
    def move(self, vG, vD):
        motorG = self.motorLeft
        motorD = self.motorRight
        dxl_io.set_moving_speed({motorG.id : vG, motorD.id : vD})
        motorG.w = vG
        motorD.w = vD 
        
    def rotate(self, alpha):
        if alpha > 0:
            self.move(-Robot.baseSpeed, -Robot.baseSpeed)
        else:
            self.move(Robot.baseSpeed, Robot.baseSpeed)
    
    def go_to_xya(x_c, y_c, theta_c):
        alpha = tan(y_c/x_c)
        l = sqrt(pow(x_c, 2) + pow(y_c, 2))
        #on effectue la boucle tant qu'on la position du robot ne correspond pas a la cible
        while(self.theta != alpha):
            self.rotate(alpha)
            self.tick_odom()
        
                
                
            
            
