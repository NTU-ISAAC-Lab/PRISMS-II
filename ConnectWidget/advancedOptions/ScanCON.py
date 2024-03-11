"""
NAME: ScanCON.py
AUTHOR: John Archibald Page
DATE CREATED: 13/12/2022 
DATE LAST UPDATED: 21/11/2023

PURPOSE:
    the functionality of the scanning routine pop-up that allows you to make a scanning file
    
Methods/notes:
    Exposure:
        The exposure can be one of the following:
            1) a set value for each filter, found by taking a cube with autoexposure on the white
               and pulling in the exposure results from this file.
            2) autoexposure on every filter.
            3) Have a set exposure but scale by distance, this will only work if the light gun is also plugged in.
            
    Scanning region:  
        The angular field of view (AFOV) can be calculated from the following equation:
        
            AFOV = 2arctan(H/2f)
            
        where H is the height of the sensor, and f is the distance from the lens to the sensor, and sensor size is = 13.3 x 13.3 mm, 
    
        when inputting the start and end positions of the scan, the row length is calculated as follows:
        
            length = (n-2)*(FOV-2*O) + 2*(FOV-O) + (n-1)*O
            length = n*(FOV-O)+O
            
        where n is the cube number, FOV is the angular field of view and O is the overlap

        These cube numbers are then scalled by the altitude because of the cos(theta) factor brought in by the azi-alt coordinate system.
        Therefore, the final scan will fit in a "petal" shape with the higher rows having fewer cubes than lower rows for large altitdue changes.
        
    Filename and Location:
        This states where the files will be saved. A new folder will be made to store all of the mosaic.
        The file numbering system will be filename-row-column, and will be saved with a .dat file
        
    Crash routine:
        if the mosaicking crashes while running the crash cube will be saved and the routine can be continued from this cube

Reference:
    1)https://www.edmundoptics.co.uk/knowledge-center/application-notes/imaging/understanding-focal-length-and-field-of-view/ [Last Accessed: 19/12/2023]

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets,QtGui
import numpy as np
import re
import os
import math
import datetime
from GUI.SelfDefinedWidgets.popupMessage import popupmessage_class

class ScanCON_class():
    """To connect the functionality to the Mosiacking option"""
    def __init__(self, capturecubeCON, focGUI, AOGUI, Scanwindow, positionGUI, connectfunctions, save, read, saveopendir, AOwindow):
        super(ScanCON_class,self).__init__() 
        #initalise classes
        self.cf, self.sc, self.read, self.saveopendir, self.windowcreate, self.Scanwindow = connectfunctions,save,read, saveopendir,AOwindow, Scanwindow
        self.posGUI, self.FocGUI, self.cubeCON = positionGUI, focGUI, capturecubeCON
        #define the buttons
        self.Scanbutton = self.cf.pushbuttonsrefences(AOGUI)[0] # call in the set up button
        self.aebutton = self.cf.pushbuttonsrefences(self.Scanwindow)[0] 
        self.indbutton = self.cf.pushbuttonsrefences(self.Scanwindow)[1]
        self.whiteexpbutton = self.cf.pushbuttonsrefences(self.Scanwindow)[2]
        self.grabpos1button = self.cf.pushbuttonsrefences(self.Scanwindow)[3] 
        self.grabpos2button = self.cf.pushbuttonsrefences(self.Scanwindow)[4]
        self.grabfolderbutton = self.cf.pushbuttonsrefences(self.Scanwindow)[5] #back button
        #self.backbutton = self.cf.pushbuttonsrefences(self.Scanwindow)[6] #back button
        self.savebutton = self.cf.pushbuttonsrefences(self.Scanwindow)[7]  
        self.widgetlist = self.cf.Textboxrefences(self.Scanwindow)
        self.scanningregion = self.cf.tablerefences(self.Scanwindow)[0]
        self.scalewithdistancebox = self.cf.checkboxrefences(self.Scanwindow)[0]
        self.crashroutinebox = self.cf.checkboxrefences(self.Scanwindow)[1]
        #list the widgets individually
        self.FOVW, self.FOVH, self.azistart,self.altstart,self.aziend,self.altend,self.Columns,self.Rows,self.Cubes,self.azioverlap,self.altoverlap = self.widgetlist[11:22]
        self.Name,self.Location, self.crashlocation = self.widgetlist[22:]
        #connect functionality
        self.connectInputs()
        self.connectButtons()
        self.initalisewidgetValues()
        
#GUI creation and connecting widgets--------------------------------------------------------------------------------
    def runwindow(self):
        """Create an Set-up advanced options pop-up with options open previous set-up or save current set-up"""
        #messages, push buttons, and functionality of said buttons
        title, msgtitle, msg = "Scan", "Options", "Open existing Scan file or create new file."
        obutton, sbutton = QtWidgets.QPushButton("Open"), QtWidgets.QPushButton("Create")
        ofunc, sfunc= self.ScanopenFUNC, self.createScanfile
        #build pop up windows with these messages and the buttons
        self.window = self.windowcreate(title,msgtitle,msg,obutton,ofunc,sbutton,sfunc,col=False)
        self.window.show()

    def createScanfile(self):
        """Opens up a new file and closes the options menu"""
        self.Scanwindow.show()
        self.window.hide()

    def initalisewidgetValues(self):
        """set the widgets to have inital values"""
        self.widgetlist[0].setEnabled(False)  # the focus distance scaler
        self.cubeCON.exposureoptionFUNC(self.widgetlist[1:11], self.aebutton, self.indbutton, ae = False)
        self.update_AFOV(steps = int(self.read.getConstant(["FocRange"]))) 
        self.azioverlap.setText(str(self.read.getConstant(["MinoverlapAzi"])))
        self.altoverlap.setText(str(self.read.getConstant(["MinoverlapAlt"])))
        self.Name.setText("Scan-{}".format(datetime.datetime.now().date()))
        self.Location.setText(os.getcwd()+"\\OutputFiles\\Images\\")
        self.crashroutinebox.setChecked(False)
        self.crashroutineFUNC()

    def connectInputs(self):
        """The inputs are interdependant due to how the Scan is calculated. When the input is entered then otehr inputs will be updated"""
        self.cf.widgetconnect(self.azistart, self.scanningregionFUNC, clickedF = False, returnF = True, textchangedF = True)
        self.cf.widgetconnect(self.altstart, self.scanningregionFUNC, clickedF = False, returnF = True, textchangedF = True)
        self.cf.widgetconnect(self.aziend, self.scanningregionFUNC, clickedF = False, returnF = True, textchangedF = True)
        self.cf.widgetconnect(self.altend, self.scanningregionFUNC, clickedF = False, returnF = True, textchangedF = True)
        self.cf.widgetconnect(self.crashroutinebox, self.crashroutineFUNC, clickedF = False, statechangedF = True)
        
    def connectButtons(self):
        """Connect the buttons used in the Scan window"""
        self.cf.widgetconnect(self.Scanbutton, self.runwindow)
        self.cf.widgetconnect(self.savebutton, self.ScansaveFUNC)
        self.cf.widgetconnect(self.aebutton, lambda: self.cubeCON.exposureoptionFUNC(self.widgetlist[1:11], self.aebutton, self.indbutton, ae = True))
        self.cf.widgetconnect(self.indbutton, lambda: self.cubeCON.exposureoptionFUNC(self.widgetlist[1:11], self.aebutton, self.indbutton, ae = False))
        self.cf.widgetconnect(self.whiteexpbutton, lambda: self.cubeCON.grabWhite(self.widgetlist, self.aebutton, self.indbutton))
        self.cf.widgetconnect(self.scalewithdistancebox, lambda: self.cubeCON.FocusScalerFUNC(self.scalewithdistancebox, self.widgetlist[0], self.aebutton), clickedF=False, statechangedF = True)
        self.cf.widgetconnect(self.grabpos1button, lambda: self.grabcurrentPosition(self.azistart, self.altstart))
        self.cf.widgetconnect(self.grabpos2button, lambda: self.grabcurrentPosition(self.aziend, self.altend))
        self.cf.widgetconnect(self.grabfolderbutton, lambda: self.cubeCON.FolderopenFUNC(self.Location))

#Button functionality---------------------------------------------------------------------------------
    def ScansaveFUNC(self):
        """Functionality of save current current Scan inputs"""
        #1) call in the values
        vals = self.cf.readvaluesofwidget(self.widgetlist)
        #2) Save the crash routine function
        if self.crashroutinebox.isChecked() == False:
            vals[-1] = "0"
        #3) add in the button values
        vals.append(self.aebutton.isChecked())
        vals.append(self.indbutton.isChecked())
        #3) add in checkbox values
        vals.append(self.scalewithdistancebox.isChecked())
        vals.append(self.crashroutinebox.isChecked())
        #4) get the file name and save
        savopendir = self.saveopendir(savediropen="save", filepurpose= "Scan file", filepath = "\\InputFiles\\Scans\\", filetype="csv") # get the file name
        self.sc.filesave("scan",vals,savopendir.filename)
        self.popup = popupmessage_class("SCAN FILE SAVED!", f"{savopendir.filename}", "Scan file saved", "info")

    def ScanopenFUNC(self):
        """Functionality of open already saved Scan file set-up button"""
        #0) get the file name
        savopendir = self.saveopendir(savediropen="open", filepurpose= "Scan file", filepath = "\\InputFiles\\Scans\\", filetype="csv") # get the file name
        #1) get the data from the file and filter out nan values if they are there
        newvals = self.read.readcol(savopendir.filename) # call in new values from the folder
        newvals = ["" if i != i else i for i in newvals] # remove nan values for empty strings
        #2) update the values
        self.cf.setvaluesofwidget(self.widgetlist,newvals[:-4])#update values
        #3)sets the state of the exposure button depending on the values called in
        self.aebutton.setChecked(newvals[-4] == "True")
        self.indbutton.setChecked(newvals[-3] == "True")
        self.cubeCON.exposureoptionFUNC(self.widgetlist[1:11], self.aebutton, self.indbutton)
        #3.5) set the checked box options
        self.scalewithdistancebox.setChecked(newvals[-2] == "True")
        self.crashroutinebox.setChecked(newvals[-1] == "True")
        #4) if the recovery routine is not 0 then set the check button to true
        if newvals[-3] != "0":
            self.crashroutinebox.setChecked(True == "True")
        #5) show the window
        self.Scanwindow.show()
        self.window.hide()

    def grabcurrentPosition(self, aziinput, altinput):
        """grabs the current position of the mount and inputs to the scan inputs"""
        #update current AFOV
        self.update_AFOV()
        #get positions from the groupbox title
        azi, alt = re.findall(r'[+-]?\d+(?:\.\d+)?', self.posGUI.widget(0).title())
        #set the text boxes
        aziinput.setText(azi)
        altinput.setText(alt)
        #update the scaning region values
        self.scanningregionFUNC()
        
#Input functionality. These are interdependant and will be listed in order of appearance---------------------------------------------------------------------------------------------------------------------------------------          
    def scanningregionFUNC(self):
        """Updates the total azi/alt Scan region box when a value is entered and return is pressed for them inputs"""
        #0) call in the minimum value of overlap and the FOV
        OL_min = [float(i) for i in self.read.getConstant(["MinoverlapAzi","MinoverlapAlt"])]
        fovw_val, fovh_val = self.update_AFOV()
        #1) find the number of columnss and set the columns number.
        #this cas a cos theta factor to set to get the biggest FOV in the scan given the smallest altitude
        if self.altstart.text() != "":
            fovw_val = fovw_val/np.cos((np.pi/180)*float(self.altstart.text()))
        colnumber = self.update_columns_and_rows(self.Columns, self.azistart, self.aziend, fovw_val, self.azioverlap, OL_min[0])
        #2) find the number of rows and set the row number
        rownumber = self.update_columns_and_rows(self.Rows, self.altstart, self.altend, fovh_val, self.altoverlap, OL_min[1])
        #3) Cubes and the table shape      
        self.update_Cubes_and_Table(rownumber, colnumber)

    def crashroutineFUNC(self):
        """show whether this is a recovery file"""
        if self.crashroutinebox.isChecked() == True:
            self.crashlocation.setEnabled(True)
            self.crashlocation.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);") 
        else:
            self.crashlocation.setEnabled(False)
            self.crashlocation.setStyleSheet("background-color: #323232") 

#updating the widgets functions-------------------------------------------------------------------------------------------------------------------------
    def update_columns_and_rows(self, columnrowW, startW, endW, FOVW, overlapW, minoverlap):
        """From the inputted start and end positon with the FOV the columns and rows values are found"""
        if startW.text() != "" and endW.text() != "": # if start, end and fov values are input
            #1)find the column number assume overlap of the minimumcalculate_cubenumber(self, start, end, FOV, doverlap_rat)
            colrownumber, moverlap_rat = self.calculate_minimum_cubenumber_and_overlap(float(startW.text()), float(endW.text()), FOVW, minoverlap) 
            #2)update the column or row text
            columnrowW.setText(str(colrownumber))
            overlapW.setText(str(round(moverlap_rat,2)))
            return(colrownumber)

    def update_Cubes_and_Table(self, rownumber, colnumber, white=QtGui.QColor(255,255,255), red=QtGui.QColor(255,0,0) ,green = QtGui.QColor(0,255,0)):
        """update the shape of the table and the value of the Cubes if the volumns and rows widgets are filled"""
        if self.Columns.text() != "" and self.Rows.text() != "":
            self.Cubes.setText(str(colnumber*rownumber))
            #reset the current coloured cells to white
            tablerow, tablecol = self.scanningregion.rowCount(), self.scanningregion.columnCount()
            self.scanningregion.setItem(tablerow-1, 0, QtWidgets.QTableWidgetItem());self.scanningregion.setItem(0, tablecol-1, QtWidgets.QTableWidgetItem())
            self.scanningregion.item(0, tablecol-1).setBackground(white);self.scanningregion.item(tablerow-1, 0).setBackground(white) 
            #change the shape to the new scan shape
            self.scanningregion.setRowCount(rownumber);self.scanningregion.setColumnCount(colnumber)
            #2)set the start and end cube colour as green and red respectivly
            #start
            self.scanningregion.setItem(rownumber-1, 0, QtWidgets.QTableWidgetItem())
            self.scanningregion.item(rownumber-1, 0).setBackground(green)
            #end
            self.scanningregion.setItem(0, colnumber-1, QtWidgets.QTableWidgetItem())
            self.scanningregion.item(0, colnumber-1).setBackground(red) 

    def update_AFOV(self, steps = True):
        """update the angular FOV"""
        fovw_val, fovh_val = self.calculate_AngularFOV(steps = steps)
        self.FOVW.setText(str(fovw_val))
        self.FOVH.setText(str(fovh_val))
        return(fovw_val, fovh_val)

#calculations for the effective length and Cubes given overlap--------------------------------------------------------------------------------------------- 
    def calculate_minimum_cubenumber_and_overlap(self, start, end, FOV, minoverlap_rat, onecubeflag = False):
        """from the field of view and the angular length, find the overlap and cube number to fit the whole length"""  
        #-1) find the full FOV length: start and end aim at the centre of the FOV, so image captured is actually +/- FOV/2 on either side
        fullFOVlength = abs(start-end) + FOV 
        #0)find how many FOV fit into the scanning region (FOVfull), and if non-whole FOV remains (FOVpart)
        fullFOVlength_rat = fullFOVlength/FOV # number of FOV in the fullFOV length
        FOVpart, FOVfull = math.modf(fullFOVlength_rat)
        #1)the remaining cube outside this region, so 1-frac, will be put into the overlap
        totOLLength = (1-FOVpart)*FOV
        cubenumber = math.ceil(fullFOVlength_rat)
        #2) run conditions for if the FOV does not fit exactly
        #a)if FOV fit exactly in, then add another FOV cube, this will all be tucked into the overlap
        if float(totOLLength) == float(FOV) and cubenumber > 1:
            cubenumber += 1
        #b) if the cubenumber is 1, meaning the scanning region is exactly 1 FOV or less, make the overlap 1
        if float(totOLLength) == float(FOV) and cubenumber == 1:
            onecubeflag = True
            cubenumber = 1
            OL_rat = 1 
        #3)find the overlap ratio and the number of FOV
        if onecubeflag == False:
            OLnum = cubenumber - 1 # how many overlaps between Cubes
            OL_rat = (totOLLength/OLnum)/FOV #the ratio of a FOV the overlap is between each intersection
            #make sure bigger than the minimum overlap, add one cube until this condition is met
            ccounter = 1
            while OL_rat < minoverlap_rat:
                totOLLength = FOV*((1-FOVpart)+ccounter)
                cubenumber += 1
                OLnum = cubenumber - 1 # how many overlaps between Cubes
                OL_rat = (totOLLength/OLnum)/FOV #the ratio of a FOV the overlap is between each intersection
                ccounter = ccounter + 1
        return(cubenumber, OL_rat)
    
    def calculate_AngularFOV(self, steps = True): 
        """Based on the current focus position calculates the angular FOV (AFOV): AFOV = 2arctan(H/2f)"""
        #call in variables and constants
        SenW, SenH, minf, Focdistancerange, Focstepsrange = [float(i) for i in self.read.getConstant(["SensorW","SensorH", "minfDistance", "FocDistance", "FocMaxSteps"])]
        #used when initalising the system
        if steps == True:
            currentSteps = int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0])
        else:
            currentSteps = steps
        #to convert from radians to degrees
        rad_to_deg = 1/0.0174533 
        #Focal distance = minimum focal distance + steps distance
        f = minf + currentSteps*(Focdistancerange/Focstepsrange)
        #angular fov
        fovw = round(2*np.arctan((SenW*10**(-3))/(2*f))*rad_to_deg, 2)
        fovh = round(2*np.arctan((SenH*10**(-3))/(2*f))*rad_to_deg, 2)
        return(fovw, fovh) # converted to degrees