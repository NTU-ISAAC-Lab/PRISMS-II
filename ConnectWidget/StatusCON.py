"""
NAME: StatusCON.py
AUTHOR: John Archibald Page
DATE CREATED: 23/11/2023
DATE LAST UPDATED: 23/11/2023

PURPOSE:
To update the status log of the current session

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import datetime

class StatusCON_class():
    """Build the functionality for the Filter controls"""
    def __init__(self,StatusGUI, scrollpopup, connectfunctions):
        super(StatusCON_class,self).__init__()
        #initalise class, this also connects the device
        self.status, self.cf, self.scrollwindow =  StatusGUI, connectfunctions, scrollpopup
        #call references to the widgets
        self.logbutton = self.cf.pushbuttonsrefences(self.status)[0]
        #connect the one button to functionality
        self.cf.widgetconnect(self.logbutton, self.runwindow)

    def runwindow(self):
        """Rune the status pop-up to show the log so far for the current session"""
        message = self.readlogFile()
        self.popup = self.scrollwindow("Session Log", "", message)
        self.popup.show()

    def readlogFile(self):
        """read the most recent outcoming log and print to the textbox"""
        #current log path
        logpath = "OutputFiles/Logs/"
        logFile = "PRISMSII{}.log".format(datetime.datetime.now().date())
        #read in log
        with open(logpath + logFile) as f:
            f = f.readlines()
        #the locator line
        topmessage = "Initiating program..." #all messages below this instance and the pre-amble of the log will be included
        includeabove = 7 # number of lines above this message to start from
        #find last instance in the file of the topmessage line
        f.reverse() #the original list is then reversed
        locationlist = [f.index(i) for i in f if topmessage in i]
        startrevindex = min(locationlist) # last one to appear
        #startrevindex = frev.index(topmessage in raw_file_content)
        startindex = len(f)-(startrevindex+1)-includeabove
        #text to include in the message:
        f.reverse() # the list is then reversed again
        message=f[startindex:]
        message = ''.join(message)
        return(message)