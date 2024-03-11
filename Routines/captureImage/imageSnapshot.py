"""
NAME: imageSnapshot.py
AUTHOR: John Archibald Page
DATE CREATED: 26/07/2023
DATE LAST UPDATED: 26/07/2023

PURPOSE:
    To capture an image of one band, at whichever filter is set at the time the snapshot is taken

METHOD:
    1) capture image
    2) save as one image with a .dat file

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
#import standard modules
import tifffile
import numpy as np

class captureImageSnapshot_class():
    """Functionality to capture an image with the full range of filters"""
    def __init__(self, cameradriver, saveopendir, SetupCON, save, statusUpdater):
        super(captureImageSnapshot_class,self).__init__()
        self.saveopendir, self.SetupCON, self.sv, self.su , self.camera = saveopendir, SetupCON, save, statusUpdater, cameradriver

    def savesnapshot(self, filename = False):
        """Functionality of save current set-up button"""
        self.su.updateStatus(f"*CAPTURING SNAPSHOT...*", messagetype ="routine")
        #1)take the images at the found exposures for different filters
        image = np.array(self.camera.currentimage)
        image = np.rot90(image,3)
        imagedat = self.SetupCON.setupsaveFUNC()
        try:
            #2)Get the filename and savepath
            if filename == False:
                savopendir = self.saveopendir(savediropen="save",filepurpose= "Save image snapshot", filepath = "\\OutputFiles\\Images\\", filetype="image") # get the file name
                filenamepath = savopendir.filename
            else:
                filenamepath = filename
            #2a) save dat file
            filenamedat = filenamepath[:-5]+".csv"
            filename = filenamepath[:-5].split('/')[-1]
            self.sv.datSave(imagedat,filenamedat)
            #2b)save image file
            tifffile.imwrite(filenamepath, image)
            self.su.updateStatus(f"*{filename}.TIFF SAVED!*", messagetype ="success")
        except:
            self.su.updateStatus(f"*SAVE CANCELLED...*", messagetype ="fail")