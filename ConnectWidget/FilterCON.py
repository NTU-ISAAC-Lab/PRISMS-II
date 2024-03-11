"""
NAME: FilterCON.py
AUTHOR: John Archibald Page
DATE CREATED: 29/11/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    To write functionality to filter.
    <>:move the filter to the printed number, update the camera label
    u: enter moves the filter to this one, update the label for the camera

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
class FilterCON_class():
    """Build the functionality for the Filter controls"""
    def __init__(self,FGUI, connectfunctions,connectequipment,filterwheel_class, filterdriver, statusUpdater):
        super(FilterCON_class,self).__init__()
        #initalise class, this also connects the device
        self.cf, self.ce, self.func, self.driver, self.su =  connectfunctions,connectequipment,filterwheel_class, filterdriver,statusUpdater
        #call references to the widgets
        self.dial = self.cf.Dialrefences(FGUI)[0]
        #initalise connection
        if self.ce.available[2] == True:
            try:
                self.dialconnect()
                self.func.setFilterWheel(4,self.driver) #initalise filter to 5th filter
            except:
                self.su.updateStatus("Filter not connected...")
        else:
            self.su.updateStatus("Filter not connected...")
    
    #connect buttons functionality   
    def dialconnect(self):
        """Connect spinwheel functionality"""
        self.cf.widgetconnect(self.dial, self.updatelabelandmovespinwheel, clickedF = False, valuechangedF = True, thread = True)

    def updatelabelandmovespinwheel(self):
        """Combine the update label and move the spin wheel by combining the funcitons"""
        self.func.setFilterWheel(self.dial.value(),self.driver) # move the spin filter
        self.su.updateStatus(f"Filter = {self.dial.value()}")

    def moveabsolute(self, abspos):
        """Move to absolute filter position, used in the set-up"""
        self.func.setFilterWheel(int(abspos),self.driver) # move the spin filter
        self.su.updateStatus(f"Filter = {abspos}")