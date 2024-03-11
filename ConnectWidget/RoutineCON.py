"""
NAME: RoutineCON.py
AUTHOR: John Archibald Page
DATE CREATED: 11/07/2023
DATE LAST UPDATED: 19/07/2023

PURPOSE:
    To connect the routine buttons and functions of PRISMS II

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
#self defined modules
from Routines.autoExposure.AutoExposureAlgorithum import Autoexposure_class
from Routines.autoFocusing.AutoFocusingAlgorithum import Autofocus_class
from Routines.Scanning.ScanAlgorithum import Scan_class
from Routines.captureImage.imageCube import captureImageCube_class
from Routines.captureImage.imageSnapshot import captureImageSnapshot_class

class RoutineCON_class():
    """connect the routines used by PRISMS II to their respective buttons"""
    def __init__(self, FILGUI, CGUI, CCGUI, POSGUI, FOCGUI, EXGUI, ScanGUI, cameradriver, focdriver, FocCON, FilCON, ScanCON, posCON, read, save, connectfunctions, saveopendir, SetupCON, statusUpdater, popup):
        super(RoutineCON_class,self).__init__()
        #GUi
        self.FILGUI, self.CGUI, self.FOCGUI, self.EXGUI, self.ScanGUI = FILGUI, CGUI, FOCGUI, EXGUI, ScanGUI
        #drivers
        self.cameradriver, self.focdriver = cameradriver, focdriver
        #connection functions
        self.focuserCON, self.filterCON, self.positionCON, self.ScanCON = FocCON, FilCON, posCON, ScanCON
        #functions
        self.cf, self.saveopendir, self.SetupCON, self.su, self.read, self.save, self.popup  = connectfunctions,  saveopendir, SetupCON, statusUpdater, read, save, popup
        #capture cube location and filename
        self.widgetlist = self.cf.Textboxrefences(CCGUI)
        self.Namecc,self.Locationcc= self.widgetlist[11:]
        #image item used to get the camera data from
        self.imageitem = self.cf.glwrefences(CGUI)[0].getItem(0, 0).allChildItems()[3]
        #routines
        self.ae = Autoexposure_class(self.cameradriver, self.FILGUI, self.read, self.su) 
        self.af = Autofocus_class(self.cameradriver, self.focuserCON, self.FOCGUI, self.su, self.read, self.cf)
        self.cic = captureImageCube_class(self.cameradriver, self.filterCON, self.ae.autoexposureIteration, POSGUI, FOCGUI, FILGUI, EXGUI, ScanGUI, CCGUI, self.saveopendir, self.SetupCON, self.save, self.read, self.su, self.cf, self.popup)
        self.cis = captureImageSnapshot_class(self.cameradriver, self.saveopendir, self.SetupCON, self.save, self.su)
        self.mf = Scan_class(self.cic, self.af, self.ae, self.positionCON, self.filterCON, self.ScanCON, self.cameradriver.updateExposure, ScanGUI, self.read, self.save, self.su, self.cf, self.popup) 
        #call the references for each button
        self.autoexpbutton,self.autofocusbutton,self.runScanbutton, self.savesnapshotbutton,self.savecubebutton = self.buttonreferences(CGUI, CCGUI, FOCGUI, EXGUI, ScanGUI)
        #assign the valeus to the buttons
        self.connectbuttons()

    def buttonreferences(self, CGUI, CCGUI, FOCGUI, EXGUI, ScanGUI):
        """Get the references t the routine buttons"""
        aebutton = self.cf.pushbuttonsrefences(EXGUI)[0] 
        afbutton = self.cf.pushbuttonsrefences(FOCGUI)[0]
        savesnapshotbutton = self.cf.pushbuttonsrefences(CGUI)[2] # call in the save button
        savecubebutton = self.cf.pushbuttonsrefences(CCGUI)[5] # call in the save button
        rmobutton = self.cf.pushbuttonsrefences(ScanGUI)[8]
        return(aebutton,afbutton,rmobutton, savesnapshotbutton, savecubebutton)
    
    def connectbuttons(self):
        """Connect the routine buttons"""
        #AUTOEXPOSURE
        try:self.cf.widgetconnect(self.autoexpbutton, self.ae.autoexposureIteration, thread = True, freeze = True)
        except:self.su.updateStatus("Autoexposure failed to connect...")
        #AUTOFOCUSING
        try:self.cf.widgetconnect(self.autofocusbutton, self.af.autofocusIteration, thread = True, freeze = True)
        except:self.su.updateStatus("autofocus failed to connect...")
        #SCANNING ROUTINE
        try:self.cf.widgetconnect(self.runScanbutton, self.mf.scanningRoutine, thread = True, freeze = True) 
        except:self.su.updateStatus("Scanning failed to connect...")
        #SAVE IMAGE SNAPSHOT
        try:self.cf.widgetconnect(self.savesnapshotbutton, self.cis.savesnapshot)
        except:self.su.updateStatus("Snapshot failed to connect...")   
        #SAVE IMAGE CUBE
        try:self.cf.widgetconnect(self.savecubebutton, lambda: self.cic.saveimagecube(self.Locationcc.text() +"\\" + self.Namecc.text() + ".TIFF"), thread = True, freeze = True)
        except:self.su.updateStatus("Capture Cube failed to connect...")              