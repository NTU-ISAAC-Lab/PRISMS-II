"""
NAME: AutoExposureAlgorithum.py
AUTHOR: John Archibald Page
DATE CREATED: 14/05/2023
DATE LAST UPDATED: 31/10/2023

PURPOSE:
    Autoexposure routine of PRISMS II

 VARIABLES:
    Exposure (E) - integration time camera has been set to when taking an iamge
    Starting Exposure (Es) - 30ms, chosen from linear region of white 99% testing
    Counts (C) - The average pixel value in a ROI
    Full Saturation (Sf) - When a pixel has value 2**16 - 1 for a 16 bit image
    Effective Saturation (Se) - When a pixel's value is above the region it can linearly increase, in this case 54312 for a 99% white standard under the large security light lighting.
    Full Saturation Percentage (Sf%) - The percentage of pixels in an image that have the value of Sf
    Effective Saturation Percentage (Se%) - The percentage of pixels with values equal to or above Se

AUTOEXPOSURE ROUTINE:
    1) initalise E using the config file starting exposure:
        a) The starting exposure for the standard filter is read in
        b) This is then scaled using the WhiteStandardFile file, taken from the .csv file of an autoexposure taken of a white cube in the desired lighting
    2) get exposure to a level where the saturation criteria is broken and then drop to half of this:
        a)filter scattering areas from calculation of image
        b) see if the image has saturation values over Sf% and Se% max
        c) if not, double the exposure and run steps for 2) again.           
    3) update the exposure to half the exposure that broke the criteria     
    4) Scale the exposure in the linear region and check not too saturated:
        a) scale the exposure by Ef*scaler / median counts
        b) Filter scattering areas from calculation of image
        c) see if the image has saturation values under Sf% and Se% max
        d) if not, scale the scaler by 1/(how many times it has failed with the scaler) and run steps for 2) again. 
    5) Check if satuaration is above the acceptable level defined in the config.
        
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why.
    08/01/2024:  WORK AROUND FOR ROI NOT UPDATING, remove udpating camera ROI as does not work
    18/01/2024:  -Remove ROI
                 -change scaled to Median and 75% of the effective saturation
                 -add additional check to the exposure once it has been updated
                 -add in the config values instead of the stated values
    09/02/2024: adding in a helper file that scales the starting exposure to make the exposure run faster
"""
import time
import numpy as np
import time
import os
import re
from scipy.ndimage import measurements

