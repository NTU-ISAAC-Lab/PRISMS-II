
"""
NAME: caputureCubeGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 26/06/2023 
DATE LAST UPDATED: 11/10/2023 

captureCube_class -> sets the exposure settings for capturing an image cube
________________________________
|@|Capture Cube             |X| |
|-------------------------------|            
|_Exposure_time________________ |  
| |autoexposure|  |setexposure| |
||fil: 1 2 3 4 5 6 7 8 9 10    ||  
||exp | | | | | | | | | | | |o|||
|_File_Name_&_Save_Location____ |  
||file name:     |         |   ||  
||Save location: |         ||o|||  
|------------------------------||                
|Back|                 |CAPTURE||
--------------------------------
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets, QtGui
from GUI.SelfDefinedWidgets.InputLayouts import  numberInput, labelledInput

class captureCube_class(QtWidgets.QWidget):
    """This is a pop-up class which creates a csv. Scan file that can be ran or saved"""
    def __init__(self):
       super(captureCube_class,self).__init__()
       self.buildpopup()
       self.setWindowTitle("Capture image cube") # title of window
       self.setWindowIcon(QtGui.QIcon('GUI/Images/Logo.png'))
       
    def buildpopup(self):
        """Build the layout of the pop up"""
        #call in widgets to build layout
        etgroupbox = self.Exposuretime()
        flgroupbox = self.filenameandloc() 
        button1, button2= self.Buttons()
        #define layouts
        VLayout = QtWidgets.QVBoxLayout()
        HLayout = QtWidgets.QHBoxLayout()
        #build button layout
        HLayout.addWidget(button1)
        HLayout.addWidget(button2)
        #build overall layout
        VLayout.addWidget(etgroupbox)
        VLayout.addWidget(flgroupbox)
        VLayout.addLayout(HLayout)
        #put layout to ,main widget
        self.setLayout(VLayout)
 
    def Exposuretime(self):
        """sublayout exposure time with options of auto exposure, scalled to channel 5 or mnually set each channel"""   
        #buttons auto-exposure, ratio, all-set
        aebutton,indbutton = QtWidgets.QPushButton("Auto-Exposure"), QtWidgets.QPushButton("Set Exposure")
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

    def Buttons(self):
        """Build the buttons needed for the advanced options. if button already has function then put func# = False"""
        #the back button which closes the current window, in this case the advanced options window
        #back
        button1 = QtWidgets.QPushButton("Back")
        button1.clicked.connect(lambda: self.hide())
        #run
        button2 = QtWidgets.QPushButton("Capture")
        button2.setStyleSheet("background-color: green")
        return(button1,button2)