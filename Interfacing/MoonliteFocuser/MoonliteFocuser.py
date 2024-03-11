"""
Name: MoonliteFocuser.py
Author: John Archibald Page
Date Created: 09/12/2022
Date Last Updated: 28/11/2023

Purpose: 
To control the moonlite focuser via the serial.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtCore
import logging as log

class Moonlite_class():
    """List of serial commands to control the moonlite focuser"""
    
    def __init__(self):
        super(Moonlite_class,self).__init__()

    def moveabsolute(self, pos, driver):
        command = ':SN{}# :FG#'.format(self.hex2complement(int(pos)))  # this is the command used to move
        command = command.encode() # encode to bytes
        driver.write(command)
        #chekc if finished moving before stating updated position
        isbusy = self.checkbusy(driver)
        while isbusy == "01#":
            isbusy = self.checkbusy(driver)

    def moverelative(self, pos, dir, steps, driver): #######
        #convert steps to int
        dirdict = {"Nr":-1, "Fr":1}
        steps = 1 if steps == "" else int(steps)# if no value set for steps
        #relative direction
        newpos = int(pos) + int(steps)*dirdict[dir]
        command = ':SN{}# :FG#'.format(self.hex2complement(newpos))  # this is the command used to move
        command = command.encode() # encode to bytes
        driver.write(command)

    def emergencySTOP(self, driver):
        command = ':FQ#'
        command = command.encode() # encode to bytes
        driver.write(command)

    def position(self, driver):
        command = ':GP#'
        command = command.encode() # encode to bytes
        driver.write(command)
        curthread = QtCore.QThread.currentThread() # the current thread this function is being ran on
        curthread.usleep(10)#usleep takes int of microseconds to wait, so convert ms to us
        pos = driver.read(10) # result back in bytes
        pos = pos.decode() # unpack as string
        pos = pos.replace('#', '') # remove # part of reply
        pos = int(pos, base=16)   #convert back to decimal
        ####FOCUSER BUG:Sometimes it reads the value in as (2**16 + 1) times higher, so if pos reads too high divide through by this value to correct it    
        if pos > 65537: #### change to max focus pos when possible
            pos = str(pos / 65537) 
        return(pos) # outputs decimal integer

    def checkbusy(self,driver):
        command = ':GI#'
        command = command.encode() # encode to bytes
        driver.write(command)
        moving = driver.read(10) #bytes
        moving = moving.decode() #decode
        if moving == "01#":
            moving = True
        else:
            moving = False
        log.info(f"Focuser Moving = {moving}")
        return(moving)

    def setstepsize(self,driver,size = 1):
        """Sets the step size used by the stepper motor"""
        log.info(f"Focuser step size = {size}")
        stepdict  ={1:':SF#' , 0.5:':SH#'} # full, half
        command = stepdict[size]
        command = command.encode() # encode to bytes
        driver.write(command)

    def setspeed(self,speed,driver):
        """set the speed the stepper motor moves, speed options 1-5, where 1 is fastest"""
        speeddict = {1:"02",2:"04",3:"08",4:"10",5:"20"} #  02, 04, 08, 10 and 20 -> stepping delay of 250, 125, 63, 32 and 16 steps per second
        log.info(f"Focuser speed = Setting {speed}")
        command = ':SD{}#'.format(speeddict[speed])
        command = command.encode() # encode to bytes
        driver.write(command)

    def hex2complement(self,number):
        hexadecimal_result = format(number, "03X")
        return(hexadecimal_result.zfill(4)) # .zfill(n) adds leading 0's if the integer has less digits than n