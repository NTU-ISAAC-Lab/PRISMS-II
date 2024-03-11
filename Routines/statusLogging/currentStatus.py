"""
NAME: currentStatus.py
AUTHOR: John Archibald Page
DATE CREATED: 28/07/2023
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    To update the most recent status and append to the log.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import logging as log

class currentStatus_class():
    """Read widgets and write .dat file"""
    def __init__(self,statusGUI, connectFunction):
        super(currentStatus_class,self).__init__() 
        #read in the modules
        self.status, self.cf = statusGUI, connectFunction
        #get the status textline
        self.statusBar = self.cf.Textboxrefences(self.status)[0]

    def updateStatus(self,message):
        """Formats the widget vals to be saved to a .csv"""
        #Add to the log
        log.info(message)
        #update the status bad
        self.statusBar.setText(message)
