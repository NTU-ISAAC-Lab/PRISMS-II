"""
NAME: ScanAlgorithum.py
AUTHOR: John Archibald Page
DATE CREATED: 24/05/2023
DATE LAST UPDATED: 01/08/2023

PURPOSE:
    To run the scanning function of PRISMS II.

METHOD:
    0) initalise parameters and inputs
        > start time, input values, Exposure, Scan positions and file inputs
    ---#ENTER scannING ROUTINE#---
    0) Update the error message with current position in-case routine crashes
    1) Move to the position
    2) Autofocus on standard filter
        a) move the standard filter
        b) set the exposure to 30 ms
        c) Autofocusing routine begins:
            i)initalise parameters
            ii) make a number of parameter cases to run through the focus routine to get the image to focus
            iii) Run the defined parameter inputs until the image is focused or it fails
    3)save an image cube of the in focus cube
    4) repeat 0) to 3) Once all images complete make a pop-up stating the regime has finished

UPDATE HISTORY: 
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import time
import itertools
import numpy as np
import os

class Scan_class():
    """Functionality to run a scanning regime"""
    def __init__(self, captureFullImage, Autofocus, Autoexposure, standCON, filCON, scanCON, updateexposure, ScanGUI, read, save, statusUpdater, connectfunctions, popup):
        super(Scan_class,self).__init__()
        #function connect to the equipment
        self.standCON, self.filCON, self.exposureupdaterFUNC, self.scanCON = standCON, filCON, updateexposure, scanCON
        #routines
        self.cfi, self.af, self.ae = captureFullImage, Autofocus, Autoexposure
        #useful functions
        self.save, self.read,  self.su, self.cf, self.popup = save, read, statusUpdater, connectfunctions, popup
        #widgets
        self.widgetlist = self.cf.Textboxrefences(ScanGUI)
        self.aEbutton = self.cf.pushbuttonsrefences(ScanGUI)[0] #autoexposure button
        self.setEbutton = self.cf.pushbuttonsrefences(ScanGUI)[1] #set exposure button
        self.recoveryroutine_checkbox = self.cf.checkboxrefences(ScanGUI)[1] # whether to use a recovery file or not
        #list the widgets individually
        self.FOVW, self.FOVH, self.azistart,self.altstart,self.aziend,self.altend,self.Columns,self.Rows,self.Cubes,self.azioverlap,self.altoverlap = self.widgetlist[11:22]
        self.Name,self.Location, self.crashlocation = self.widgetlist[22:]

    def scanningRoutine(self, crashroutine = False):
        """The main routine for running a Scan PRISMS II. optexprat is the optimum exposure to find the focus as a ratio of the best exposure"""
        self.su.updateStatus(f"*SCANNING INITIATED...*", messagetype ="routine") 
        #-2)whether the incoming file is from a scan that half ran, where "CRASHED_" is is the file name
        if self.recoveryroutine_checkbox.isChecked() == True:
            foldername = self.Name.text() + "_RECOVERY"
            strt_cube = int(self.crashlocation.text())
            strt_idx = strt_cube - 1
            crashroutine = True
            self.su.updateStatus(f"RECOVERY ROUTINE... starting at cube {strt_cube}", messagetype ="routine")
        else:
            foldername = self.Name.text()
            strt_idx, strt_cube = 0, 1

        #-1) create a folder to store all of the scanning routine in form this run
        folder_counter = 0
        while os.path.isdir(self.Location.text() + f"\\{foldername}-{folder_counter}") == True:
            folder_counter += 1
        mosaic_dir = self.Location.text() + f"\\{foldername}-{folder_counter}"
        os.mkdir(mosaic_dir)

        #0) initalise parameters and inputs    
        starttime, standardfilter, optexp = time.time(), int(self.read.getConstant(["StandFil"])),  float(self.read.getConstant(["FocExp"]))
        #scanning input positons and file names
        try: Scanposlist = self.Scanpositions_costheta()
        except: self.popup.create("ERROR!","Defining positions...", "Error encountered while calling in Scan inputs,\n check that the Scan input locations are correct!","error")
        try: filenamelist = self.outputfilenames(Scanposlist,crashroutine = crashroutine) 
        except: self.popup.create("ERROR!","Defining filenames...", "Error encountered while calling in Scan inputs,\n check that the Scan input locations are correct!","error")
        print(filenamelist)
        #---#SCANNING BEGINS#---
        tot_ind = len(Scanposlist)
        self.su.updateStatus(f"GIVEN ALTITUDES OF SCAN AND COS(THETA) FACTOR, {tot_ind} CUBES AT POSITIONS = {Scanposlist}", messagetype ="routine") 
        try:
            self.standCON.entermoveabs(Scanposlist[strt_idx][0], Scanposlist[strt_idx][1])
            for i in range(tot_ind - strt_idx):
                #0) UPDATE THE CRASH LOCATION JUST IN CASE
                self.crashlocation.setText(str(strt_cube+i))
                #1) MOVE TO POSITION
                self.standCON.entermoveabs(Scanposlist[strt_idx+i][0], Scanposlist[strt_idx+i][1])
                #2) AUTOFOCUSING ROUTINE   
                #a) set the exposure to the optimum exposure for focusing
                self.exposureupdaterFUNC(optexp) 
                #b)set standard filter
                try: self.filCON.moveabsolute(standardfilter)
                except: self.popup.create("ERROR!","Moving Filter...", "Error encountered while calling in Scan inputs,\n check that the Scan input file is correct.","error")
                #c) run autofocusing routine using scanning inputs
                #in this list you could add more items if you wanted more attempts at normal routine (false) and worst case scenario (true)
                inFocusflag, focntr, opt_or_wcs_parms = False, 0, [False, False ,True] 
                while inFocusflag == False and focntr < len(opt_or_wcs_parms):
                    try: inFocusflag = self.af.autofocusIteration(wcs = opt_or_wcs_parms[focntr]) 
                    except: pass 
                    if opt_or_wcs_parms[focntr] == True:
                        self.su.updateStatus(f"Using worst-case-scenario autofocus routine!", messagetype ="routine") 
                    focntr += 1
                #(d) if still not in focus then a fail routine runs where the cube will still be taken but it should be re-taken in the future
                if inFocusflag == False:
                    filenamelist[strt_idx+i] = "blurflag_"+filenamelist[strt_idx+i] # flag this error on the file
                    self.popup.create("ERROR!","Focusing routine...", f"unable to focus for filename {filenamelist[strt_idx+i]}, azimuth:{Scanposlist[strt_idx+i][0]}, altitude:{Scanposlist[strt_idx+i][1]}\n, this cube will need repeating!","info") # this cube will have to be repeated but the scan will continue   
                #3)SAVE THE IMAGE CUBE
                self.cfi.saveimagecube(filename = mosaic_dir+"\\" +filenamelist[strt_idx+i], imagetype = "scan")
            #4) SCANNING COMPLETED
            self.popup.create("SCANNING COMPLETED :)","", f"Your files are stored in file location {self.Location.text()}","success")
            self.su.updateStatus(f"*SCANNING SUCCESS!* {round(time.time()-starttime,2)}s", messagetype ="success")
            self.crashlocation.setText("0") # reset the crash condition
        except:
            self.su.updateStatus(f"*SCANNING FAILED...*  {round(time.time()-starttime,2)}s", messagetype ="fail")
            self.popup.create("ERROR!","SCANNING FAILED :(", 
                                f"Scan Fail Position -> filename {filenamelist[strt_idx+i]}, azimuth:{Scanposlist[strt_idx+i][0]}, altitude:{Scanposlist[strt_idx+i][1]}, Cubes ran: {strt_idx+i}\{self.Cubes.text()} \n find the RECOVERY file at location {self.Location.text()} with file name RECOVERY_{self.Name.text()}.csv"
                                ,"error")
            vals = self.cf.readvaluesofwidget(self.widgetlist)
            self.save.filesave("scan",vals,self.Location.text()+"\\" +"RECOVERY_"+self.Name.text()+".csv")
        
#scanning positions and file names
    def outputfilenames(self, Scanposlist, crashroutine = False):
        """the outcoming names to be used in the order they will be imaged, naming convention = basename.row.column.tiff. Images in a snaking pattern starting from the bottom left."""
        #0) call in the values
        basename = self.Name.text()
        if crashroutine == True:
            basename = basename+"_RECOVERY"
        #1) Get the names of the initial rows
        #initalise constants
        filenamelist = []
        col_count, row_count = 0,0
        position_check = Scanposlist[0]
        #2)run a loop to get the column names based on the positions
        for i in Scanposlist:
            #the column position
            if position_check[0] < i[0]:  col_count = col_count + 1
            if position_check[0] > i[0]: col_count = col_count -  1
            #the row position
            if position_check[1] < i[1]: row_count  += 1 
            #update the check
            filenamelist.append("{}.{}.{}.tiff".format(basename,row_count,col_count))
            #update the check
            position_check = i

        return(filenamelist)
    
    def Scanpositions_costheta(self):
        """returns a chronilogical list of the positions the Scan will move to, following a snaking pattern starting with right to left
        TAKING INTO ACCOUNT COS(AZI) TO MAINTAIN AZIMUTH OVERLAP"""
        # Old prisms method
        #Azi_costheta = min(Scanposlist[:][0]) + (Scanposlist[strt_idx+i][0] - min(Scanposlist[:][0]))/np.cos((np.pi/180)*Scanposlist[strt_idx+i][1])
        #0) get the values
        AziFOV, AltFOV = float(self.FOVW.text()), float(self.FOVH.text())
        AziSt, AziEd = float(self.azistart.text()), float(self.aziend.text())
        AltSt, AziEd, Rows = float(self.altstart.text()), float(self.aziend.text()), float(self.Rows.text())
        AltOL =  float(self.altoverlap.text())
        #1) find range of azi and alt values that will be held
        altstep =  AltFOV - AltOL*AltFOV
        #2) make a list of alt positions that will be held
        altvalues = [AltSt+altstep*i for i in range(int(Rows))]
        #3) get the number of columns in each row
        minoverlap_rat = float(self.read.getConstant(["MinoverlapAzi"]))
        azivalues_list = []
        for x in altvalues: 
            AziFOV_costheta = AziFOV/np.cos((np.pi/180)*x)
            Columns, AziOL = self.scanCON.calculate_minimum_cubenumber_and_overlap(AziSt, AziEd, AziFOV_costheta, minoverlap_rat)
            azistep = AziFOV_costheta - AziOL*AziFOV_costheta
            azivalues = [AziSt+azistep*i for i in range(int(Columns))]
            azivalues = [round(i,3) for i in azivalues]
            azivalues_list.append(azivalues)
        #3) round to send nicer numbers to the positions
        altvalues =  [round(j,3) for j in altvalues] 
        #4) make lists of tupples of the positions and put into lists of the rows
        rowlists = [[(i,altvalues[j]) for i in azivalues_list[j]] for j in range(len(altvalues))]
        #5) then alternating reverse the order of every second row (.i.e. 1,3,5 index) due to snaking pattern
        for i in range(len(rowlists)):
            if (i % 2) != 0:
                rowlists[i].reverse()
        #6) join into one big list that will be the coordinates in order
        Scanposlist = list(itertools.chain.from_iterable(rowlists))
        return(Scanposlist)
    
    def Scanpositions(self):
        """returns a chronological list of the positions the Scan will move to, following a snaking pattern starting with right to left"""
        #0) get the values
        AziFOV, AltFOV = float(self.FOVW.text()), float(self.FOVH.text())
        AziSt, Columns = float(self.azistart.text()), float(self.Columns.text())
        AltSt, Rows = float(self.altstart.text()), float(self.Rows.text())
        AziOL, AltOL = float(self.azioverlap.text()), float(self.altoverlap.text())
        #1) find range of azi and alt values that will be held
        azistep, altstep = AziFOV - AziOL*AziFOV, AltFOV - AltOL*AltFOV
        #2) make a list of positions that will be held
        azivalues, altvalues = [AziSt+azistep*i for i in range(int(Columns))], [AltSt+altstep*i for i in range(int(Rows))]
        #3) round to send nicer numbers to the positions
        azivalues, altvalues = [round(i,3) for i in azivalues], [round(j,3) for j in altvalues] 
        #4) make lists of tupples of the positions and put into lists of the rows
        rowlists = [[(i,j) for i in azivalues] for j in altvalues]
        #5) then alternating reverse the order of every second row (.i.e. 1,3,5 index) due to snaking pattern
        for i in range(len(rowlists)):
            if (i % 2) != 0:
                rowlists[i].reverse()
        #6) join into one big list that will be the coordinates in order
        Scanposlist = list(itertools.chain.from_iterable(rowlists))
        return(Scanposlist)