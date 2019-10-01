
class Robot():
    #coordonnées du robot dans le repère du monde
    x = 0
    y = 0
    theta = 0

    #vitesse linéaire dans le repère du monde
    vLin = 0
    #vitesse angulaire dans le repère du monde
    vTheta = 0

    #coordonnées du robot dans le repère robot à l'instant t
    #on analyse une image de la vidéo tous les dt (t+1 = t + dt)
    dx = 0
    dy = 0
    dTheta = 0

    