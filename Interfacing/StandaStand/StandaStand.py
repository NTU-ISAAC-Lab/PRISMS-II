"""
NAME: StandaStand.py
AUTHOR: John Archibald Page
DATE CREATED: 31/01/2022 
DATE LAST UPDATED: 31/01/2023

PURPOSE:
    To write functionality to stand, using zaber-motion python library.
    this funcitonality will be set to buttons in seperate document
    max speed = 60 deg/s
    **may need to reset where the home location is

    PYTHON LIBRARY: libximc
    INSTALL VIA COMMANDLINE: pip install libximc
    DOCUMENTATION: https://doc.xisupport.com/en/8smc5-usb/8SMCn-USB/Programming/Communication_protocol_specification.html#all-controller-commands [Last Accessed 31/01/2023]
    
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
""" 
import time
import libximc.highlevel as ximc
import re
#self defined module
from ConnectWidget.advancedOptions.ConnectEquipment import ConnectEquipment_class

class StandaStand_class():
    """Build the functionality for the position controls"""
    def __init__(self, read): 
        super(StandaStand_class,self).__init__()
        #initalise class
        self.ce, self.read = ConnectEquipment_class(), read 
        #hard coded limits
        self.LMinAzi,self.LMaxAzi,self.LMinAlt,self.LMaxAlt = [float(i) for i in self.read.getConstant(["LMinAzi","LMaxAzi","LMinAlt","LMaxAlt"])]
    
    #functions for connecting and writing to the devices
    def connectStand(self, device1, device2):
        """Connect the light gun stand (Standa)"""
        #if self.ce.available[4] == True:
        #get the com number from the device
        dev1com = str(re.findall(r'\d+', str(device1))[0])
        dev2com = str(re.findall(r'\d+', str(device2))[0])
        #get the axis
        self.axis1 = ximc.Axis(r"xi-com:\\.\COM" + dev1com)
        self.axis2 = ximc.Axis(r"xi-com:\\.\COM"+ dev2com)
        #name the axis
        self.axis1.open_device()
        self.axis2.open_device()
        #set configuration
        self.configStand([self.axis1, self.axis2])
        return(self.axis1, self.axis2) 

    def configStand(self, device_list):
        """Connect the light gun stand (Standa)"""
        #grab the callabration values from the config file
        Azideg, Azistep, Altdeg, Altstep = [float(i) for i in self.read.getConstant(["LAzidegrat", "LAzisteprat", "LAltdegrat", "LAltsteprat"])]
        #set the calibration
        Aziscaler, Altscaler = Azideg/Azistep, Altdeg/Altstep
        device_list[0].set_calb(Aziscaler, ximc._flag_enumerations.MicrostepMode.MICROSTEP_MODE_FULL)
        device_list[1].set_calb(Altscaler, ximc._flag_enumerations.MicrostepMode.MICROSTEP_MODE_FULL)
        #set the settings
        device_list[0].set_feedback_settings(ximc.feedback_settings_t(4000, ximc._flag_enumerations.FeedbackType.FEEDBACK_ENCODER, ximc._flag_enumerations.FeedbackFlags.FEEDBACK_ENC_REVERSE,4000))
        device_list[1].set_feedback_settings(ximc.feedback_settings_t(4000, ximc._flag_enumerations.FeedbackType.FEEDBACK_ENCODER, ximc._flag_enumerations.FeedbackFlags.FEEDBACK_ENC_REVERSE,4000))
        #reset locks on axis just in case
        ximc.reset_locks()
        return(self.axis1, self.axis2)  

    #sending commands to the device
    def moverelative(self,curpos,dir,amount, device_list):
        """Moves amount in unit degrees relative to current position"""
        #offset
        self.AziO, self.AltO = [float(i) for i in self.read.getConstant(["LAzioffset", "LAltoffset"])]
        #if nothing written in the input, moves 1 degrees
        amount = 1 if amount == "" else float(amount)
        #initalise dictionaries and devices
        reldict = {"u":1,"d":-1,"l":-1,"r":1} # relative directions
        axisOdict = {"u":self.AltO, "d":self.AltO,"l":self.AziO, "r":self.AziO}
        axisdict = {"u":device_list[1],"d":device_list[1],"l":device_list[0],"r":device_list[0]} # what axis is used
        #check limits
        newpos = amount*reldict[dir]+ float(curpos) + axisOdict[dir] # new position after being moved
        if (dir == "u" and newpos > self.LMaxAlt) or (dir == "d" and newpos < self.LMinAlt) or (dir == "l" and newpos < self.LMinAzi) or (dir == "r" and newpos > self.LMaxAzi):
            pass  #move out of range: Altitude -60 to 60
        else:
            axisdict[dir].command_movr_calb(amount*reldict[dir] + axisOdict[dir]) 
            
    def moveabsolute(self,dir,abspos,device_list):
        """Moves to absolute position in degrees. the lineedit boxes, defined in GUI, 
        have limited inputs to stop going beyond mechanical limits: Altitude -60 to 60"""
        #offset
        self.AziO, self.AltO = [float(i) for i in self.read.getConstant(["LAzioffset", "LAltoffset"])]
        #write to a given axis
        axisdict = {"alt":device_list[1],"azi":device_list[0]}
        axisOdict = {"alt":self.AltO,"azi":self.AziO}
        #make sure hard limits are met
        axisdict[dir].command_move_calb(float(abspos) + axisOdict[dir])

    def setzero(self,device_list):
        """Sets the stand back to altitude, azimuth 0,0 degrees. This can be physically seen on the stand."""
        self.moveabsolute("alt",0,device_list)#altitude
        self.moveabsolute("azi",0,device_list)#azimuth

    def emergencySTOP(self,device_list):
        """Stops all motion and freezes further motion from the zaber stand"""
        device_list[0].command_stop()
        device_list[1].command_stop()

    def setSpeed(self, val, device_list):
        """Set the speed of both axis"""
        #get the current settings
        Azicurset = device_list[0].get_move_settings_calb()
        Altcurset = device_list[1].get_move_settings_calb()
        #set both axis to the same speed
        device_list[0].set_move_settings_calb(ximc.move_settings_calb_t(int(val),Azicurset.Accel,Azicurset.Decel,Azicurset.AntiplaySpeed,Azicurset.MoveFlags))
        device_list[1].set_move_settings_calb(ximc.move_settings_calb_t(int(val),Altcurset.Accel,Altcurset.Decel,Altcurset.AntiplaySpeed,Altcurset.MoveFlags))
        
    def currentposition(self,device_list):
        """Returns current position of stand"""
        altpos = float(device_list[0].get_position_calb().Position) # .get_position() <- steps not user units
        azipos = float(device_list[1].get_position_calb().Position) # .get_position() <- steps not user units
        return(azipos,altpos)
    
    def busycheck(self,device_list):
        """Check if stand is moving in any direction"""
        aziaxbusy = True if bool(device_list[0].get_status().MoveSts) else False
        altaxbusy = True if bool(device_list[1].get_status().MoveSts) else False
        return(aziaxbusy,altaxbusy)
    
if __name__ == "__main__":
    StandaStand_class()