class Autoexposure_class():
    """Autoexposure algorithum for andor camera"""
    def __init__(self, cameradriver, FilGUI, read, statusUpdater):
        super(Autoexposure_class,self).__init__()
        self.su, self.camera, self.read,self.FilGUI = statusUpdater, cameradriver,  read, FilGUI

    def autoexposureIteration(self, increasefactor = 2, saturationFlag1 = False, saturationFlag2 = False, scalingcounter = 1):
        """Autoexposure algorithm to find the optimal exposure"""
        self.su.updateStatus(f"*AUTOEXPOSURE INITIATED...*", messagetype ="routine")
        
        #0)call in the start time, constants, and current filter settings
        starttime = time.time()
        StrtexpStandFil, effsatcounts,EffSatScalRat, maxfullsat, maxeffSat, ExpLim = [float(i) for i in self.read.getConstant(["ExpStrt","EffSat", "EffSatScalRat","FullSatPerc","EffSatPerc","ExpLim"])]
        curFil, standFil = int(re.findall(r'\d+', self.FilGUI.widget(0).title())[0]), int(self.read.getConstant(["StandFil"]))
        
        #1)call in the white standard file which will be used as a starting exposure ratio
        WhiteStandardFile = str(self.read.getConstant(["WhiteStandardFile"]))
        try: startingExposureList = self.read.readcol(os.getcwd() + WhiteStandardFile, col="Exposure", header = 0)
        except: startingExposureList = np.array([1]*10) # if this file does not exist, then ratio is just 1
        
        #2) scale the incoming starting exposure for the standard filter to the current filter
        expCur = (StrtexpStandFil/startingExposureList[standFil])*startingExposureList[curFil]
        if expCur < 1:
            self.su.updateStatus(f"*AUTO-EXP FAILED ...* starting exposure too low, increase your starting exposure or update your white standard ratio file! ", messagetype ="fail")
            raise Exception("Raise your starting exposure/ change your white standard ratio!")
        
        #3) initalise E
        self.su.updateStatus(f"1) Starting exposure = {expCur} ms", messagetype ="routine")
        self.camera.updateExposure(expCur) 
        
        #4) Multiply E by increasefactor until the saturation criteria are met
        self.su.updateStatus(f"2) Multiply by x{increasefactor} until Saturation Criteria broken...", messagetype ="routine")
        try:
            while saturationFlag1 == False and expCur < ExpLim:
                self.su.updateStatus(f"2) Trying exposure = {round(expCur,2)} ms", messagetype ="routine")
                #a) call the image and filter out scattering areas caused by surfaces such as gold
                img = self.excludeScatteringClusters(np.array(self.camera.currentimage))
                #b) Check if satuaration is above the acceptable level defined in the config.
                if self.checkSaturation(img) > maxfullsat and self.checkSaturation(img, saturation = effsatcounts) > maxeffSat:
                    self.su.updateStatus(f"2) Criteria met, dropping to {round(expCur/increasefactor,2)} ms", messagetype ="routine")
                    saturationFlag1 = True
                #c)if saturation levels still too low then double the exposure and repeat a-c until good exposure to scale found
                else: 
                    self.su.updateStatus(f"2) Criteria not met... ", messagetype ="routine")
                    expCur = expCur * increasefactor
                    self.camera.updateExposure(expCur)    
        except:
            self.su.updateStatus(f"*AUTO-EXP FAILED (2)...* {round(time.time() - starttime,2)} s", messagetype ="fail")
            raise Exception("AutoExposure failed...")
            
        #5) update the exposure to half the exposure that broke the saturation criteria
        expCur = expCur/increasefactor
        self.camera.updateExposure(expCur)

        #6) scale the exposure in the linear region and check not too saturated
        self.su.updateStatus(f"3) Scaling exposure to optimum...", messagetype ="routine") 
        try:
            while saturationFlag2 == False and expCur < ExpLim:
                #a) get the scaling ratio
                scalrat = self.exposureScaler(effsatcounts, EffSatScalRat, increasefactor, scalingcounter)
                self.su.updateStatus(f"3) Scaling exposure {round(expCur,2)} ms by x{round(scalrat,2)}", messagetype ="routine")
                #b) update the exposure
                self.camera.updateExposure(expCur*scalrat)
                if scalrat == 1: # if the ratio is 1 it means remain the same
                    self.su.updateStatus(f"3) No scaling, Optimum exposure = {round(expCur*scalrat,2)} ms", messagetype ="routine")
                    saturationFlag2 = True
                    break
                #d) grab the updated image
                img = self.excludeScatteringClusters(np.array(self.camera.currentimage))
                #c) Check if satuaration is above the acceptable level defined in the config.
                if self.checkSaturation(img) <= maxfullsat and self.checkSaturation(img, saturation = effsatcounts) <= maxeffSat:
                    self.su.updateStatus(f"3) x{round(scalrat,3)} scaling, Optimum exposure = {round(expCur*scalrat,2)} ms", messagetype ="routine")
                    saturationFlag2 = True
                    break
                #d)if saturation levels still too high then lower the exposure and repeat a-d until good exposure to scale found
                else:
                    scalingcounter = scalingcounter + 1
                    self.su.updateStatus(f"3) x{round(scalrat,3)} failed, attempt counter = {scalingcounter}...", messagetype ="routine")
        except:
            self.su.updateStatus(f"*AUTO-EXP FAILED (3)...* {round(time.time() - starttime,2)} s", messagetype ="fail")
            raise Exception("AutoExposure failed...")
        
        #7) Success!
        self.su.updateStatus(f"*AUTO-EXP SUCCESS!* {round(time.time() - starttime,2)} s", messagetype ="success")
        return(expCur*scalrat)

    def exposureScaler(self, effsatoptim, scaler, increasefactor, scalingcounter):
        """Scales the exposure so median counts is moved up to the effective saturation times by a scaler"""
        #1)find the median value of the image. the median value should increase linearly below the effective saturation
        medpixelval = np.median(np.array(self.camera.currentimage)) #median counts value
        #2)get the scaling ratio from the current median counts to the highest median counts
        scalrat = (effsatoptim*scaler)/ medpixelval
        #3) if this scaler causes the exposure to be too high previously, the modifier reduces the ratio further
        scalrat = scalrat/scalingcounter
        #4)check if the value scales higher than the exposure found to break the criteria, or lower than the current one
        if scalrat < 1: # lower not needed as criteria met for higher value
            self.su.updateStatus(f"3) x{round(scalrat,3)} too low, use current exposure...", messagetype ="routine")
            return(1)
        if scalrat > increasefactor: #too high
            self.su.updateStatus(f"3) x{round(scalrat,3)} too high, use increasefactor*scaler = x{round(increasefactor*scaler,3)}...", messagetype ="routine")
            return(increasefactor*scaler)
        else:
            self.su.updateStatus(f"3) x{round(scalrat,3)} found", messagetype ="routine")
            return(scalrat)
    
    def checkSaturation(self,img, saturation = (2**16)-1):
        """Checks saturation percentage of an image. 16 bit image so (2**16)-1 bit depth when saturated"""
        pixels_sat_arr = (img >= saturation) #img of truth values, pixel saturated =  True
        pixels_sat = pixels_sat_arr.sum() #the sum of truth values in above img
        pixels_tot = img.shape[0] * img.shape[1]  #total number of pixels
        return((pixels_sat/pixels_tot)*100)
    
    def excludeScatteringClusters(self, img, saturation = (2**16)-1): 
        """If there is localised regions of saturation caused by highly scattering surface, these regions will not be counted in the calculation of saturation percentage."""
        #0) call in the parameters set for flagging up the areas of high reflection (such as from gold)
        minclustersize, maxclustersize, featurelimit = [float(i) for i in self.read.getConstant(["minclustersize", "maxsatcluster", "featurelimit"])]
        #1) get a boolean  map of where there are pixels equal to saturation, convert to binary
        satMap = (img == saturation) # boolean
        satMap = satMap.astype(int) #  bianry
        #2) put the img into clusters
        labeled_array, num_features = measurements.label(satMap)
        #3) find the area of each cluster
        area = measurements.sum(satMap, labeled_array, index=np.arange(labeled_array.max() + 1)) 
        #4) filter the clusters by size
        clusterindex = [a for a in range(len(area)) if minclustersize<=area[a] and area[a]<=maxclustersize] 
        #5) if there is no clusters of more clusters than the feature limit, return original image
        if len(clusterindex) > featurelimit or len(clusterindex) == 0:
            return(img)
        #6) else, set the saturated values to 0 so they will not be caught in saturation clause
        for i in clusterindex:
            labeled_array[labeled_array==i] = 0
        #7) filtered map of points to discard when doing the saturation check 
        labeled_array[labeled_array!=0] = 1 # convert the cluster map back to binary
        satMap_filtered = np.logical_not(labeled_array) # invert values
        return(img*satMap_filtered)# return filtered img