import picamera
import picamera.array
import numpy as np
import datetime, time
import urllib.request
import boto3

s3 = boto3.resource('s3')
motionDetected = 0 # counter contains current number of motion-detected frames (up to a limit)

# currently checks for my presence by checking the router for my phone's MAC address
def phonePresent(): # don't care for the name
    routerAddress = 'http://10.0.0.1/'
    username = 'admin'
    password = 'password'
    phoneAddress = '00:11:94:BA:49:3C'

    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, routerAddress, username, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib.request.build_opener(handler)

    # use the opener to fetch a URL
    response = opener.open(routerAddress + '/DEV_device.htm')
    data = response.read().decode('utf-8')

    # search the HTML source for my MAC address, if it returns -1 it means it didn't find it
    if data.find(phoneAddress) == -1:
        return False
    else:
        print('Phone is present.')
        return True


class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        global motionDetected
        a = np.sqrt(np.square(a['x'].astype(np.float)) + np.square(a['y'].astype(np.float))).clip(0, 255).astype(np.uint8)
        # If there're more than X vectors with a magnitude greater than Y, then say we've detected motion
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
    camera.start_recording('/dev/null', format='h264', motion_output=MyMotionDetector(camera)) # throw out actual video stream, just use sthe motion_output

    counter = -1
    iAmHere = False
    print('Started!')
    while True:
        filename = ''
        if counter < 0:
            iAmHere = phonePresent()
            counter = 300
        else:
            counter -= 1
        if motionDetected > 3. and not iAmHere: # trigger recording if there is enough motion
            filename = '{}.h264'.format(datetime.datetime.now())
            camera.start_recording(filename, splitter_port=2, intra_period=3)

            while motionDetected > 0.: # while there is motion
                camera.annotate_text = str(datetime.datetime.now())
                camera.wait_recording(.1,splitter_port=2)

            # no more motion
            camera.stop_recording(splitter_port=2)
            print('Done recording')
            # upload to s3
            print('Start uploading')
            data = open(filename, 'rb')
            s3.Bucket('qvqcbwk5').put_object(Key=filename, Body=data)
            print('Done uploading')

        # if there isn't motion
        camera.wait_recording(.05)

    # done
    camera.stop_recording()
