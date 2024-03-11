"""
NAME: SetUpCON.py
AUTHOR: John Archibald Page
DATE CREATED: 13/12/2022 
DATE LAST UPDATED: 20/11/2023

PURPOSE:
    connect the buttons for the advanced options interfacing. apply setup is a routine.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets
from GUI.SelfDefinedWidgets.popupMessage import popupmessage_class
import re
import datetime
import time

class SetUpCON_class():
    """saves a set-up of the euqipment as a file that can be re-launched"""
    def __init__(self, AOGUI, statusupdater, save, read, connectfunction, advancedOptions, savediropen, camCON, FocCON, FilCON, posCON, PositionGUI, FilterGUI, FocuserGUI, ExposureGUI):
        super(SetUpCON_class,self).__init__() 
        #useful functions
        self.su, self.save, self.read, self.cf, self.advancedOptions, self.savediropen = statusupdater, save, read, connectfunction, advancedOptions, savediropen
        #call the widgets
        self.FilGUI, self.FocGUI, self.PosGUI, self.ExpGUI = self.cf.groupboxrefences(FilterGUI)[1], self.cf.groupboxrefences(FocuserGUI)[1], self.cf.groupboxrefences(PositionGUI)[1], self.cf.groupboxrefences(ExposureGUI)[1]
        #call in the equipment intreracting functions
        self.cameraCON, self.focCON, self.filCON, self.standCON = camCON, FocCON, FilCON, posCON
        #connect the button
        self.connectButtons(AOGUI)

#connect the buttons
    def connectButtons(self,AOGUI):
        """Connect the buttons"""
        self.cf.widgetconnect(self.cf.pushbuttonsrefences(AOGUI)[1], self.runwindow)

    def runwindow(self):
        """Create an Set-up advanced options pop-up with options open previous set-up or save current set-up"""
        #1) define advanced option pop-up inputs
        title, msgtitle, msg = "Set-Up","Options","Open previous display or save current display (.i.e. Altitude Position, Azimuth Position, Focus Position, Exposure etc.)."
        obutton, sbutton = QtWidgets.QPushButton("Open"), QtWidgets.QPushButton("Save")
        ofunc, sfunc = self.setupopenFUNC, lambda: self.setupsaveFUNC(dat = False)
        #2) apply to pop-up window
        self.window = self.advancedOptions(title,msgtitle,msg,obutton,ofunc,sbutton,sfunc,col=False)
        self.window.show()

#button functionality
    def setupsaveFUNC(self, start = True, dat = True):
        """Functionality of save current set-up button. If dict = True then being used for image DAT files"""
        #-1) set the start time now, or take in  a start time as stated externally
        start = time.time() if start == True else start
        #0) if the capture is a snapshot then the time taken to run is 0 seconds, else it will be the time to run any autoexposure routine
        snapshot = False if start != round(time.time(),1) else True
        #1) read the values from the widgets
        vals = [list(self.getValues(start, snapshot = snapshot))]
        if dat == False:
            #2) get the file name
            savopendir = self.savediropen(savediropen="save",filepurpose= "Current Set-up", filepath = "/InputFiles/Setup/", filetype="csv")
            #3) save the file
            self.save.datSave(vals,savopendir.filename) 
            self.popup = popupmessage_class("SET-UP SAVED!", f"{savopendir.filename}", "set-up file saved", "info")
        else:
            return(vals)
        
    def setupopenFUNC(self):
        """Functionality of save current set-up button"""
        #1) get the file name
        savopendir = self.savediropen(savediropen="open",filepurpose= "Set-up", filepath = "/InputFiles/Setup/", filetype="csv") # get the file name
        #2) move equipment
        self.setupapply(savopendir.filename)
        self.popup = popupmessage_class("SET-UP APPLIED!", f"{savopendir.filename}", "set-up file applied", "info")
        #3) update the logger
        self.su.updateStatus(f"{savopendir.filename} Set-up applied")
        self.window.hide()

    def setupapply(self,filename):
        """Move the equipment to the correct positions"""
        #1) read in the values from the file
        datetime, timetaken,azipos,altpos,exppos,focpos,filpos = self.read.readrow(filename)
        #2) apply the set up the equipment to move to the set-up position
        self.standCON.entermoveabs(azipos, altpos)
        self.focCON.entermoveabs(focpos)
        self.cameraCON.updateExposure(exppos)
        self.filCON.moveabsolute(filpos)
        self.window.hide()

#get the values from the titles of the groupboxes
    def getValues(self, starttime, snapshot = False):
        """Reads in the titles from the group boxes and gets the current equipment values"""
        #datetime
        datetimenow = datetime.datetime.now()
        timetaken = 0 if snapshot == True else round(time.time() - starttime,3)
        #equipment
        azi, alt = [float(i) for i in re.findall(r'[+-]?\d+(?:\.\d+)?', self.PosGUI.title())]
        fil = int(re.findall(r'\d+', self.FilGUI.title())[0])
        foc = int(re.findall(r'\d+', self.FocGUI.title())[0])
        exp = float(re.findall(r'\d+\.\d+', self.ExpGUI.title())[0])
        return(datetimenow,timetaken,azi,alt,exp,foc,fil) #DATETIME, TIME TAKEN, AZIMUTH,ALTITUDE,EXPOSURE,FOCUS,FILTER