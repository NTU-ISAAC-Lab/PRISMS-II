
"""
NAME: ScanGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 26/06/2023 
DATE LAST UPDATED: 11/10/2023 

ScanCreate_class -> interactive GUI to create a file to run a Scan, or open file into this folder
________________________________
|@|Create Scan              |X| |
|-------------------------------|            
|_Exposure_time________________ |  
| |autoexposure|  |setexposure| |
||filter: 1 2 3 4 5 6 7 8 9 10 ||  
||Set-exp| | | | | | | | | | | ||
|_Mosacing Region_______________| 
|| FOV  |-----------|     rows ||
|| Start|           |     x    ||
|| End  |           |   Columns||
||      |-----------|     Cubes||
|_overlap______________________ |  
||thetaol, Phiol: |      |    |||
|_File_Name_&_Save_Location____ |  
||file name:     |         |   ||  
||Save location: |         |   ||
|_CRASH ROUTINE________________ |  
||Cube number: |         |  |x|||  
|------------------------------||                
|Back|                |SAVE|RUN||
--------------------------------
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from GUI.SelfDefinedWidgets.InputLayouts import bracketInput, numberInput, labelledInput

class ScanCreate_class(QtWidgets.QWidget):
    """This is a pop-up class which creates a csv. Scan file that can be ran or saved"""
    def __init__(self, read):
       super(ScanCreate_class,self).__init__()
       self.read = read
       self.buildpopup()
       self.setWindowTitle("Create Scan Config. File") # title of window
       self.setWindowIcon(QtGui.QIcon('GUI/Images/Logo.png'))
       
    def buildpopup(self):
        """Build the layout of the pop up"""
        #call in widgets to build layout
        etgroupbox = self.Exposuretime()
        pigroupbox = self.ScanRegion()
        cgroupbox = self.Overlap()
        flgroupbox = self.filenameandloc() 
        crshgroupbox = self.CrashSection()
        button1, button2, button3 = self.Buttons()
        #define layouts
        VLayout = QtWidgets.QVBoxLayout()
        HLayout = QtWidgets.QHBoxLayout()
        #build button layout
        HLayout.addWidget(button1)
        HLayout.addWidget(button2)
        HLayout.addWidget(button3)
        #build overall layout
        VLayout.addWidget(etgroupbox)
        VLayout.addWidget(pigroupbox)
        VLayout.addWidget(cgroupbox)
        VLayout.addWidget(flgroupbox)
        VLayout.addWidget(crshgroupbox)
        VLayout.addLayout(HLayout)
        #put layout to ,main widget
        self.setLayout(VLayout)
 
    def Exposuretime(self):
        """sublayout exposure time with options of auto exposure, scalled to channel 5 or mnually set each channel"""   
        #buttons auto-exposure, ratio, all-set
        aebutton,indbutton = QtWidgets.QPushButton("AutoExposure"), QtWidgets.QPushButton("Set-Exposure")
        #set hints
        aebutton.setToolTip("Autoexpose every filter.")
        indbutton.setToolTip("Each filter exposure is fixed throughout the scan.")
        #make buttons checkable
        aebutton.setCheckable(True)
        indbutton.setCheckable(True)
        #make the layout
        H0Layout = QtWidgets.QHBoxLayout()
        H0Layout.addWidget(aebutton,5)
        H0Layout.addWidget(indbutton,5)
        gridlayout = QtWidgets.QGridLayout()
        gridlayout.addWidget(QtWidgets.QCheckBox("Scale-with-Distance?"), 1,0)
        gridlayout.addWidget(QtWidgets.QLabel("Set-Exposure Focus"),0,1)
        focusposlineedit = QtWidgets.QLineEdit()
        focusposlineedit.setFixedWidth(100)
        focusposlineedit.setToolTip("Focus position of the set Exposure")
        gridlayout.addWidget(focusposlineedit,1,1)
        H0Layout.addLayout(gridlayout, 5)
        #Filter 0 1 2 3 4 5 6 7 8 9
        Filterlabel = QtWidgets.QLabel("Filter: ")
        H2Layout = QtWidgets.QHBoxLayout()
        H2Layout.addWidget(Filterlabel)
        #add all the filter labels
        for i in range(10):
            numlabel = QtWidgets.QLabel(str(i))
            H2Layout.addWidget(numlabel)
        #Set exposure | | | | | | | | | | |
        setexposurelabel = QtWidgets.QLabel("Set Exp (ms): ")
        H3Layout = QtWidgets.QHBoxLayout()
        H3Layout.addWidget(setexposurelabel)
        #add all the input boxes
        for i in range(10):
            Value = numberInput(f"Filter {i}",  0, 1000, enabled = True, width = False) 
            H3Layout.addWidget(Value)
        whiteexpbutton = QtWidgets.QPushButton(u"\u25A0")
        whiteexpbutton.setToolTip("Grab Exposure from White")
        whiteexpbutton.setStyleSheet("font-size: 24pt;")
        H3Layout.addWidget(whiteexpbutton) #add the grab the exposure from the white function
        V2Layout = QtWidgets.QVBoxLayout()
        V2Layout.addLayout(H0Layout)
        V2Layout.addLayout(H2Layout)
        V2Layout.addLayout(H3Layout)
        groupbox2 = QtWidgets.QGroupBox("Exposure Options")
        groupbox2.setLayout(V2Layout)
        return(groupbox2)

    def ScanRegion(self):
        """sublayout of the Scan positioning"""   
        #value displays: column, row, Total Cubes
        columnlayout = labelledInput("Columns: ", "Number of columns in Scan",  minlim = 0, maxlim = 1000, enabled = False, width = 100)
        rowlayout = labelledInput("Rows: ", "Max Number of rows in Scan",  minlim = 0, maxlim = 1000, enabled = False, width = 100)
        cubelayout = labelledInput("Total Cubes: ", "Number of Cubes",  minlim = 0, maxlim = 1000, enabled = False, width = 100)
        #inputs
        Mountlim = [float(i) for i in self.read.getConstant(["MinAzi","MaxAzi","MinAlt","MaxAlt"])]
        bracketHLayout0  = bracketInput(f"FOV (Azi\N{DEGREE SIGN},Alt\N{DEGREE SIGN}):", "Azi\N{DEGREE SIGN}", "Alt\N{DEGREE SIGN}", buttontitle = False,
                                       minlim1 = 0, maxlim1 = 20, minlim2 = 0, maxlim2 = 20, enabled = False)
        bracketHLayout1  = bracketInput(f"First Cube (Azi\N{DEGREE SIGN},Alt\N{DEGREE SIGN}):", "First Azi\N{DEGREE SIGN}", "First Alt\N{DEGREE SIGN}", tip3 = "Grab current position",
                                       buttontitle = u"\u2316", minlim1 = Mountlim[0], maxlim1 = Mountlim[1], minlim2 = Mountlim[2], maxlim2 = Mountlim[3], colours = "green")
        bracketHLayout2 = bracketInput(f"Last Cube (Azi\N{DEGREE SIGN},Alt\N{DEGREE SIGN}):", "Last Azi\N{DEGREE SIGN}", "Last Alt\N{DEGREE SIGN}", tip3 = "Grab current position",
                                       buttontitle = u"\u2316", minlim1 = Mountlim[0], maxlim1 = Mountlim[1], minlim2 = Mountlim[2], maxlim2 = Mountlim[3], colours = "red")
        #changing table widget
        scanningregion = QtWidgets.QTableWidget()
        scanningregion.setEnabled(False)

        #initalise the table as 4x4
        scanningregion.verticalHeader().setVisible(False)
        scanningregion.horizontalHeader().setVisible(False)
        scanningregion.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        scanningregion.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        scanningregion.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scanningregion.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scanningregion.horizontalHeader().setDefaultSectionSize(100)
        scanningregion.horizontalHeader().setMinimumSectionSize(1)
        scanningregion.verticalHeader().setDefaultSectionSize(100)
        scanningregion.verticalHeader().setMinimumSectionSize(1)
        scanningregion.setRowCount(2)
        scanningregion.setColumnCount(2)

        #set the corners start and end colour
        scanningregion.setStyleSheet("background-color: white")
        scanningregion.setItem(0, 1, QtWidgets.QTableWidgetItem())
        scanningregion.setItem(1, 0, QtWidgets.QTableWidgetItem())
        scanningregion.item(1, 0).setBackground(QtGui.QColor(0,255,0))
        scanningregion.item(0, 1).setBackground(QtGui.QColor(255,0,0))
        
        #make main layout
        gridlayout = QtWidgets.QGridLayout()

        #add to the main layout
        gridlayout.addLayout(bracketHLayout0,0,0)
        gridlayout.addLayout(bracketHLayout1,1,0)
        gridlayout.addLayout(bracketHLayout2,2,0)
        gridlayout.addWidget(scanningregion,1,1)
        gridlayout.addLayout(columnlayout,0,2)
        gridlayout.addLayout(rowlayout,1,2)
        gridlayout.addLayout(cubelayout,2,2)

        #put into groupbox
        groupbox = QtWidgets.QGroupBox("scanning Region")
        groupbox.setLayout(gridlayout)
        return(groupbox)

    def Overlap(self):
        """sublayout Positional_increments"""   
        OL_min = [float(i) for i in self.read.getConstant(["MinoverlapAzi","MinoverlapAlt"])]
        bracketHLayout1 = bracketInput("Cube Overlap ratio (Azi,Alt): ", "Azimuth Overlap Ratio", "Altitude Overlap Ratio", buttontitle = False,
                                       width = 100,  minlim1 = OL_min[0], maxlim1 = 1, minlim2 = OL_min[1], maxlim2 = 1, enabled = False)
        groupbox = QtWidgets.QGroupBox("Overlap")
        groupbox.setLayout(bracketHLayout1)
        return(groupbox) 

    def filenameandloc(self):
        """sublayout Positional_increments""" 
        #main layout
        VLayout = QtWidgets.QVBoxLayout()
        #filename
        VLayout.addLayout(labelledInput("File Names: ", "base of the file name"))
        #folder name and find a folder location button
        Hlayout = QtWidgets.QHBoxLayout()
        Hlayout.addLayout(labelledInput("Save Location: ", "Where the outcoming images will be saved"))
        folderlocation_button = QtWidgets.QPushButton(u"\U0001F4C1")
        folderlocation_button.setToolTip("Grab folder to save")
        folderlocation_button.setStyleSheet("font-size: 18pt;")
        Hlayout.addWidget(folderlocation_button)
        #add to layout
        VLayout.addLayout(Hlayout)
        #put into groupbox
        groupbox = QtWidgets.QGroupBox("File Details")
        groupbox.setLayout(VLayout)
        return(groupbox)
    
    def CrashSection(self):
        """sublayout Positional_increments"""   
        #main layout
        HLayout = QtWidgets.QHBoxLayout()
        input = labelledInput("Failed Cube #: ", "Which cube the routine failed on")
        checkbox = QtWidgets.QCheckBox("Recovery?")
        HLayout.addLayout(input)
        HLayout.addWidget(checkbox)
        #put into groupbox
        groupbox = QtWidgets.QGroupBox("Recovery Routine")
        groupbox.setLayout(HLayout)
        return(groupbox)

    def Buttons(self):
        """Build the buttons needed for the advanced options. if button already has function then put func# = False"""
        #the back button which closes the current window, in this case the advanced options window
        #back
        button1 = QtWidgets.QPushButton("Back")
        button1.clicked.connect(lambda: self.hide())
        #save
        button2 = QtWidgets.QPushButton("Save")
        #run
        button3 = QtWidgets.QPushButton("Run")
        button3.setStyleSheet("background-color: green")
        return(button1,button2,button3)