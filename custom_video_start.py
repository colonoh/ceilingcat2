import picamera
import picamera.array
import numpy as np
import datetime, time

outputPath = '/dev/null'

class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        timestamp1 = time.time()
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        global outputPath
        #print((a>10).sum())
        if (a > 10).sum() > 10:
            #print('Motion detected!')
            outputPath = 'data.h264'
        else:
            outputPath = '/dev/null'
        timestamp2 = time.time()
        #print(timestamp2-timestamp1)

startTime = time.time() # time that camera turned on
with picamera.PiCamera() as camera:
    camera.resolution = (1296, 972)
    camera.framerate = 30
    time.sleep(2)
    camera.iso = 800
    camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera))
    recordingMotion = False # currently recording or not

    print('Started!')
    while time.time() - startTime < 20:
        timestamp = datetime.datetime.now()

        # if there is motion
        if outputPath == 'data.h264' and time.time() - startTime > 3:
            #camera.split_recording('{}.h264'.format(timestamp), format='h264', motion_output=MyMotionDetector(camera))
            camera.start_recording('{}.h264'.format(timestamp), splitter_port=2, intra_period=3)

            # while there is motion
            while(outputPath == 'data.h264'):
                camera.annotate_text = str(datetime.datetime.now())
                camera.wait_recording(1,splitter_port=2)

            # no more motion
            camera.stop_recording(splitter_port=2)
            print('Done recording')

        # if there isn't motion
        camera.wait_recording(.05)

    # done
    camera.stop_recording()
