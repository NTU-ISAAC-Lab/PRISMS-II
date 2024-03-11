"""
NAME: captureCubeCON.py
AUTHOR: John Archibald Page
DATE CREATED: 22/01/2024 
DATE LAST UPDATED: 22/01/2024

PURPOSE:
    Set the options for setting the exposure when capturing an image cube.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import os
import datetime
from GUI.SelfDefinedWidgets.popupMessage import popupmessage_class

class captureCubeCON_class():
    """To connect functionality for GUI to capture one cube using different exposure settings"""
    def __init__(self, CGUI, captureCubewindow, connectfunctions, save, read, saveopendir):
        super(captureCubeCON_class,self).__init__() 
        #initalise classes
        self.cf, self.sc, self.read, self.saveopendir,  self.captureCubewindow = connectfunctions, save, read, saveopendir, captureCubewindow
        #define the buttons
        self.capturecubebutton = self.cf.pushbuttonsrefences(CGUI)[3] # call in the set up button
        self.aebutton = self.cf.pushbuttonsrefences(self.captureCubewindow)[0] 
        self.indbutton = self.cf.pushbuttonsrefences(self.captureCubewindow)[1]
        self.whiteexpbutton = self.cf.pushbuttonsrefences(self.captureCubewindow)[2]
        self.grabfolderbutton = self.cf.pushbuttonsrefences(self.captureCubewindow)[3] 
        #self.backbutton = self.cf.pushbuttonsrefences(self.captureCubewindow)[4] #back button
        self.widgetlist = self.cf.Textboxrefences(self.captureCubewindow)
        self.scalewithdistancebox = self.cf.checkboxrefences(self.captureCubewindow)[0]
        #list the widgets individually
        self.Name,self.Location= self.widgetlist[11:]
        #connect functionality
        self.connectButtons()
        self.initalisewidgetValues()
        
#initalising pop-up-----------------------------------------------------------------------------------------------
    def selectcubeOptions(self):
        """Opens up a new file and closes the options menu"""
        self.captureCubewindow.show()
        
#GUI creation and connecting widgets--------------------------------------------------------------------------------
    def initalisewidgetValues(self):
        """set the widgets to have inital values"""
        self.widgetlist[0].setEnabled(False) # the focus distance scaler
        self.exposureoptionFUNC(self.widgetlist[1:11], self.aebutton, self.indbutton, ae = False)
        self.Name.setText("Cube-{}".format(datetime.datetime.now().date()))
        self.Location.setText(os.getcwd()+"\\OutputFiles\\Images\\")
        
    def connectButtons(self):
        """Connect the buttons used in the Scan window"""
        self.cf.widgetconnect(self.capturecubebutton, self.selectcubeOptions)
        self.cf.widgetconnect(self.aebutton, lambda: self.exposureoptionFUNC(self.widgetlist[1:11], self.aebutton, self.indbutton, ae = True))
        self.cf.widgetconnect(self.indbutton, lambda: self.exposureoptionFUNC(self.widgetlist[1:11], self.aebutton, self.indbutton, ae = False))
        self.cf.widgetconnect(self.whiteexpbutton, lambda: self.grabWhite(self.widgetlist, self.aebutton, self.indbutton))
        self.cf.widgetconnect(self.grabfolderbutton, lambda: self.FolderopenFUNC(self.Location))
        self.cf.widgetconnect(self.scalewithdistancebox, lambda: self.FocusScalerFUNC(self.scalewithdistancebox, self.widgetlist[0], self.aebutton), clickedF=False, statechangedF = True)
        
#Button functionality---------------------------------------------------------------------------------
    def FolderopenFUNC(self, location):
        """Functionality of save current current Scan inputs"""
        savopendir = self.saveopendir(savediropen="dir", filepurpose= "image", filepath = "\\OutputFiles\\Images\\", filetype=False) # get folder name
        location.setText(savopendir.filename)
        
#Input functionality. These are interdependant and will be listed in order of appearance---------------------------------------------------------------------------------------------------------------------------------------   
    def exposureoptionFUNC(self, widgetlist, aebutton, indbutton,  ae = True):
        """makes sure when autoexposure button is pressed then the set exposre is not pressed and vis versa"""
        #get the widgets
        expo0,expo1,expo2,expo3,expo4,expo5,expo6,expo7,expo8,expo9 = widgetlist
        #set the buttons
        if (aebutton.isChecked() == True and ae == True) or (indbutton.isChecked() == False and ae == False):
            indbutton.setChecked(False); aebutton.setChecked(True)
            expo0.setEnabled(False);expo1.setEnabled(False);expo2.setEnabled(False);expo3.setEnabled(False);expo4.setEnabled(False);expo5.setEnabled(False);expo6.setEnabled(False);expo7.setEnabled(False);expo8.setEnabled(False);expo9.setEnabled(False)
        if (aebutton.isChecked() == False and ae == True) or (indbutton.isChecked() == True  and ae == False):
            indbutton.setChecked(True); aebutton.setChecked(False)
            expo0.setEnabled(True);expo1.setEnabled(True);expo2.setEnabled(True);expo3.setEnabled(True);expo4.setEnabled(True);expo5.setEnabled(True);expo6.setEnabled(True);expo7.setEnabled(True);expo8.setEnabled(True);expo9.setEnabled(True)

    def FocusScalerFUNC(self, checkbox, lineedit, aebutton):
        """makes sure when autoexposure button is pressed then the set exposre is not pressed and vis versa"""
        if (aebutton.isChecked() == True) or (checkbox.isChecked() == False):
            lineedit.setEnabled(False)
        if (checkbox.isChecked() == True) and (aebutton.isChecked() == False):
            lineedit.setEnabled(True)

#grab information functions    
    def grabWhite(self, widgetlist, aebutton, indbutton):
        """grab the exposure and current focus position from a white file that has been autoexposed"""
        #0)select the relevent file
        savopendir = self.saveopendir(savediropen="open",filepurpose= "white image cube .csv for exposure", filepath = "\\OutputFiles\\Images\\", filetype="csv") # get the file name
        #1)grab the exposure value
        self.grabExposure(widgetlist[1:11], aebutton, indbutton, savopendir)
        #2)grab the focus value
        self.grabFocus(widgetlist[0], savopendir)
    
    def grabExposure(self, widgetlist, aebutton, indbutton, savopendir):
        """get the exposure from a csv file produced from capturing an image cube"""
        #1)call in the exposure from the file
        exposures = self.read.readcol(savopendir.filename, col="Exposure", header = 0)
        #2)check the correct file is chosen/ has the right number of exposures
        try: 
            for i in range(len(exposures)):
                widgetlist[i].setText(str(exposures[i]))
        except: 
            self.popup = popupmessage_class("WHITE .csv FILE IS INCORRECT", f"{savopendir.filename}", "CHECK THIS IS A CUBE AND NOT A SNAPSHOT!", "error")
        #3)set the set exposure button to true
        self.indbutton.setChecked(True); self.aebutton.setChecked(False)
        self.exposureoptionFUNC(widgetlist, aebutton, indbutton, ae = False)
        
    def grabFocus(self, widgetlist, savopendir):
        """get the Focus from a csv file produced from capturing an image cube"""
        #1) call in the Focus
        focuses = self.read.readcol(savopendir.filename, col="Focus", header = 0)
        #2)check the correct file is chosen/ has the right number of exposures
        try: 
            widgetlist.setText(str(focuses[1])) # choose the second index to make sure the chosen focus is correct
        except: 
            self.popup = popupmessage_class("WHITE .csv FILE IS INCORRECT", f"{savopendir.filename}", "CHECK THIS IS A CUBE AND NOT A SNAPSHOT!", "error")