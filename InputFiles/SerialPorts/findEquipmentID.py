"""
Name: findequipmentIDs.py
Author: John Archibald Page
Created: 01/06/2023
Last Updated: 01/06/2023

Purpose: 
    To find the VID, PID, Serial number and hwid of USB drivers.
    run the script in the command line and the values for the current plugged in
    USB driver will print out.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
#import standard module
import serial.tools.list_ports
import usb.core

class findequipmentIDs_class():
    """For checking what serials are available and connecting to available devices"""
    
    def __init__(self):
        self.checkDriver()
        self.checkdriver_usb()

    def checkDriver(self):
        """Connect driver using serial"""
         #loops through availbale ports and connects to ones with correct VID and PID
        device_list = serial.tools.list_ports.comports()
        print(f"Number of devices to check... {len(device_list)}")
        print("VID PID SerialNumber hwid")
        for device in device_list:
            print(str(device.vid)," ||| ",str(device.pid)," ||| ",str(device.serial_number)," ||| ", str(device.hwid))
 
    def checkdriver_usb(self):
        """Check the using pyusb"""
        # find USB devices
        dev = usb.core.find(find_all=True)
        print(f"-----------------")
        # loop through devices, printing vendor and product ids in decimal and hex
        for cfg in dev:
            print('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
            print('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')

if __name__ == "__main__":
    findequipmentIDs_class()