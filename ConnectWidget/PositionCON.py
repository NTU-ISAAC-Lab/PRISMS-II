"""
NAME: PositionCON.py
AUTHOR: John Archibald Page
DATE CREATED: 28/11/2022 
DATE LAST UPDATED: 21/12/2023

PURPOSE:
    To Connect the functionality to the buttons of the position interface.
    up: click = move k  amount, if no k then move *** amount. 
    down: click = move k  amount, if no k then move *** amount. 
    anti-clockwise: click = move k  amount, if no k then move *** amount. 
    clockwise: click = move k  amount, if no k then move *** amount. 
    Azimuth: Prints current position. If input position, then move to this posiiton.
    Altitude: Prints current position. If input position, then move to this posiiton.
    set 0,0: clicked = current position becomes zero, have a double check on this

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import re
from Interfacing.StandaStand.StandaStand import StandaStand_class

class PositionCON_class():
    """connect the position buttons for position"""
    def __init__(self,GUI, position_class, connectfunctions, connectequipment, posdriver, statusUpdater, read, stopbutton):
        super(PositionCON_class,self).__init__()
        #initalise class, this also connects the device
        self.cf, self.ce, self.driver, self.su, self.read = connectfunctions, connectequipment, posdriver, statusUpdater, read
        #stop
        self.STOPbutton, self.posGUI = stopbutton, GUI
        #light stand
        self.lightpositionint = StandaStand_class(self.read)
        #call the references to different widgets
        self.textboxlist = self.cf.Textboxrefences(GUI)
        self.steps, self.azitext, self.alttext = self.textboxlist[2], self.textboxlist[0], self.textboxlist[1]
        self.buttonlist = self.cf.pushbuttonsrefences(GUI) # 0,0 button
        
        #lightgun azi-alt stand
        if self.ce.available[4] == True:
            try: 
                self.lightdriver = self.lightpositionint.connectStand(self.ce.deviceava[5], self.ce.deviceava[4])
                self.maxspeedpositionlight = float(self.read.getConstant(["LPosSpeed"]))
                self.lightpositionint.setSpeed(self.maxspeedpositionlight, self.lightdriver)
            except: self.su.updateStatus("Light Mount failed to connect...")
        else:
            self.su.updateStatus("Light Mount not connected...")
            
        #camera mount
        if self.ce.available[1] == True:
            try:
                self.func = position_class
                self.connectwidgets() #connect the buttons
                self.maxspeedposition = float(self.read.getConstant(["PosSpeed"])) #max speed of mount
                self.func.setSpeed(self.maxspeedposition, self.driver) #set mount speed
            except:
                self.su.updateStatus("Mount failed to connect...")
        else:
            self.su.updateStatus("Mount not connected...")
            
    #connect buttons functionality
    def connectwidgets(self):
        """Connect movement buttons"""
        #text input
        self.cf.widgetconnect(self.azitext,lambda: self.entermoveabs(self.azitext.text(), self.alttext.text()), clickedF=False, returnF=True,  thread = True)
        self.cf.widgetconnect(self.alttext,lambda: self.entermoveabs(self.azitext.text(), self.alttext.text()), clickedF=False, returnF=True,  thread = True)
        #buttons
        self.cf.widgetconnect(self.buttonlist[1],lambda: self.entermoveabs(self.azitext.text(), self.alttext.text()), thread = True)
        self.cf.widgetconnect(self.buttonlist[2],lambda: self.clickedmove("u"), thread = True)
        self.cf.widgetconnect(self.buttonlist[3],lambda: self.clickedmove("l"), thread = True)
        self.cf.widgetconnect(self.buttonlist[4],lambda: self.clickedmove("r"), thread = True)
        self.cf.widgetconnect(self.buttonlist[5],lambda: self.clickedmove("d"), thread = True)
        self.cf.widgetconnect(self.buttonlist[0],lambda: self.clickedzero(), thread = True)
        
    #functionality related to textinputs 
    def clickedmove(self,dir):
        """Movement when given button is clicked"""
        if self.STOPbutton.currentIndex() == 1:
            curazi, curalt = [float(i) for i in re.findall(r'[+-]?\d+(?:\.\d+)?', self.posGUI.title())]
            #directories to convert inputs to the correct format for the equipment functions
            textdict = {"u":curalt,"d":curalt,"l":curazi,"r":curazi}
            dirdict = {"u":"","d":"-","l":"-","r":""} 
            directiondict = {"u":"alt","d":"alt","l":"azi","r":"azi"}
            amount, curpos = self.steps.text(), textdict[dir]
            #move camera mount
            self.func.moverelative(curpos,dir,amount,self.driver)
            #try to move the light stand if listed as available
            if self.ce.available[4] == True:
                try: self.lightpositionint.moverelative(curpos,dir,amount,self.lightdriver)
                except: pass
            self.su.updateStatus(f"Mount moved {dirdict[dir]}{amount}\N{DEGREE SIGN} on {directiondict[dir]} axis")
        else:
            self.su.updateStatus(f"STOP TRIGGERED, release to continue...", messagetype = "fail")
            raise Exception("STOP TRIGGERED")

    def entermoverel(self,lineedit, dir):
        """When number is typed into the position of altitude or azimuth and enter is clicked, moves ot absolute poisition"""
        if self.STOPbutton.currentIndex() == 1:    
            amount = lineedit.text() # read in position value
            
            #if move is too big make the speed 4 times slower for safty reasons
            if amount > 10:
                #camera mount speed
                self.func.setSpeed(self.maxspeedposition/4, self.driver)
                #~~~try to move the light stand if listed as available~~~
                if self.ce.available[4] == True:
                    try: self.lightpositionint.setSpeed(self.maxspeedpositionlight/4, self.lightdriver)
                    except: pass

            #move camera mount
            self.func.moverelative(dir,amount,self.driver)
            self.func.setSpeed(self.maxspeedposition, self.driver)
            #~~~try to move the light stand if listed as available~~~
            if self.ce.available[4] == True:
                try: 
                    self.lightpositionint.moverelative(dir,amount,self.lightdriver)
                    self.lightpositionint.setSpeed(self.maxspeedpositionlight, self.lightdriver)
                except: pass
            #state movement
            self.su.updateStatus(f"Mount moved {amount}\N{DEGREE SIGN} on {dir} axis")
        else:
            self.su.updateStatus(f"STOP TRIGGERED, release to continue...", messagetype = "fail")
            raise Exception("STOP TRIGGERED")
        
    def entermoveabs(self, absposazi, absposalt):
        """When number is typed into the position of altitude or azimuth and enter is clicked, moves ot absolute poisition"""
        if self.STOPbutton.currentIndex()== 1:
            azi, alt = [float(i) for i in re.findall(r'[+-]?\d+(?:\.\d+)?', self.posGUI.title())] # current position
            if absposazi != "":
                #camer amount
                self.func.moveabsolute("azi",float(absposazi),self.driver)
                #~~~try to move the light stand if listed as available~~~
                if self.ce.available[4] == True:
                    try: self.lightpositionint.moveabsolute("azi",float(absposazi),self.lightdriver)
                    except: pass
            
            if absposazi == "":
                absposazi=azi
            if absposalt != "":
                #camer amount
                self.func.moveabsolute("alt",float(absposalt),self.driver)
                #~~~try to move the light stand if listed as available~~~
                if self.ce.available[4] == True:
                    try: self.lightpositionint.moveabsolute("alt",float(absposalt),self.lightdriver)
                    except: pass
            if absposalt == "":
                absposalt=alt
                
            self.su.updateStatus(f"Mount = ({float(absposazi)}\N{DEGREE SIGN}, {float(absposalt)}\N{DEGREE SIGN})")
        else:
            self.su.updateStatus(f"STOP TRIGGERED, release to continue...", messagetype = "fail")
            raise Exception("STOP TRIGGERED")

    def clickedzero(self):
        """When number is typed into the position of altitude or azimuth and enter is clicked, moves ot absolute poisition"""
        if self.STOPbutton.currentIndex()== 1:
            #camera mount
            self.func.setzero(self.driver)
            #~~~try to move the light stand if listed as available~~~
            if self.ce.available[4] == True:
                try: self.lightpositionint.setzero(self.lightdriver)
                except: pass
            self.su.updateStatus(f"Mount homed to (0\N{DEGREE SIGN},0\N{DEGREE SIGN})")
        else:
            self.su.updateStatus(f"STOP TRIGGERED, release to continue...", messagetype = "fail")
            raise Exception("STOP TRIGGERED")