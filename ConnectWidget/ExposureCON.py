"""
NAME: ExposureCON.py
AUTHOR: John Archibald Page
DATE CREATED: 21/12/2023 
DATE LAST UPDATED: 21/12/2023

PURPOSE:
    To write functionality to the exposure functions

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import re

class ExposureCON_class():
    """Build the functionality for the Filter controls"""
    def __init__(self,EXGUI,camera_class,connectfunctions,connectequipment, statusUpdater, read):
        super(ExposureCON_class,self).__init__()
        #initalise classes
        self.cf, self.camera, self.su, self.read = connectfunctions, camera_class, statusUpdater, read
        #textedit
        self.expdisplaylineedit = self.cf.Textboxrefences(EXGUI)[0] 
        self.expsteplineedit = self.cf.Textboxrefences(EXGUI)[1] 
        #buttons
        self.returnbutton = self.cf.pushbuttonsrefences(EXGUI)[1]
        self.expdownbutton = self.cf.pushbuttonsrefences(EXGUI)[2]
        self.expupbutton = self.cf.pushbuttonsrefences(EXGUI)[3]
        self.expGUI = EXGUI
        #initalise the lineedit inputs
        self.initaliseValues()
        #check the port is available and ready to be connected to
        self.ce = connectequipment
        if self.ce.available[0] == True:
            try: self.connectbuttons()
            except: self.su.updateStatus("Exposure failed to connect...")
        else:
            self.su.updateStatus("Exposure not connected...")

#connect button inputs-----------------------------------------------------------
    def connectbuttons(self):
        """Connect the functionality to all the exposure buttons"""
        self.cf.widgetconnect(self.expupbutton, lambda: self.exposurerelFUNC("u",self.expsteplineedit.text()))
        self.cf.widgetconnect(self.expdownbutton, lambda: self.exposurerelFUNC("d",self.expsteplineedit.text()))
        self.cf.widgetconnect(self.returnbutton, lambda: self.exposureabsFUNC(self.expdisplaylineedit.text()))
        self.cf.widgetconnect(self.expdisplaylineedit, lambda: self.exposureabsFUNC(self.expdisplaylineedit.text()), clickedF=False, returnF=True)
        
#initalise values----------------------------------------------------------------
    def initaliseValues(self, steps = str(1)):
        """initalises the input to the text edits with values"""
        self.expsteplineedit.setText(steps)
        self.expdisplaylineedit.setText(str(self.read.getConstant(["FocExp"])))

#button functionality------------------------------------------------------------
    def exposurerelFUNC(self,dir,val):
        """Set the relative exposure of the camera"""
        reldict = {"d":-1,"u":1}
        currentexp = float(re.findall(r'\d+\.\d+', self.expGUI.title())[0])
        step = 1 if val =="" else float(val) # input microseconds to GUI
        newexposure = step*reldict[dir] + currentexp
        if newexposure < 1:
            self.su.updateStatus(f"Exposure can't be  <1 ms...", "fail")
        if newexposure > 10000:
            self.su.updateStatus(f"Exposure can't be  >10000 ms...", "fail")
        else:
            self.camera.updateExposure(newexposure)
            self.su.updateStatus(f'Exposure = {round(newexposure,2)} ms')

    def exposureabsFUNC(self,val):
        """Set the relative exposure of the camera"""
        if val =="":
            self.su.updateStatus(f'No Exposure input...')
        else:
            newexposure =  float(val) # input microseconds to GUI
            if newexposure < 10000:
                self.su.updateStatus(f"Exposure can't be  >10000 ms...", "fail")
            if newexposure < 1:
                self.su.updateStatus(f"Exposure can't be  <1 ms...", "fail")
            else:
                self.camera.updateExposure(newexposure)
                self.su.updateStatus(f'Exposure  = {round(newexposure,2)} ms')