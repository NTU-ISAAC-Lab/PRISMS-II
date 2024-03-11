'''
NAME: ReadCSV.py
AUTHOR: John Archibald Page
DATE CREATED: 13/12/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
read in a csv to interact with files

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
'''
import pandas as pd
import os

class Read_class():
    """Reading the config file"""
    def __init__(self):
        super(Read_class,self).__init__()   

#generic useful functions
    def readcol(self,filename, col=1, header = None):
        """Reads in a CSV file values"""
        df = pd.read_csv(filename,header = header)
        values = df[col] #values to input to the lineedits
        return(values)

    def readrow(self,filename, row=1):
        """Reads in a CSV file values"""
        df = pd.read_csv(filename,header = None)
        values = df.loc[row] #values to input to the lineedits
        return(values)

    def readval(self,filename, row = 1,col=1):
        """Reads in a CSV file values"""
        df = pd.read_csv(filename,header = None)
        values = df.loc[row,col] #values to input to the lineedits
        return(values)

#get variable from a specific file
    def getConstant(self, constant):
        """Get a constant/ list of constants from a file"""
        configfiledir = os.environ["CONFIGFILEPATH"]
        constntnames = self.readcol(configfiledir, col= 0) 
        constantvals = self.readcol(configfiledir)
        dictconstants = {constntnames[i]:constantvals[i] for i in range(len(constantvals))}
        #for the called constants get a list
        constantslist = []
        for i in range(len(constant)):
            constantslist.append(dictconstants[constant[i]])
        #if it is only one constant then return the one constant
        if len(constantslist) == 1:
            constantslist = constantslist[0]
        return(constantslist)