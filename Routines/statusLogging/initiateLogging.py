"""
NAME: initiateLogging.py
AUTHOR: John Archibald Page
DATE CREATED: 29/11/2022 
DATE LAST UPDATED: 30/11/2022

PURPOSE:
    To initiate the logging file that logs will be saved to. a new log will be created each day

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import logging as log
import datetime
#initalise program information---------------------------------
programname= "PRISMS II"       
author = "John Archibald Page"
creationdate = "30/11/2022"
updatedate =  "02/01/2024"
#initialise file name and path
logpath = "OutputFiles/Logs/"
logFile = "PRISMSII{}.log".format(datetime.datetime.now().date())

#----------------------------------------------------------------
#initalise log file
logfp = logpath + logFile
log.basicConfig(filename = logfp,level = log.NOTSET,filemode = 'a',format = '%(asctime)s: %(message)s',datefmt = '%m/%d/%Y %H:%M:%S', force=True)

#welcome message formatting
logo = ".~ " + programname + " ~."
im2 = "Author: " + author
im3 = "Created on: " + creationdate
im4 = "Last updated on: " + updatedate
is1 = "~"
is3 = " "
is4 = "-"

#calculations for the start message
messages = [len(im2),len(im3),len(im4),len(logo[0])]
width = max(messages)+1 # width of inital message

##start printing the initial message
log.info(is1*(width+2))
log.info(width*is3)
log.info(logo)
log.info(width*is3)
log.info(im2+is3*(width - len(im2)))
log.info(im3+is3*(width - len(im3)))
log.info(im4+is3*(width - len(im4)))
log.info(is1*width)
log.info("Initiating program...")