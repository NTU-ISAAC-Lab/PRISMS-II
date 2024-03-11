"""
NAME: AndorCamera.py
AUTHOR: John Archibald Page
DATE CREATED: 07/12/2022 
DATE LAST UPDATED: 08/11/2023

PURPOSE:
To write functionality to the Andor Camera, which is used as the main camera for PRISMS II

PYTHON LIBRARY: andor3
DEPENDANT:Andor Solis (64-bit) library, downloaded frm the Andro website
INSTALL VIA COMMANDLINE: pip install andor3
DOCUMENTATION: https://pypi.org/project/andor3/ [Last Accessed 08/12/2022]

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    #06/11/2023: strip out the plot, move the the GUI
    #15/01/2024: added condition to the new image check to stop freezing if the image is fully saturated
"""
import logging as log
from PyQt5 import QtCore
import numpy as np
import andor3

class AndorCamera_class(QtCore.QObject):
    """a frameserver is started with the andor camera and the incoming images are emited as a qt signal which is picked up by the CameraGUI """
    image_acquired = QtCore.pyqtSignal(np.ndarray)
    def __init__(self, read, parent=None):
        super().__init__(parent)
        self.read = read

    def launchCamera(self):
        """Runs all of the functions to launch the camera if it is connected"""
        self.initialisecamera()     #define camera
        self.initaliseconstants()  #define camera constants
        self.startframeserver()    #start a frameserver

    def initialisecamera(self):
        """initalise camera"""
        try:
            self.cam = andor3.Andor3()
            #log.info(f"Found {self.cam.CameraFamily} {self.cam.CameraModel} {self.cam.CameraName} {self.cam.InterfaceType}")
        except:
            log.exception("Unable to initialise Andor3 camera!")

    def initaliseconstants(self): 
        """Initalise the features of the camera"""
        #call in variables
        fr,ImageW,ImageH = [int(i) for i in self.read.getConstant(["Framerate","ImageW","ImageH"])]
        #variables------------------------------------------
        #print("ingoing exposure to start with", float(self.read.getConstant(["ExpStrt"]))*10**(-3))
        self.cam.ExposureTime = float(self.read.getConstant(["FocExp"]))*10**(-3)
        self.cam.FrameRate = fr #any faster than 30 frames/s then usb 3.0 too fast and image freezes up**
        #constants-------------------------------------------
        #fan
        self.cam.SensorCooling = True
        self.cam.FanSpeed = "On"
        #function of camera and corrections
        self.cam.TriggerMode = "Internal"
        self.cam.SpuriousNoiseFilter = False #replaces with mean values of surrounding pixels
        self.cam.StaticBlemishCorrection = False
        self.cam.MetadataEnable = False
        #pixel settings
        self.cam.AOIHeight = ImageH
        self.cam.AOIWidth = ImageW
        self.cam.VerticallyCentreAOI = True
        self.cam.HorizontallyCentreAOI = True
        self.cam.PixelEncoding = "Mono16"
        self.cam.FastAOIFrameRateEnable = True
        self.cam.SimplePreAmpGainControl = "16-bit (low noise & high well capacity)"

    def startframeserver(self):
        """Create the FrameServer helper and start it serving frames in a background thread"""
        self.fsvr = andor3.FrameServer(self.cam, self.frame_callback)
        self.openEvent()
    
    def frame_callback(self, n, data, timestamp):
        """This just emits the Qt Signal so that the UI can then be updated within the Qt event loop."""
        self.currentimage = data
        self.image_acquired.emit(data)
    
    def closeEvent(self):
        """Handler for window close event."""
        try:
            self.fsvr.stop()
        except:
            log.exception("Error attempting to stop FrameServer.")

    def openEvent(self):
        """Handler for window start event."""
        try:
            self.fsvr.start(frame_rate_max=60)
        except:
            log.exception("Error attempting to start FrameServer.")
            
    def updateROI(self, ROI = True): # this is a function only used in the routines Autoexposure and Autofocus 
        """Tells the camera only to collect smaller ROI. True means only get ROI, False means return to full image"""
        if ROI == True:
            roiw, roih = [int(i) for i in self.read.getConstant(["ROIW", "ROIH"])] # sets to a sub region of interest
        if ROI == False:
            roiw, roih = [int(i) for i in self.read.getConstant(["ImageW","ImageH"])] # returns tot he full image
        self.cam.AOIHeight = roih
        self.cam.AOIWidth = roiw
        print("self.cam.AOIWidth,self.cam.AOIHeight",self.cam.AOIWidth,self.cam.AOIHeight)
        
    def wait_for_new_Image(self, waittype = 0):
        """Work around for the fr being faster than the image updating:
        waittype:
            0: no additional
            1: exposure time plus rolling filter
            2: minimum filter change
            3: maximum filter change  
            4: max of minimum filter change and exposure
            5: max of max filter change and exposure
        numberofupdates:
            number of new images. NOT same as new frame    
        """
        curthread = QtCore.QThread.currentThread() # the current thread this function is being ran on
        scale, numberofupdates = float(self.read.getConstant(["UpdatetimeScaler"])), int(self.read.getConstant(["numberofupdates"]))# 1.5, 3
        #0) initalise time constants
        #rollshut, filmax, filmin = 10, 90, 30 # ms, hard coded as stated in the andor zyla 4.2 manual and FLI filter wheel amnual respectivly
        rollshut, filmax, filmin = [int(i) for i in self.read.getConstant(["RollShutter","minFilt","maxFilt"])]
        #1) set the waittype: 0: no additional, 1: exposure time plus rolling filter, 2: minimum filter change, 3: maximum filter change
        waitdict = {0:0, 1:self.currentExposure() + rollshut, 2:filmin, 3:filmax, 4:max([self.currentExposure() + rollshut, filmin]), 5:self.currentExposure() + rollshut + filmax}

        #2) wait for the time to pass for the initial update  
        curthread.usleep(int((waitdict[waittype]*scale)*10**3))#usleep takes int of microseconds to wait, so convert ms to us

        #3) loop through the images until the image has updated x times
        imagechangedcounter,  imagecheck1 =  0,  self.currentimage
        while imagechangedcounter < numberofupdates:
            #a) new image to compare
            imagecheck2 = self.currentimage
            #b) check if this is the same as the last image
            if np.array_equal(imagecheck1, imagecheck2) == False or np.all(imagecheck1 == 2**16 - 1): ###SECOND CONDITION IS SO DOES NOT GET STUCK IF THE WHOLE IMAGE IS OVER SATURATED###
                imagechangedcounter += 1
            #set the current image ready to compare to the old one
            imagecheck1 = imagecheck2

        #log.info(f"Image updated {numberofupdates} times, {round(time.time() - start, 3)} s")

    def updateFramerate(self, fr):
        """update the framerate"""
        self.cam.FrameRate = fr
        log.info(f"Framerate = {fr} frames/s")
        
    def updateExposure(self, newexposure):
        """updates the exposure and waits for a new image to come through before exiting.Allows the exposure to fully update"""
        if float(newexposure) < 1:
            raise Exception("Exposure can't be <1 ms or >10000 ms...")
        if float(newexposure) > 10000:
            newexposure = 10000
            log.info(f"Exposure  =  {newexposure} ms")
            log.info(f"Exposure can't be >10000 ms...")
        else:
            self.cam.ExposureTime = float(newexposure)*10**(-3)
            self.wait_for_new_Image()
            
    def currentExposure(self):
        """updates the exposure and waites for a new image to come through before exiting.Allows the exposure to fully update"""
        return(self.cam.ExposureTime*10**(3))