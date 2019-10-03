from motor import Motor
from math import *
import time

class Robot():
    #Each dt we analyze one frame of the video dt (t+1 = t + dt)
    dt = 0.100 #en secondes
    baseSpeed = 10 #vitesse en rpm

    coeff = 0.05 #coefficient de coubure

    def __init__(self):
        #coordonnees du robot dans le repere du monde
        self.x = 0
        self.y = 0
        self.theta = 0

        #vitesse lineaire dans le repere du monde en m/s
        self.vLin = 0
        #vitesse angulaire dans le repere du monde rad/s
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
        # print("DK vG", vG)
        vD = self.motorRight.w
        # print("DK vD", vD)

        if(vG>0 and vD>0): #on tourne a droite en avancant
            self.vLin = Motor.R*(vG - vD) / 2
            # print("DK vLin", self.vLin)
            self.vTheta = - Motor.R*(vG + vD) / (self.d)
        else:
            if(vG<=0 and vD<=0): #on tourne a gauche en avancant
                self.vLin = Motor.R*(vG - vD) / 2
                # print("DK vLin", self.vLin)
                self.vTheta = - Motor.R*(vG + vD) / (self.d)
            else: #on avance ou on recule en ligne droite
                self.vLin = Motor.R*(vG - vD) / 2
                # print("DK vLin", self.vLin)
                self.vTheta = Motor.R*(vG + vD) / (self.d)
                # print("DK vTheta", self.vTheta)

    def odom(self):
        #calcule les deplacements dX, dY, et dTheta entre les instants t et t + dt dans le repere du robot
        self.dTheta = self.vTheta * Robot.dt
        # print("odom dTheta", self.dTheta)
        dL = self.vLin * Robot.dt
        # print("odom vLin", self.vLin)
        #projection du deplacement dL dans le repere monde
        self.dx = dL * cos(self.theta + self.dTheta)
        # print("odom dx", self.dx)
        self.dy = dL * sin(self.theta + self.dTheta)
        # print("odom dy", self.dy)

    def tick_odom(self):
        #MAJ des parametres dans le repere monde
        self.DK()
        self.odom()
        self.x += self.dx
        # print("tick_odom x", self.x)
        self.y += self.dy
        # print("tick_odom y", self.y)
        self.theta += self.dTheta
        self.theta = self.theta%(2*pi)
        # print("tick_odom theta", self.theta)

    #speed in parametres is in rpm
    def move_straight_forward(self, speed):
        motorG = self.motorLeft
        motorD = self.motorRight
        Motor.dxl_io.set_moving_speed({motorG.id : speed, motorD.id : -speed})
        speed = Motor.rpmToRps(motorG, speed)
        motorG.w = speed
        motorD.w = -speed

    def move_straight_backward(self, speed):
        motorG = self.motorLeft
        motorD = self.motorRight
        Motor.dxl_io.set_moving_speed({motorG.id : -speed, motorD.id : speed})
        speed = Motor.rpmToRps(motorG, speed)
        motorG.w = -speed
        motorD.w = speed


    #Convert linear speed and angular speed into speed for Left engine and Right engine
    #d is the distance between the two wheels. It s given in the Robot class
    #vLin, vTheta are linear speed and angular speed of the Robot. They are given in the Robot Class
    def IK(self):
        vLin = self.vLin
        # print("IK vLin", vLin)
        vTheta = self.vTheta
        # print("IK vTheta", vTheta)
        d = self.d
        if(vTheta<=0): #on tourne a droite
            self.motorLeft.w = (vLin - vTheta*d/2) / Motor.R
            # print("IK self.motorLeft.w", self.motorLeft.w)
            self.motorRight.w  = - (vLin + vTheta*d/2) / Motor.R
            # print("IK self.motorRight.w", self.motorRight.w)
        else: #on tourne a gauche
            self.motorLeft.w = - (vLin + vTheta*d/2) / Motor.R
            self.motorRight.w  = (vLin - vTheta*d/2) / Motor.R


    #Based on speeds given by IK we set the speed of each motor
    def move(self, vG, vD):
        motorG = self.motorLeft
        motorD = self.motorRight
        Motor.dxl_io.set_moving_speed({motorG.id : vG, motorD.id : vD})
        vG = Motor.rpmToRps(motorG, vG)
        vD = Motor.rpmToRps(motorD, vD)
        motorG.w = vG
        motorD.w = vD

    def stop(self):
        self.move(0,0)

    #alpha : orientation of the robot. Depending of its sign we rotate the robot toward left or right
    def rotate(self, alpha):
        # print("rotate alpha", alpha)
        if alpha > 0: #on tourne à gauche
            self.move(-Robot.baseSpeed, -Robot.baseSpeed)
        else:
            if alpha < 0 : #on tourne à droite
                self.move(Robot.baseSpeed, Robot.baseSpeed)

    def calc_alpha(self, x_c, y_c):
        x_0 = self.x
        y_0 = self.y
        if((abs(x_c)-abs(x_0)) < 0):
            alpha = atan((y_c - y_0)/(x_c - x_0))%(2*pi) + pi
        elif((abs(x_c)-abs(x_0)) > 0):
            alpha = atan((y_c - y_0)/(x_c - x_0))%(2*pi)
        else:
            if((abs(y_c)-abs(y_0)) < 0):
                alpha = -pi/2
            elif((abs(y_c)-abs(y_0)) > 0):
                alpha = pi/2
            else:
                alpha = 0
        return alpha

    def go_to_xya(self,x_c, y_c, theta_c):
        self.tick_odom()
        x_0 = self.x
        y_0 = self.y
        #angle en rad de rotation dans le repere monde signe
        alpha = self.calc_alpha(x_c, y_c)
        print("goto alpha", alpha, "theta", self.theta, "diff:", self.theta - alpha)
        #on effectue la boucle tant qu on la position du robot ne correspond pas a la cible

        while(abs(abs(self.theta)-abs(alpha)) > 0.05):
            print("goto self.theta",self.theta)
            print("goto abs(alpha)", abs(alpha))
            self.rotate(alpha)
            self.tick_odom()
            time.sleep(Robot.dt)
            # print(self.theta)
        while((abs((abs(self.x) - abs(x_c))) > 0.05) and (abs((abs(self.y) - abs(y_c))) > 0.05)):
            print("goto abs(self.x)", abs(self.x), "goto abs(x_c)", abs(x_c))
            print("goto abs(self.y)", abs(self.y), "goto abs(y_c)", abs(y_c))
            print("vLin:", self.vLin)
            self.move_straight_forward(Robot.baseSpeed)
            self.tick_odom()
            time.sleep(Robot.dt)
        while(abs(abs(self.theta)-abs(theta_c)) > 0.05):
            print("goto abs(self.theta - alpha)", abs(self.theta - alpha))
            print("goto abs(theta_c)",theta_c)
            self.rotate(theta_c-self.theta)
            self.tick_odom()
            time.sleep(Robot.dt)
        self.move(0, 0)
