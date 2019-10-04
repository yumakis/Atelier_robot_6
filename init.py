import sys
import numpy as np
import cv2
import matplotlib as plt
import pypot
import time
from robot import *
from motor import *
from capture import *


def main():
    robot = Robot()
    lx, ly = vision()
    robot.stop()
    # robot.draw_ride(lx,ly)
    time.sleep(10)

    lx, ly = robot.odometry()
    # robot.draw_ride(lx,ly)
    time.sleep(5)

    robot.start()
    lx, ly = robot.go_to_xya(1,1,3.14/2)
    # robot.draw_ride(lx,ly)
    # robot.go_to_xya(0,0,0)
    # robot.go_to_xya(-1,-1,3.14/4)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Killed by user')
        sys.exit(0)