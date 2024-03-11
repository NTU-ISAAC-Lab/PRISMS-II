"""
NAME: ZaberStand.py
AUTHOR: John Archibald Page
DATE CREATED: 05/12/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    To write functionality to stand, using zaber-motion python library.
    this funcitonality will be set to buttons in seperate document
    max speed = 60 deg/s

    PYTHON LIBRARY: zaber_motion
    INSTALL VIA COMMANDLINE: pip install zaber_motion
    DOCUMENTATION: https://www.zaber.com/software/docs/motion-library/ascii/references/python/ [Last Accessed 07/12/2022]

NB:
    If you update the firmware, this will flip the axis sometimes, so the device numbers may need to be switched!!!!
    
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
""" 
from zaber_motion import Units, Library
from zaber_motion.ascii import Connection
#self defined module
from ConnectWidget.advancedOptions.ConnectEquipment import ConnectEquipment_class

class ZaberStand_class():
    """Build the functionality for the position controls"""
    def __init__(self, read):
        super(ZaberStand_class,self).__init__()
        #initalise class
        self.ce, self.read = ConnectEquipment_class(), read
        #hard coded limits
        self.MinAzi,self.MaxAzi,self.MinAlt,self.MaxAlt = [float(i) for i in self.read.getConstant(["MinAzi","MaxAzi","MinAlt","MaxAlt"])]
        
    #functions for connecting and writing to the devices
    def connectStand(self):
        Library.enable_device_db_store()
        if self.ce.available[1] == True:
            #open using the zabermotion internal function
            connection = Connection.open_serial_port(self.ce.deviceava[1].name)
            device_list = connection.detect_devices()
        return(device_list)   

    def deviceList(self,device_list):  
        """Output the stepper motor references""" 
        altitude = device_list[0] #77260= horizontal pivot/azimuth 
        azimuth = device_list[1] #77261  = verital pivot
        altitudeaxis = altitude.get_axis(1)   
        azimuthaxis = azimuth.get_axis(1)
        return(azimuthaxis,altitudeaxis)

    #sending commands to the device
    def moverelative(self,curpos,dir,amount,device_list):
        """Moves amount in unit degrees relative to current position"""
        #if nothing written in the input, moves 1 degrees
        amount = 1 if amount == "" else float(amount)
        #initalise dictionaries and devices
        aziax,altax = self.deviceList(device_list)
        reldict = {"u":1,"d":-1,"l":-1,"r":1} # relative directions
        axisdict = {"u":altax,"d":altax,"l":aziax,"r":aziax} # what axis is used
        #check limits
        newpos = amount*reldict[dir]+ float(curpos) # new position after being moved
        if (dir == "u" and newpos > self.MaxAlt) or (dir == "d" and newpos < self.MinAlt) or (dir == "l" and newpos < self.MinAzi) or (dir == "r" and newpos > self.MaxAzi):
            pass#Zaber Stand move out of range: Altitude -60 to 60"
        else:
            axisdict[dir].move_relative(amount*reldict[dir], Units.ANGLE_DEGREES) #"Zaber Stand has moved {} degrees to new position {}
            
    def moveabsolute(self,dir,abspos,device_list):
        """Moves to absolute position in degrees. the lineedit boxes, defined in GUI, 
        have limited inputs to stop going beyond mechanical limits: Altitude -60 to 60"""
        abspos = float(abspos)
        #write to a given axis
        aziax,altax = self.deviceList(device_list)
        axisdict = {"alt":altax,"azi":aziax}
        #make sure hard limits are met
        axisdict[dir].move_absolute(abspos, Units.ANGLE_DEGREES)

    def currentposition(self,device_list):
        """Returns current position of stand"""
        aziax,altax = self.deviceList(device_list)
        altpos = altax.get_position(unit = Units.ANGLE_DEGREES)
        azipos = aziax.get_position(unit = Units.ANGLE_DEGREES)
        return(azipos,altpos)

    def setzero(self,device_list):
        """Sets the stand back to altitude, azimuth 0,0 degrees. This can be physically seen on the stand."""
        #altitude
        self.moveabsolute("alt",0,device_list)
        #azimuth
        self.moveabsolute("azi",0,device_list)
   
    def busycheck(self,device_list):
        """Check if stand is moving in any direction"""
        #call in the devices
        altax,aziax = self.deviceList(device_list)
        #check if busy
        aziaxbusy = True if aziax.is_busy() else False
        altaxbusy = True if altax.is_busy() else False
        return(aziaxbusy,altaxbusy)

    def emergencySTOP(self,device_list):
        """Stops all motion and freezes further motion from the zaber stand"""
        altax,aziax = self.deviceList(device_list)
        altax.stop()
        aziax.stop()
        altax.wait_until_idle() # no new functions until this is stopped
        aziax.wait_until_idle() # no new functions until this is stopped

    def setSpeed(self, val, device_list):
        """Set the speed of both axis"""
        altax,aziax = self.deviceList(device_list)
        #speed = altax.settings.get("maxspeed", Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND)
        #set both axis to the same speed
        altax.settings.set("maxspeed", val, Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND)
        aziax.settings.set("maxspeed", val, Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND)