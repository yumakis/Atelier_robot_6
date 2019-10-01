import sys
import numpy as np
import cv2
import matplotlib as plt
import pypot
import time
from robot import Robot

def main():
    robot = Robot()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Killed by user')
        sys.exit(0)