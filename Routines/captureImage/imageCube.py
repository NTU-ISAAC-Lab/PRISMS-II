"""
NAME: imageCube.py
AUTHOR: John Archibald Page
DATE CREATED: 11/07/2023
DATE LAST UPDATED: 09/11/2023

PURPOSE:
    To capture an image cube using all the filters.

METHOD:
    1) set exposure
    2) capture image
    3) repeat 1) and 2) until all filter channels have been captured
    4) save as one image tif where each bit has 10 values

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    #30/01/2023: remove the functionality for scalling the exposure
"""
import numpy as np
import tifffile
import time
import re
import os

class captureImageCube_class():
    """Functionality to capture an image with the full range of filters"""
    def __init__(self, camerdriver,  filCON, autoexposure, posGUI, focGUI, filGUI, expGUI, ScanGUI, captureCubeGUI, saveopendir, SetupCON, save, read, statusUpdater, confunctions, popup):
        super(captureImageCube_class,self).__init__()
        self.popup, self.PosGUI, self.FocGUI, self.ScanGUI, self.captureCubeGUI = popup, posGUI, focGUI, ScanGUI, captureCubeGUI
        #displays with informations
        self.filGUI, self.expGUI, self.cameradriver = filGUI, expGUI, camerdriver
        #connect to equipment functions
        self.filCON, self.autoexposureFUNC = filCON, autoexposure
        #useful functions
        self.read, self.saveopendir, self.SetupCON, self.sv, self.su, self.cf =  read,  saveopendir, SetupCON, save, statusUpdater, confunctions
        #the scale by distance option from the scan
        self.scalewithdistancebox = self.cf.checkboxrefences(self.ScanGUI)[0]
        #references to the widgets
        self.expwidgets = self.cf.Textboxrefences(self.expGUI)[:10]
            
    def saveimagecube(self, filename, imagetype = "cube"):
        """
        Functionality of save current set-up button. 
        Possible autoexposureflag, setexposureflag combinations:
            1) autoexposureflag = False, setexposureflag = False x -> Use the current exposure for all filters, used for snapping image cube
            2) autoexposureflag = True, setexposureflag = False x -> Use autoexposure for every filter
            3) autoexposureflag = False, setexposureflag = list of exposure values x -> Use prefound exposure values
        """
        self.su.updateStatus(f"*CAPTURING CUBE...*", messagetype ="routine")
        #0) initalise variables: start time and exposure ratios
        starttime = time.time()
        try:
            autoexposureflag, setexposureflag =  self.exposureInput(imagetype)
        except:
            self.popup.create("ERROR!","EXPOSURE FLAG ERROR :(", "Something wrong with the exposure settings in your inputs!","error")
            raise Exception("Exposure input error...")
        
        #1) set the exposure based on the autoexposureflag and setexposureflag inputs
        if autoexposureflag == False and setexposureflag == False: #1) Use current exposure: for taking cube image
            exposurelist = False

        if autoexposureflag == True: #2) Use autofocus for every filter
            exposurelist = []
        
        if type(setexposureflag) == list: #3) use a set list
            exposurelist = setexposureflag 

        #2) move back to the first filter as this will take the longest time, and set the exposure to give time to update
        starttime_filter = time.time() # the start time for this filter to auto expose to gauge how long each filter takes
        self.filCON.moveabsolute(0) # move the spin filter
        self.cameradriver.wait_for_new_Image(waittype = 3)
        if autoexposureflag == True:
                newexp = self.autoexposureFUNC()
                exposurelist.append(newexp)
        if type(exposurelist) != bool:
            self.cameradriver.updateExposure(exposurelist[0]) #change camera exposure
        
        #3)take the images at the found exposures for different filters
        imagelist, imagedatlist = [], []
        for i in range(10):
            #a)output last image and save to list. save image data to list
            imgtosv = np.array(self.cameradriver.currentimage)
            imgtosv = np.rot90(imgtosv,3)
            imagedat = self.SetupCON.setupsaveFUNC(start = starttime_filter)
            #b)add to the list
            imagelist.append(imgtosv)
            imagedatlist.append(list(imagedat[0]))
            if i < 9:
                starttime_filter = time.time() # the start time for this filter to auto expose to gauge how long each filter takes
                #set the exposure to 1 ms to stop the bug where pixels stay saturated if it goes from a high saturation to low
                self.cameradriver.updateExposure(1)
                #c) make filter and exposure correct
                self.filCON.moveabsolute(i+1) # move the spin filter
                self.cameradriver.wait_for_new_Image(waittype = 2)
                #d)set the exposure depending on exposure setting
                if autoexposureflag == True:
                    newexp = self.autoexposureFUNC()
                    exposurelist.append(newexp)
                if type(exposurelist) != bool:
                    self.cameradriver.updateExposure(exposurelist[i+1]) #change camera exposure

        #4)combine the images into one
        cubefinishtime = round(time.time() - starttime,2)
        finalarray = np.dstack(imagelist).astype(np.uint16)
        self.su.updateStatus(f"*CUBE CAPTURED!* {cubefinishtime} s", messagetype ="routine")
        
        #5)save the files
        try:
            filenamedat = filename[:-5]+".csv"
            filename1 = filename[:-5].split('/')[-1]
            filenamepath = filename
            #make sure the filter names and exposure are correct as they do not update fast enough when being read in from equipment
            for i in range(len(imagedatlist)):
                imagedatlist[i][6] = i # the filter names
                if type(exposurelist) != bool: # only if the exposure is being updated as this routine runs
                    imagedatlist[i][4] = round(exposurelist[i],2) # the exposure value
            # update the datefilename
            self.sv.datSave(imagedatlist,filenamedat)
            #4b)save image file
            tifffile.imwrite(filenamepath, finalarray, planarconfig='contig')
            self.su.updateStatus(f"*{filename1}.tiff SAVED!* {cubefinishtime} s", messagetype ="success")
        except:
            self.su.updateStatus(f"*SAVE CANCELLED...*", messagetype ="fail")

    def exposureInput(self, imagetype):
            """
            From the widget input the exposure routine is determined for saving the image. 
            Possible routines:
            1) set exposure value: int, list, False
                a) FALSE: Set exposure is not selected, an autofocus regime will run instead
                c)FAIL: if the exposure input is all empty, then there will be an error as this will not work with the set exposure
                d)LIST len 10: if none of the inputs are empty then take these as the set exposures
            2) autoexposure value: int, True, False
                a)FALSE: a set exposure routine will run instead
                b)TRUE: all of the filters will be auto-exposed seprately
            """
            #-1) grab the exposure widget values depending on whether one cube is being taken or a scan
            gui = self.captureCubeGUI if imagetype == "cube" else self.ScanGUI # which GUI to read from
            aEbutton = self.cf.pushbuttonsrefences(gui)[0] #autoexposure button
            setEbutton = self.cf.pushbuttonsrefences(gui)[1] #set exposure button
            widgetlist = self.cf.Textboxrefences(gui)
            self.scalewithdistancebox = self.cf.checkboxrefences(gui)[0]    
            self.focustoscalefrom = widgetlist[0]    
            exposurelist = [i.text() for i in widgetlist[1:11]]   
            
            #1) set exposure value: int, list, False
            if setEbutton.isChecked() == False: #a)
                setexposureflag = False 
            if setEbutton.isChecked() == True:
                if len([i for i in exposurelist if i in ["","0"]]) == len(exposurelist): #c)
                    self.popup.create("ERROR!","SET EXPOSURE FLAG ERROR :(", "The set Exposure flag button is pressed but no exposures have been input...","error")
                    raise Exception("Exposure input error...")
                if len([i for i in exposurelist if i not in ["","0"]]) == len(exposurelist): #d)
                    setexposureflag = [float(i) for i in exposurelist]
                    #if this is a scanning routine that has the distance scalling option checked, scale the option by the focus value based on the input focsvsdistance
                    if self.scalewithdistancebox.isChecked() == True:
                        setexposureflag = self.scaleexposurebydistance(setexposureflag)
            #2) autoexposure value: int, True, False
            if aEbutton.isChecked() == False: #a)
                autoexposureflag = False
            if aEbutton.isChecked() == True:
                autoexposureflag = True  #b)
            return(autoexposureflag, setexposureflag)
        
    def scaleexposurebydistance(self, exposurelist):
        """"Depending on the original distance, scale the exposure ratios"""
        print("Function entered!")
        #1) read in the focus vs distance curve
        focdistfilelocation = str(self.read.getConstant(["FocvsDistFile"]))
        focuses_raw = self.read.readcol(os.getcwd() + focdistfilelocation, col="Focus", header = 0)
        distance_raw = self.read.readcol(os.getcwd() +  focdistfilelocation, col="Distance", header = 0)

        #2)get the lists in order of focus and distance, and apply offset
        # offset
        FocDistoffset = int(self.read.getConstant(["FocDistoffset"])) 
        #order the list
        focuses = np.array(sorted(focuses_raw))+FocDistoffset
        distance = [distance_raw[i] for i in sorted(range(len(focuses_raw)), key=lambda k: focuses_raw[k])]

        #3)interpolate to second degree polynomial to fin the distance at this focus
        #polynomial fit 2nd degree
        FocDistpolyfit = np.polyfit(focuses, distance, 2)
        #start focus to distance
        startFoc = int(self.focustoscalefrom.text())
        startDist = np.polyval(FocDistpolyfit, startFoc) # second degree polynomial
        #current focus to distance
        curFoc = int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0])
        curDist = np.polyval(FocDistpolyfit, curFoc) # second degree polynomial

        #4) return the scalled exposure list
        #offset_azi, offset_alt = [float(i) for i in self.read.getConstant(["LAzioffset", "LAltoffset"])]
        #angle_at_target = np.sqrt(offset_azi**2 + offset_alt**2) # angle taking to account the azimuth and altitdue difference
        #startLDist = self.dist_light_to_target(startDist, angle_at_target) # distance to the light
        #curLDist = self.dist_light_to_target(curDist, angle_at_target) # distance to the light

        #5) return the scalled exposure
        return(list(np.array(exposurelist)*(curDist/startDist)**2))
    
#####THIS IS STILL BEING INVESTIGATED!####################
    def dist_light_to_target(self, dist_camera_to_target, azi):
        """From the distance between the camera and the target, calculate the distance from the light to the target.
        This is derived from the cosine and law of sines rule."""
        dist_camera_to_light = float(self.read.getConstant(["CameratoLight"]))
        d0,d1 = dist_camera_to_light, dist_camera_to_target
        d3 = d1*np.cos(azi*np.pi/180) + np.sqrt( (d0**2) - (d1**2)*((np.sin((azi)*np.pi/180))**2))
        return(d3)