# ceilingcat2
Motion-based security system using Raspberry Pi camera module

##Notes
- originally used capture instead of recording but framerate was too low
- originally subtracted difference frames from average to determine motion
- now using motion_output based on encoder motion estimation
- sensitivity based on number of vectors and magnitude
- increased key frame rate to try and increase ability to extract usable images from frames
- added frame counter to ignore spurious events and extend recording of large-motion events
- checks for presence by checking router for phone's MAC address
- email notifications provided by Amazon SNS (notification on new item in bucket)
- TODO: add immediate(?) uploading of videos


##References

- http://picamera.readthedocs.org/en/release-1.10/
- http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
