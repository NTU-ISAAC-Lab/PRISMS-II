"""
Name: ConnectEquipment.py
Author: John Archibald Page
Created: 31/05/2023
Last Updated: 05/06/2023

Purpose: 
    To automatically connect the PRISMS II equipment using their unique VID, PID, and serial number. 
    These ID can be found via the "findequipmentID.py" script and updated at a later date.
    The cameras can not be checked using pyserial due to their drivers, so their respective modules will be ran to check they can connect instead.
    If the device is not available this will be noted and the system will be launch sans that functionality.

    *****If equipment is changed, make sure to update these IDS!!!!******

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import time
import serial.tools.list_ports
import serial
import pandas as pd
import andor3
#from thorcam.camera import ThorCam
#from Interfacing.RGBCamera.RGBCamera import MyThorCam

class ConnectEquipment_class():
    """For checking what serials are available and connecting to available devices"""
    def __init__(self):
        self.name, self.available, self.deviceava = self.checkDriver()

    def readIDs(self):
        """Read in the unique IDs fo the equipment"""
        df = pd.read_csv("InputFiles\\SerialPorts\\equipmentID.csv")
        return(df["component"],df["VID"],df["PID"],df["SerialNumber"],df["hwid"])

    def checkDriver(self):
        """Check the drivers are available for each driver"""
        available, deviceava = [False,False,False, False, False, False], [None,None,None,None, None, None] # this is two lists of 6length if the RGB camera is being interfaced
        ###RUN CHECKS FOR FOCUSER, FILTER, CAMERA MOUNT, AND LIGHT GUN MOUNT----------------------------------------
        #call in ids
        name, vid, pid, sn, hwid = self.readIDs()
         #loops through availbale ports and connects to ones with correct VID and PID
        device_list = serial.tools.list_ports.comports()
        for id in range(len(vid)):
            for device in device_list:
                #check whether the device existed
                if (str(device.hwid) == str(hwid[id])):
                    available[id] = True
                    deviceava[id] = device
                #As the filter serial hwid changes based on where it is plugged in (.i.e. SER= LOCATION=1-7.4.1), just look at the first 21 characters and ignore the location
                if "LOCATION" in str(device.hwid) and "LOCATION" in str(hwid[id]):
                    if (str(device.hwid)[:22] == str(hwid[id])[:22]):
                        available[id] = True
                        deviceava[id] = device
                        
        ####RUN CHECKS FOR THE CAMERA---------------------------------------------------------
        try:
            self.cam = andor3.Andor3()
            available[0] = True
        except:
            pass
        """
        try:
            print("Trying to connect to RGB camera...")
            self.rgbcam = MyThorCam()
            print("RGB camera connected!")
            available[4] = True
        except:
            print("RGB camera can not connect...")
        """
        return(name, available,deviceava)

    def connectDriver(self,device, br = 9600):
        """Connect focuser, filter, and stand driver"""
        #connect port
        driver = serial.Serial(port=str(device[0]), baudrate=br, timeout=.1)
        if(driver.isOpen() == False): #if not already connected, open the driver
                driver.open()
        else:
            print("Driver already open...")
        #pause, and clear the buffer
        time.sleep(1.5)
        pos = driver.read(64) # result back in bytes
        pos = pos.decode('ascii') # unpack as string
        time.sleep(1.5)
        return(driver)