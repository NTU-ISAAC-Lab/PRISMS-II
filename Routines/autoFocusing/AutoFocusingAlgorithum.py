"""
NAME: AutoFocusingAlgorithum.py
AUTHOR: John Archibald Page
DATE CREATED: 02/11/2023
DATE LAST UPDATED: 17/11/2023

PURPOSE:
    CONITNUOUS MOVING AUTOFOCUS: This lets the focuser run continually while taking measurments from the camera to find the focus position.
    
INPUT PARAMETERS:
    DEFAULT VAlUE = variable name = Description
    400 steps = maxinfocussteps = should be the maximum number of steps by eye a frame appears in focus + ~30%
    125 steps/s = speed = The speed the focuser moves forward
    250 steps/s = maxspeed = Maximum speed of the focuser 
    0.95 = dropflag = The ratio the current image contrast value is compared to the previous value
    1.01 = noisefil = what is the ratio of the minimum contrast value that would steal count as the flat portion of the contrast
    False = wcs = Worst case scenario, done as a last resort in mosiacking routine and looks a whole range and fits a curve to get the values

METHOD:
    1) Set the focuser back half maxinfocussteps, wait till this finishes
    2) Run the focuser to search through maximum in focus distance
    3) enter a while statement to collect images frequently while the focuser runs continuously:
        i) if the wcs is set then the whole range will be searched. **For Mosaicking
        ii) if wcs is False, the focuser will stop once the contrast has dropped enough indicating the focus peak has been passed
    4) Take the max contrast value as the location of the focus
    5) move to the focus position
    
    *if at any step something fails, then the focuser will move back to the original position*
    
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    #08/12/2023: remove the gaussian fit and data cleaning and instead use the max value as there is frequent enough collections!
"""
#import standard modules
import numpy as np
import time
from PyQt5 import QtCore
import re
import math
#import self-defined modules
from Routines.autoFocusing.contrastAlgorithum import contrastAlgorithums_class as  contrastAlgorithums#contrast algorithums: LAPV, LAPM, TENG, MLOG

class Autofocus_class():
    """Functionality to autofocus the system using cotinuous motion focuser"""
    def __init__(self, cameradriver, focCON, focGUI, statusUpdater, read, connectfunction):
        super(Autofocus_class,self).__init__()
        #drivers, interfacing functions, contrast algorithums
        self.FocGUI, self.focCON, self.camera = focGUI, focCON, cameradriver
        #useful function
        self.cf, self.read, self.su = connectfunction, read, statusUpdater

    def autofocusIteration(self, wcs = False):
        """finds the optimal focus position in steps for PRISMS II."""
        self.su.updateStatus(f"*AUTOFOCUS INITIATED...*", messagetype ="routine")
        #0) initialise parmaters: start time, current position, steps to move
        #self.camera.updateROI(ROI = True)#set the camera to smaller region of interest for faster aquisition
        starttime, originalposition, maxspeed= time.time(), int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0]), int(self.read.getConstant(["FocMaxSpeed"]))
        #worst case scenario or a normal run
        if wcs == False:
            maxinfocussteps,speed,dropflag,noisefil, focCheckSteps = [float(i) for i in self.read.getConstant(["FocRange","FocSpeed","DropRat","noiseFil", "focCheckSteps"])]
        else:
            maxinfocussteps,speed,dropflag,noisefil, focCheckSteps = [float(i) for i in self.read.getConstant(["FocRangeWCS","FocSpeedWCS","DropRatWCS","noiseFilWCS", "focCheckStepsWCS"])]
        #the amount to move forward and backwards
        forwardsteps, backsteps = maxinfocussteps, maxinfocussteps//2 
        #0) original position
        self.su.updateStatus(f"0) Original Position = {originalposition} steps...", messagetype ="routine")
        #1) Move backwards from current position by maxinfocussteps//2 before starting routine. Current position should roughly be in focus
        self.afMove(originalposition - backsteps, maxspeed, movesteps = backsteps, wait = True)
        self.su.updateStatus(f"1) Moving -{backsteps} steps...", messagetype ="routine")
        #2) Set of the focuser moving through maxinfocussteps
        self.afMove(originalposition - backsteps + forwardsteps, speed)
        self.su.updateStatus(f"2) Moving {forwardsteps} steps...", messagetype ="routine")
        starttime1 = time.time()
        try:
            #3) Take focus and contrast measurments as image changes until stop cndition is met
            self.su.updateStatus(f"3) Collecting images...", messagetype ="routine")
            focuslist, contrastlist = self.collectValues(forwardsteps, originalposition, backsteps, starttime1,  speed, dropflag, wcs)
            #4) take the max contrast value as the location of in focus
            focusOptimum, infocusflag= self.findFocus(focuslist, contrastlist, noisefil, int(focCheckSteps))
            #6) move to focus position (or back to original position if failed)
            if infocusflag == True:
                self.afMove(math.ceil(focusOptimum), maxspeed, movesteps = abs(math.ceil(focusOptimum) - focuslist[-1]),  wait = True)
                self.su.updateStatus(f"Focus found! = {math.ceil(focusOptimum)} steps", messagetype ="routine")
                self.su.updateStatus(f"*FOCUSED SUCCESS!* {round(time.time() - starttime,2)}s", messagetype ="success")
            else: 
                self.afMove(originalposition, maxspeed, movesteps = abs(originalposition - focuslist[-1]), wait = True)
                self.su.updateStatus(f"*AUTOFOCUS FAILED, no peak found...* {round(time.time() - starttime,2)}s", messagetype ="fail")
                infocusflag = False
        except: #FAIL CLAUSE 2)  Try again with better exposure or starting position!
            self.afMove(originalposition, maxspeed, movesteps = abs(originalposition - focuslist[-1]), wait = True)
            self.su.updateStatus(f"*AUTOFOCUS FAILED...* {round(time.time() - starttime,2)}s", messagetype ="fail")
            infocusflag = False
        #self.camera.updateROI(ROI = False) # return back to the full image
        return(infocusflag)

#3) collect the focus position and contrast values routines
    def collectValues(self, forwardsteps, originalposition, backsteps, starttime, speed, dropflag, wcs): 
        """Collect the values of focus position and contrast values until condition met."""
        roiw, roih,fullw,fullh =  [int(i) for i in self.read.getConstant(["ROIW", "ROIH", "ImageW","ImageH"])]
        focuslist, contrastlist, timelist  =  [], [], []
        counter, comparisoncounter = 0, 0
        while int((time.time()-starttime)*speed) < forwardsteps:
            counter += 1
            #self.su.updateStatus(f"Looking for Contrast... {counter}\n", messagetype ="routine")
            imgraw = np.array(self.camera.currentimage)
            img = imgraw[(fullw-roiw)//2:(fullw+roiw)//2, (fullh-roih)//2:(fullh+roih)//2] # select the region of interest### WORK AROUND FOR ROI NOT UPDATING
            self.storeValues(img, focuslist, contrastlist, timelist, originalposition, backsteps, starttime, speed)
            #1) first get the list to have at least 2 values so they can be compared
            if len(contrastlist) <= 1 or wcs == True:
                self.storeValues(img, focuslist, contrastlist, timelist, originalposition, backsteps, starttime, speed)
            #2) initalise the comparing the current contrast with previous contrast
            if len(contrastlist) == 2:
                curCon, prevCon = contrastlist[-1], contrastlist[-2] # this is to keep the highest value
            #3)not dropped enough to pass yet
            if prevCon*dropflag <= curCon: 
                self.storeValues(img, focuslist, contrastlist, timelist, originalposition, backsteps, starttime, speed)
                #update the contrasts to compare and the drop counter
                curCon, prevCon = contrastlist[-1], contrastlist[-(2+comparisoncounter)]
                if prevCon >= curCon:
                    comparisoncounter += 1
                else:
                    comparisoncounter = 0
                continue
            #4) dropped to dropflag*previous value
            if prevCon*dropflag > curCon and len(contrastlist) >= 4: #dropped to dropflag*previous value and list is longer than the number of parameters needed to pass the peak
                self.su.updateStatus(f"3) Focus peak passed!", messagetype ="routine")
                self.focCON.stopFocuser()
                break
        return(focuslist, contrastlist)
   
    def storeValues(self, img, focuslist, contrastlist, timelist, originalposition,backsteps, starttime, speed):
            """update lists with current image contrast and focus positions"""
            contrastlist.append(self.findContrast(img)) 
            focuslist.append(((time.time()-starttime)*speed)+(originalposition-backsteps))
            timelist.append(time.time()-starttime)
            
#4) finding the max contrast value, whichwill be taken as the focus location
    def findFocus(self, focuslist, contrastlist, noiseFil,  checksteps, infocusflag = False):
        """Find where the optimum focus from the incoming data as where the contrast is max"""
        #find the difference in magnitude of contrast with an element checksteps to its left
        l_thresh =  []
        for i in range(len(contrastlist)):
            if checksteps < i:
                l_thresh.append(contrastlist[i] - contrastlist[i - checksteps])
        #extract the position of the maximum threshold
        peakidx = l_thresh.index(max(l_thresh))
        focusOptimum = focuslist[peakidx]# optimum focus position, current focus steps position
        ##Flag to see whether the contrast contains pek of ir just flat data##
        if max(contrastlist) > min(contrastlist)*noiseFil:
            infocusflag = True
        return(focusOptimum, infocusflag)  

    def getidx(self, whereidx, subidx = -1):
        "get one value out of a where condition whether it is a list or not"
        return(int(whereidx[subidx]) if len(whereidx) > 1 else int(whereidx[0]))

#basic functions for finding the image contrast and moving the focuser
    def findContrast(self,img):
        """finds contrast metric of an image in region of interest"""
        blurValue = contrastAlgorithums.TENG(np.array(img)) #TENG only metric that picks up the white peak, chek the white works if you are going to change this! 
        return(blurValue)

    def afMove(self, pos, setspeed, movesteps = False, wait = False):
        """move the correct number of steps during autofocusing routine"""
        self.focCON.setFocuserspeed(setspeed) # set the speed
        #move the focuser
        self.focCON.entermoveabs(pos)
        #wait for the move to finish if needed before performing the next step
        if wait == True:
            curthread = QtCore.QThread.currentThread()
            #usleep takes int of microseconds to wait, so 10**6 to convert seconds to microseconds
            curthread.usleep(int(((movesteps/setspeed)*1.5)*10**6)) # 1.5 factor is a safty buffer for processing time
            
