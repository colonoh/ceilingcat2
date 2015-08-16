import cv2
import picamera
import picamera.array
import numpy as np
import time
import datetime

avg = None

with picamera.PiCamera() as camera:
    camera.framerate = 24
    camera.resolution = (1024, 768)
    #camera.led = False
    time.sleep(2)
    camera.shutter_speed = 10000
    camera.exposure_mode = 'off'
    with picamera.array.PiRGBArray(camera) as stream:
        #camera.capture(stream, format='bgr', use_video_port=True)
        for f in camera.capture_continuous(stream, format="bgr", use_video_port=True):
            print('capture')
            isMotion = False
            image = f.array
            timestamp = datetime.datetime.now()
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            stream.truncate(0)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #gray = cv2.GaussianBlur(gray, (21, 21), 0)


            if avg is None:
                avg = gray.copy().astype("float")


            cv2.accumulateWeighted(gray, avg, 0.5)

            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
            ret,thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)
            #thresh = cv2.dilate(thresh, None, iterations=2)



            _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for c in contours0:
                (x, y, w, h) = cv2.boundingRect(c)
                if (x, y, w, h) != (0,0,0,0):
                    if cv2.contourArea(c) > 30:
                        print(x, y, w, h)
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        isMotion = True

            if isMotion is True:
                cv2.imwrite('avg {}.jpg'.format(ts), avg)
                cv2.imwrite('thresh {}.jpg'.format(ts), thresh)
                cv2.imwrite('frameDelta {}.jpg'.format(ts), frameDelta)
                cv2.imwrite('{}.jpg'.format(ts), image)
                print('Found motion! {}'.format(ts))
