from motor import Motor
from math import *
import time

class Robot():
    #Each dt we analyze one frame of the video dt (t+1 = t + dt)
    dt = 0,100 #en secondes
    baseSpeed = 10 #vitesse en rpm

    def __init__(self):
        #coordonnees du robot dans le repere du monde
        self.x = 0
        self.y = 0
        self.theta = 0

        #vitesse lineaire dans le repere du monde
        self.vLin = 0
        #vitesse angulaire dans le repere du monde
        self.vTheta = 0

        #coordonnees du robot dans le repere robot  a l instant t
        self.dx = 0
        self.dy = 0
        self.dTheta = 0

        #instanciation des 2 moteurs
        self.motorRight = Motor(2)
        self.motorLeft = Motor(1)

        #distance entre les 2 roues du robot en metres
        self.d = 0.165

    def DK(self):
        #convertit les vitesses angulaires (rad/s) du moteur gauche vG et du moteur droit vD dans le repere monde
        #en vitesses lineaire (m/s) vLin et vitesse angulaire (rad/s) vTheta dans le repere monde
        vG = self.motorLeft.w
        vD = self.motorRight.w
        self.vLin = Motor.R*(vG + vD) / 2
        self.vTheta = Motor.R*(vG - vD) / (2 * self.d)

    def odom(self):
        #calcule les deplacements dX, dY, et dTheta entre les instants t et t + dt dans le repere du robot
        self.dTheta = self.vTheta * Robot.dt
        dL = self.vLin * Robot.dt
        #projection du deplacement dL dans le repere monde
        self.dx = dL * cos(self.theta + self.dTheta)
        self.dy = dL * sin(self.theta + self.dTheta)

    def tick_odom(self):
        #MAJ des parametres dans le repere monde
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
    #d is the distance between the two wheels. It s given in the Robot class
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

    #alpha : orientation of the robot. Depending of its sign we rotate the robot toward left or right
    def rotate(self, alpha):
        if alpha > 0:
            self.move(-Robot.baseSpeed, -Robot.baseSpeed)
        else:
            self.move(Robot.baseSpeed, Robot.baseSpeed)

    def go_to_xya(self,x_c, y_c, theta_c):
        alpha = tan(y_c/x_c)
        #on effectue la boucle tant qu on la position du robot ne correspond pas a la cible
        while(abs(self.theta) <= abs(alpha)):
            self.rotate(alpha)
            self.tick_odom()
        while((abs(self.x) <= abs(x_c)) and (abs(self.y) <= abs(y_c))):
            self.move_straight_forward(Robot.baseSpeed)
            self.tick_odom()
        while(abs(self.theta - alpha) <= abs(theta_c)):
            self.rotate(theta_c)
            self.tick_odom()
