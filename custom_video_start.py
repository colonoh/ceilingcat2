import picamera
import picamera.array
import numpy as np
import datetime, time

motionDetected = 0 # counter contains current number of motion-detected frames (up to a limit)

class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        global motionDetected
        a = np.sqrt(np.square(a['x'].astype(np.float)) + np.square(a['y'].astype(np.float))).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater than 50, then say we've detected motion
        if (a > 20).sum() > 20:
            if motionDetected < 6.:
                motionDetected += 1. # add because motion was detected
        else:
            if motionDetected > 0.:
                motionDetected -= .1 # subtract because of lack of motion

startTime = time.time() # time that camera turned on
with picamera.PiCamera() as camera:
    camera.resolution = (1296, 972)
    camera.framerate = 30
    time.sleep(2)
    camera.iso = 800
    camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))

    print('Started!')
    while time.time() - startTime < 20:
        if motionDetected > 3.: # trigger recording if there is enough motion
            camera.start_recording('{}.h264'.format(datetime.datetime.now()), splitter_port=2, intra_period=3)

            while motionDetected > 0.: # while there is motion
                camera.annotate_text = str(datetime.datetime.now())
                camera.wait_recording(.1,splitter_port=2)

            # no more motion
            camera.stop_recording(splitter_port=2)
            print('Done recording')

        # if there isn't motion
        camera.wait_recording(.05)

    # done
    camera.stop_recording()
