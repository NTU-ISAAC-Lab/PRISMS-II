"""
NAME: SaveCSV.py
AUTHOR: John Archibald Page
DATE CREATED: 13/12/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    save csv in specific format

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import pandas as pd
import numpy as np

#define the class
class Save_class():
    """Saving information in a csv file format"""
    def __init__(self):
        super(Save_class,self).__init__()  
        #dictionary of different labels for different files types
        self.scanlabels = ["whiteFoc", "Exp0", "Exp1", "Exp2", "Exp3", "Exp4", "Exp5", "Exp6", "Exp7", "Exp8", "Exp9", "AziFOV","AltFOV","AziStart","AltStart","AziEnd","AltEnd",
                   "Columns","Rows","Cubes","AziOverlap","AltOverlap","Name", "Location", "CrashLocation","AutoExposureCheck","SetExposureCheck","scaledistanceCheck","crashCheck"] # Scan
        self.slabels = ["Datetime","timeelapsed","Azimuth","Altitude", "Exposure","Focus","Filter"] # setup
        self.clabels = ["ExpLim", "ExpStrt", "WhiteStandardFile","EffSat", "EffSatScalRat","FullSatPerc","EffSatPerc","Bias","minclustersize", "maxsatcluster", "featurelimit", 
                        "FocRange","FocSpeed","DropRat","noiseFil", "focCheckSteps","FocRangeWCS","FocSpeedWCS","DropRatWCS","noiseFilWCS",
                        "focCheckStepsWCS","SensorW","SensorH", "minfDistance", "FocDistance", "FocExp","MinoverlapAzi","MinoverlapAlt", "LAzioffset", "LAltoffset", "LMinAzi","LMaxAzi","LMinAlt","LMaxAlt","LPosSpeed",
                    "CameratoLight", "LAzidegrat", "LAzisteprat", "LAltdegrat", "LAltsteprat","FocvsDistFile","MinAzi", 
                    "MaxAzi", "MinAlt", "MaxAlt", "PosSpeed", "FocMaxSteps","FocMaxSpeed", "FocDistoffset",
                    "StandFil","minFilt","maxFilt","Framerate","ImageW","ImageH","ROIW","ROIH","RollShutter","numberofupdates","UpdatetimeScaler"] #config
 
    def filesave(self,file,vals,filesavepath):
        """Save Scan,setup, or config in the correct format"""
        dictlabels = {"scan":self.scanlabels,"setup":self.slabels,"config":self.clabels}
        #make the format
        dfarray = np.c_[dictlabels[file.lower()],vals]
        df = pd.DataFrame(dfarray)
        df.to_csv(filesavepath,index=False, header=False)

    def datSave(self,vals,filepath, headerlist = "setup"):
        """save the setup at a given set-up"""
        #make the values into a dataframe
        df = pd.DataFrame(vals)
        #make the headers for the set-up, unless there is a different list put in
        hl = self.slabels if headerlist == "setup" else headerlist
        #save the dataframe
        df.to_csv(filepath, index=False, header=hl)