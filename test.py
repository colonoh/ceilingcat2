import cv2
import picamera
import picamera.array
import numpy as np
import time


with picamera.PiCamera() as camera:
    #camera.start_preview()
    time.sleep(2)
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr', use_video_port=True)
        # At this point the image is available as stream.array
        image = stream.array
        stream.truncate(0)


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('test.jpg', gray)
        cv2.imwrite('color.jpg', image)
