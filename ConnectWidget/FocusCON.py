"""
NAME: FocusCON.py
AUTHOR: John Archibald Page
DATE CREATED: 09/12/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    To write functionality to the focuser, connecting the buttons and text inputs.
    >: enter moves the filter to this one, update the label for the camera
    autofocus: runs the auto focus routine.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import re

class FocusCON_class():
    """Build the functionality for the Filter controls"""
    def __init__(self,GUI,connectfunctions,focuser_class,connectequipment,focuserdriver, statusUpdater, read, stopbutton):
        super(FocusCON_class,self).__init__()
        #initalise classes
        self.cf, self.func, self.ce, self.driver, self.su, self.read = connectfunctions,focuser_class,connectequipment,focuserdriver, statusUpdater, read
        #call the emrgency stop signal
        self.STOPbutton = stopbutton
        #call the references to the buttons and textbox entries
        self.textboxlist,self.buttonlist= self.cf.Textboxrefences(GUI), self.cf.pushbuttonsrefences(GUI) #movement buttons
        #define the widgets
        self.inputbox, self.stepsbox, self.absposButton, self.Nrbutton, self.Frbutton, self.FocGUI = self.textboxlist[0], self.textboxlist[1], self.buttonlist[1], self.buttonlist[2], self.buttonlist[3], GUI
        #initalise lineedit boxes
        self.initaliseValues()
        #initalise connection
        if self.ce.available[3] == True:
            try:
                self.connectbuttons()
                maxspeedfocuser = int(self.read.getConstant(["FocMaxSpeed"]))
                self.setFocuserspeed(maxspeedfocuser)
            except:
                self.su.updateStatus("Focuser not connected...")
        else:
            self.su.updateStatus("Focuser not connected...")

#initalise values----------------------------------------------------------------
    def initaliseValues(self, steps = str(1), display = str(0)):
        """initalises the input to the text edits with values for focuser"""
        self.stepsbox.setText(steps) #initalise the default steps
        self.inputbox.setText(display) #initalise the display with checking while it is first updating

#connect functions-------------------------------------------------------------------
    def connectbuttons(self):
        """Connect movement buttons for focuser"""
        self.cf.widgetconnect(self.Nrbutton, lambda: self.entermoverel("Nr"), thread = True)
        self.cf.widgetconnect(self.Frbutton, lambda:  self.entermoverel("Fr"), thread = True)
        self.cf.widgetconnect(self.absposButton, lambda: self.entermoveabs(int(self.inputbox.text())), thread = True)
        self.cf.widgetconnect(self.inputbox, lambda: self.entermoveabs(int(self.inputbox.text())), clickedF=False, returnF=True, thread = True)
        
#functions to connect to-------------------------------------------------------------        
    def entermoverel(self, dir):
        """moves to relative poisition, making sure the move is in the focuser stepper motor range"""
        dirtextdict = {"Nr":"-", "Fr":""} # [int(i) for i in re.findall(r'\d+', self.FilGUI.title())][0]
        dirdict = {"Nr":-1, "Fr":1}
        if self.STOPbutton.currentIndex() == 1:
            FocMaxSteps = int(self.read.getConstant(["FocMaxSteps"]))
            abspos, steps = int(".".join(re.findall(r'\d+', self.FocGUI.title()))), self.stepsbox.text() # read in position value
            steps = 1 if steps == "" else int(steps)# if no value set for steps
            #relative direction
            newpos = int(abspos) + int(steps)*dirdict[dir]
            if newpos >= 0 and newpos <= FocMaxSteps: # check the move is in the defined range 
                self.func.moverelative(abspos, dir, steps, self.driver)
                self.su.updateStatus(f"Focuser moved {dirtextdict[dir]}{steps} steps")
            else:
                self.su.updateStatus(f"Focuser move outside of 0-{FocMaxSteps} range", messagetype = "fail")
                raise Exception("focuser can't be moved out of range...")
        else:
            self.su.updateStatus(f"STOP TRIGGERED, release to continue...", messagetype = "fail")
            raise Exception("STOP TRIGGERED")

    def entermoveabs(self, abspos):
        """Moves to an absolute postion, making sure the move is in the focuser stepper motor range"""
        if self.STOPbutton.currentIndex() == 1:
            FocMaxSteps = int(self.read.getConstant(["FocMaxSteps"]))
            if int(abspos) >= 0 and int(abspos) <= FocMaxSteps: # check the move is in the defined range
                self.func.moveabsolute(int(abspos),self.driver)
                self.su.updateStatus(f"Focuser = {abspos} steps")
            else:
                self.su.updateStatus(f"Focuser move outside of 0-{FocMaxSteps} range", messagetype = "fail")
                raise Exception("focuser can't be moved out of range...")
        else:
            self.su.updateStatus(f"STOP TRIGGERED, release to continue...", messagetype = "fail")
            raise Exception("STOP TRIGGERED")
        
    def currentPosition(self):
        """finds where the focuser currently is"""
        pos = int(self.func.position(self.driver))
        self.su.updateStatus(f"Focuser = {pos} steps")
        return(pos)

    def setFocuserspeed(self, setspeed):
        "set the speed opf the focuser"
        actualspeeddict = {250:1, 125:2, 63:3, 32:4, 16:5} # derived from the input parameters to the focuser, shown in the manual
        self.func.setspeed(actualspeeddict[setspeed],self.driver) # set the speed
        self.su.updateStatus(f"Focuser speed = {setspeed} steps/s")

    def stopFocuser(self):
        """Stop the focuser in an emergency!"""
        self.func.emergencySTOP(self.driver) # set the speed
        self.su.updateStatus(f"FOCUSER STOPPED!!!")