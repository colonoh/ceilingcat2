import cv2
import picamera
import numpy as np
import time


with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    #camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture('foo.jpg')
