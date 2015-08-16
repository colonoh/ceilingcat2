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

        #image = cv2.imread('circle.jpg')


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        #thresh = cv2.dilate(thresh, None, iterations=2)
        cv2.imwrite('thresh.jpg', thresh)
        _, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours0:
            (x, y, w, h) = cv2.boundingRect(c)
            if (x, y, w, h) != (0,0,0,0):
                if cv2.contourArea(c) > 30:
                    print(x, y, w, h)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.putText(image, "LOL", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imwrite('test.jpg', image)
