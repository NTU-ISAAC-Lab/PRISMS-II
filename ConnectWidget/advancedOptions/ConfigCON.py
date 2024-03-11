"""
NAME: ConfigCON.py
AUTHOR: John Archibald Page
DATE CREATED: 13/12/2022 
DATE LAST UPDATED: 18/10/2023

PURPOSE:
    Attach functionality to the advanced options interface config button.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    #18/10/2023:> implement the functions from the csv for reading and writting csv files
                > get rid of apply button re-launch method, instead the constant file will be read in when a constant is needed
"""
from PyQt5 import QtWidgets
import os
from GUI.SelfDefinedWidgets.popupMessage import popupmessage_class

class ConfigCON_class():
    """read and update the config values for the functions"""
    def __init__(self, cameradriver, AOGUI, configGUI, connectfunction, save, read, savediropen, AOwindow):
        super(ConfigCON_class,self).__init__() 
        #initalise classes
        self.camera, self.configwindow, self.save, self.read, self.cf, self.savediropen, self.windowcreate = cameradriver, configGUI, save, read, connectfunction, savediropen, AOwindow
        #widget references
        self.widgetlist = self.cf.Textboxrefences(self.configwindow)
        #call buttons
        self.configbutton = self.cf.pushbuttonsrefences(AOGUI)[2] # call in the config button, as seen on the main window GUI
        self.save_and_applybutton = self.cf.pushbuttonsrefences(self.configwindow)[-1] #Apply config.
        #connect buttons
        self.connectButtons()

    def runwindow(self):
        """Create a config advanced options pop-up with options open previous config or save current config"""
        #pop-up message
        title, msgtitle, msg = "Config", "Options", "Open existing Config file or create new file."
        #button definitions and functions
        obutton, cbutton = QtWidgets.QPushButton("Open"), QtWidgets.QPushButton("Create")
        ofunc, cfunc = lambda: self.configopenFUNC(), lambda: self.configwindow.show()
        #apply to pop-up window
        self.window = self.windowcreate(title,msgtitle,msg,obutton,ofunc,cbutton,cfunc,col=False)
        self.window.show()

    def connectButtons(self):
        """Connect the button funcitonality"""
        self.cf.widgetconnect(self.configbutton, self.runwindow)
        self.cf.widgetconnect(self.save_and_applybutton, self.configsaveFUNC)

    def configsaveFUNC(self):
        """Functionality of save current config through "save" button"""
        vals = self.cf.readvaluesofwidget(self.widgetlist)
        savopendir = self.savediropen(savediropen="save",filepurpose= "Config file", filepath = "\\InputFiles\\Config\\", filetype="csv") # get the file name
        self.save.filesave("config",vals,savopendir.filename)
        #apply as the new config
        os.environ["CONFIGFILEPATH"] = savopendir.filename
        #update the camera settings
        self.camera.updateFramerate(float(self.read.getConstant(["Framerate"])))
        #show a pop up to confirm this has been saved
        self.popup = popupmessage_class("CONFIG FILE SAVED AND APPLIED!", f"{savopendir.filename}", "Config file saved and set as the current config file", "info")

    def configopenFUNC(self):
        """Functionality of save current config button"""
        savopendir = self.savediropen(savediropen="open",filepurpose= "Config file", filepath = "\\InputFiles\\Config\\", filetype="csv") # get the file name
        newvals = self.read.readcol(savopendir.filename) # call in new values from the folder
        self.cf.setvaluesofwidget(self.widgetlist ,newvals)#update values
        self.window.hide()
        self.configwindow.show()