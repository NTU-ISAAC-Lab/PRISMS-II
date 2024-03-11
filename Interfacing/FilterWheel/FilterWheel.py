"""
NAME: FilterWheel.py
AUTHOR: John Archibald Page
DATE CREATED: 29/11/2022 
DATE LAST UPDATED: 26/10/2023

PURPOSE:
    To write functionality to filter.
    From documentation:
        >Longest distance (5 filter positions or 180 degree wheel turn): 90ms
        >Adjacent filter transition: 30 ms

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    #28/11/2023: add a wait condition as there is no way to find out when filter is not busy. uses stated max filter time
"""
import struct

class FilterWheel_class():
    """Build the functionality for the filter controls, which takes binary commands given through serial"""
    def __init__(self):
        super(FilterWheel_class,self).__init__()
        
    def setFilterWheel(self, filter, driver, speed=7):
        """Set filter wheel to given filter at given speed. When command sent respond sent as command which can then be read."""
        filters = {0: "0000", 1: "0001", 2: "0010", 3: "0011", 4: "0100", 5: "0101", 6: "0110", 7: "0111", 8: "1000", 9: "1001"}
        speeds = {0: "000", 1: "001", 2: "010", 3: "011", 4: "100", 5: "101", 6: "110", 7: "111"}
        #binary message to send to filter wheel
        message = struct.pack(">B", int("0"+ speeds[speed] + filters[filter],2))
        driver.write(message)

    def readFilterWheel(self, driver):
        """read filter wheel position"""
        filters = {"70":0, "71":1, "72":2, "73":3, "74":4, "75":5, "76":6, "77":7, "78":8, "79":9}
        #binary message to send to filter wheel
        s = driver.readline()
        msg = bytes.hex(s, ' ')
        filternumberkey=str(msg.replace(" ", "").replace("0d", ""))
        if filternumberkey == "":
            filternumber = None
        else:
            filternumber = filters[filternumberkey]
        return(filternumber)