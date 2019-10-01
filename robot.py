from motor import Motor

class Robot():
    #on analyse une image de la vidéo tous les dt (t+1 = t + dt)
    dt = 100 #en millisecondes
    motorRight = Motor(2)
    motorLeft = Motor(1)

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
    
    def tick_odom(self):

