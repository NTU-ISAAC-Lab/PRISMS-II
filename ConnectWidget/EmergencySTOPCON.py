"""
NAME: FilterCON.py
AUTHOR: John Archibald Page
DATE CREATED: 29/11/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    Emergency stop button used primarily for when equipment is moving in a way it should not be doing

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
class EmergencySTOPWorker():
    """This will produce the signals for all of the displays that will be updated continuously (.i.e. position, focus, filter)"""
    def __init__(self, focint, posint, posdriver, Focdriver,  emergencySTOPbutton, connectfunction, statusUpdater, GUI):
        super(EmergencySTOPWorker, self).__init__()
        #interfacing
        self.focint, self.posint = focint, posint
        #drivers
        self.focdriver, self.posdriver =  Focdriver, posdriver
        #useful functions
        self.cf, self.su = connectfunction, statusUpdater
        #the stop button and GUI
        self.emergencySTOPbutton, self.GUI = emergencySTOPbutton, GUI
        #connect the emergency stop button to release the signal
        self.cf.widgetconnect(emergencySTOPbutton.widget(0), self.EMERGENCYSTOP)
        self.cf.widgetconnect(emergencySTOPbutton.widget(1), self.EMERGENCYSTOP)

    def EMERGENCYSTOP(self):
        """stops moving equipment, stops a routine running"""
        if self.emergencySTOPbutton.currentIndex() == 1:
            self.su.updateStatus("EMERGENCY STOP!!!", messagetype = "fail")
            #disablenable the gui
            for i in self.GUI:
                i.setEnabled(False)
            #1) moving equipment that if the set-up is incorrectly could be damaged.
            self.focint.emergencySTOP(self.focdriver)#focuser
            self.posint.emergencySTOP(self.posdriver)#positional stand
            #switch to the go button
            self.emergencySTOPbutton.setCurrentIndex(0)
        if self.emergencySTOPbutton.currentIndex() == 0:
            self.su.updateStatus("STOP RELEASED...", messagetype = "success")
            #enable the gui
            for i in self.GUI:
                i.setEnabled(True)
            #switch to the stop button
            self.emergencySTOPbutton.setCurrentIndex(1) #switch symbol to stop as equipment is enabled