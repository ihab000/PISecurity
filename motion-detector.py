# Write your code here :-)
import time
import os

from gpiozero import MotionSensor
from picamera import PiCamera

pir = MotionSensor(4)
camera = PiCamera()

cwd = os.getcwd()  # Get the current working directory (cwd)

while True:
    pir.wait_for_motion()
    print("Motion DETECTED!")
    camera.capture("/home/pi/Assignment2/doorPhotos/testing.jpg")
    time.sleep(5)
    
camera.close()