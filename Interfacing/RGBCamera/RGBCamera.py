"""
NAME: RGBCamera.py
AUTHOR: John Archibald Page
DATE CREATED: 08/12/2022 
DATE LAST UPDATED: 08/12/2022

PURPOSE:
To write functionality to the RGB Camera, which is used as navigating camera for PRISMS II,
as the main camera may not be clear when it is running to what it is actually looking at.

PYTHON LIBRARY: thorcam
INSTALL VIA COMMANDLINE: pip install thorcam
DOCUMENTATION: https://pypi.org/project/thorcam/ [Last Accessed 08/12/2022]

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    .i.e. #01/12/2022: updated the message used in the pop up
"""
import logging as log ##troubleshooting
log.info(__file__)  ##troubleshooting
from thorcam.camera import ThorCam
#self defined module

class MyThorCam(ThorCam):
    """Class to run the RGB camera for PRISMS II with output messages"""
    
    def __init__(self):
        super(MyThorCam,self).__init__()
        #initalise class

    def received_camera_response(self, msg, value):
        """Prinst camera's responses with outgoing messages and images"""
        super(MyThorCam, self).received_camera_response(msg, value)
        if msg == 'image':
            return
        print('Received "{}" with value "{}"'.format(msg, value))
    
    def got_image(self, image, count, queued_count, t):
        """find out more information about a given image"""
        print('Received image "{}" with time "{}" and counts "{}", "{}"'
              .format(image, t, count, queued_count))
        
    def playCamera(self,cam):
        """start camera stream"""
        cam.play_camera()

    def stopCamera(self):
        """Stop the camera playing"""
        cam.stop_playing_camera()
    
    def connectRGB(self, cam):
        """creates a server to read thor cam from"""
        # start the server etc.
        cam.start_cam_process()
        #get serial names
        serialnum = cam.refresh_cameras()[0]
        #connect to cam
        cam.open_camera(serialnum )

    def checkExposure(self, cam):
        """Check RGB current exposure"""
        return(cam.exposure_ms)

    def setExposure(self, cam, exptm):
        """set RGB current exposure"""
        #cam.exposure_range # exposure range [0.0, 1000000.0]
        cam.set_setting('exposure_ms', exptm)

# create camera
cam = MyThorCam()

# start the server etc.
cam.start_cam_process()
