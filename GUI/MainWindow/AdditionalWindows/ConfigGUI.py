
"""
NAME: ConfigGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 25/11/2022 
DATE LAST UPDATED: 24/11/2023

ConfigCreate_class -> interactive GUI to create a file to run a Scan, or open file into this folder
 ______________________________________________
|@|Create Config                            |X| 
|---------------------------------------------|            
| _Constants____________________ _____________|              
|| |Main Camera|  |save paths|  ||Switch   |  |  
||             |Filter|         ||in widget|  |     etc.
||______________________________||_________|  |                
|Back|                            |SAVE|APPLY||

when button is clicked there will be a widget switched in the the right side
 with options for changing the values

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets,QtGui
from GUI.SelfDefinedWidgets.InputLayouts import labelledInput

class ConfigCreate_class(QtWidgets.QWidget):
    """This is a pop-up class which creates a csv. config file that can be ran or saved"""
    def __init__(self):
       super(ConfigCreate_class,self).__init__()
       self.buildpopup()
       self.setWindowTitle("Create Config file") # title of window
       self.setWindowIcon(QtGui.QIcon('GUI/Images/Logo.png'))

    def buildpopup(self):
        """Build the layout of the pop up"""
        self.stack = self.formfuncstack()
        #call in widgets to build layout
        mainbuttonlayout = self.mainButtonsGrouping()
        bottomButtonslayout = self.bottomButtonsGroupings()
        #define layouts
        VLayout = QtWidgets.QVBoxLayout()
        self.HLayout = QtWidgets.QHBoxLayout()#buttons
        #build button layout
        self.HLayout.addLayout(mainbuttonlayout)
        self.HLayout.addWidget(self.stack)
        #build overall layout
        VLayout.addLayout(self.HLayout)
        VLayout.addLayout(bottomButtonslayout)
        #put layout to ,main widget
        self.setLayout(VLayout)
 
    def mainButtonsGrouping(self):
        """Buttons stored on the left hand side that lead to the form options"""
        mainCamera,Filter,Focuser,cStand,lStand,Scanningip, scanningwcsaf,Autofocus,Autoexposure = self.mainButtons() #,savePath
        V1Layout = QtWidgets.QVBoxLayout()
        #1)equipment buttons group
        groupbox1 = QtWidgets.QGroupBox("Equipment")
        G1Layout = QtWidgets.QGridLayout()
        G1Layout.addWidget(mainCamera,0,0)
        G1Layout.addWidget(Filter,0,1)
        G1Layout.addWidget(Focuser,0,2)
        G1Layout.addWidget(cStand,1,0)
        G1Layout.addWidget(lStand,1,1)
        groupbox1.setLayout(G1Layout)
        #2)routienes
        V2Layout = QtWidgets.QVBoxLayout()
        groupbox2 = QtWidgets.QGroupBox("Routines")
        G2Layout = QtWidgets.QGridLayout()#row 1
        #scanning routine sub-grouping
        groupbox3 = QtWidgets.QGroupBox("Scanning")
        G3Layout = QtWidgets.QGridLayout()#row 1
        G3Layout.addWidget(Scanningip,0,0)
        G3Layout.addWidget(scanningwcsaf,0,1)
        groupbox3.setLayout(G3Layout)
        #rest of routines
        G2Layout.addWidget(Autofocus,0,0)
        G2Layout.addWidget(Autoexposure,0,1)
        V2Layout.addWidget(groupbox3)
        V2Layout.addLayout(G2Layout)
        groupbox2.setLayout(V2Layout)
        #put into one layotu
        V1Layout.addWidget(groupbox1)
        V1Layout.addWidget(groupbox2)
        return(V1Layout)

    def mainButtons(self):
        """The buttons that when clicked opens up the stacked input options"""
        #equipment
        mainCamera = QtWidgets.QPushButton("Main Camera")
        mainCamera.clicked.connect(lambda: self.switchstack(0))
        Filter = QtWidgets.QPushButton("Filter")
        Filter.clicked.connect(lambda: self.switchstack(1))  
        Focuser = QtWidgets.QPushButton("Focuser")
        Focuser.clicked.connect(lambda: self.switchstack(2))
        cStand = QtWidgets.QPushButton("Camera Mount")
        cStand.clicked.connect(lambda: self.switchstack(3)) 
        lStand = QtWidgets.QPushButton("Light Mount")
        lStand.clicked.connect(lambda: self.switchstack(4))    
        #Routine
        Scanningip = QtWidgets.QPushButton("Initial Parameters")
        Scanningip.clicked.connect(lambda: self.switchstack(5))  
        Scanningwcsaf = QtWidgets.QPushButton("Focusing Subroutine")
        Scanningwcsaf.clicked.connect(lambda: self.switchstack(6))  
        Autofocus = QtWidgets.QPushButton("Autofocusing")
        Autofocus.clicked.connect(lambda: self.switchstack(7))
        Autoexposure = QtWidgets.QPushButton("Autoexposure")
        Autoexposure.clicked.connect(lambda: self.switchstack(8))
        return(mainCamera,Filter,Focuser,cStand,lStand,Scanningip,Scanningwcsaf,Autofocus,Autoexposure)

    def bottomButtonsGroupings(self):
        """Layout formatting for the "back","save" and "apply" buttons"""
        button1,button3 = self.bottomButtons()
        HLayout = QtWidgets.QHBoxLayout()
        HLayout.addWidget(button1)
        HLayout.addWidget(button3)
        return(HLayout)

    def bottomButtons(self):
        """Build the "back","save and apply" buttons"""
        button1 = QtWidgets.QPushButton("Back")
        button1.clicked.connect(lambda: self.hide())
        button3 = QtWidgets.QPushButton("Save and Apply")
        button3.setStyleSheet("background-color: green")
        return(button1,button3)

    def formfunc(self,title,labellist):
        """sublayout for confoig with a form filling format"""   
        VLayout = QtWidgets.QVBoxLayout()
        label_elipse_list = [i+ ": " for i in labellist]
        for i in range(len(labellist)):
            VLayout.addLayout(labelledInput(label_elipse_list[i], labellist[i],  minlim = False, maxlim = False))
        #put into groupbox
        groupbox = QtWidgets.QGroupBox(title)
        groupbox.setLayout(VLayout)
        return(groupbox)

    def formfuncstack(self):
        """Make the stack widget of all the forms"""
        #stacked widget
        self.stackwidget = QtWidgets.QStackedWidget()
        #groupboxes to stack
        self.stackwidget.addWidget(self.formfunc("Main Camera",["Framerate (Frame/s)", "Image Width (px)", "Image Height (px)", "ROI Width (px)", "ROI Height (px)", "Rolling Shutter time (ms)", "Number of image updates after wait", "Update wait time scaler"]))
        self.stackwidget.addWidget(self.formfunc("Filter",["Standard Filter","Minimum Filter Move time (ms)","Maximum Filter Move time (ms)"]))
        self.stackwidget.addWidget(self.formfunc("Focuser",["Max Steps", "Max Speed (steps/s)", "Focus vs Distance Offset"])) 
        self.stackwidget.addWidget(self.formfunc("Camera Alt-Azmiuth Mount",[ u"Min Azi (\N{DEGREE SIGN})",u"Max Azi (\N{DEGREE SIGN})",u"Min Alt (\N{DEGREE SIGN})",u"Max Alt (\N{DEGREE SIGN})", u"Speed (\N{DEGREE SIGN}/s)"])) 
        self.stackwidget.addWidget(self.formfunc("Light Alt-Azmiuth Mount",[u"Azi offset (\N{DEGREE SIGN})", u"Alt offset (\N{DEGREE SIGN})", u"Min Azi (\N{DEGREE SIGN})",u"Max Azi (\N{DEGREE SIGN})",u"Min Alt (\N{DEGREE SIGN})",u"Max Alt (\N{DEGREE SIGN})", u"Speed (\N{DEGREE SIGN}/s)", "Camera to Light Distance (m)", "Azi angle ratio (\N{DEGREE SIGN})", "Azi step ratio", "Alt angle ratio (\N{DEGREE SIGN})", "Alt step ratio", "Focuser vs Distance File Location"])) 
        self.stackwidget.addWidget(self.formfunc("Initial Parameters",["Sensor Width (mm)","Sensor Height (mm)", "Distance from Sensor to Focuser at 0 steps (m)", "Focuser range distance moved (m)", "Focusing Exposure (ms)","Minimum overlap Ratio Azi","Minimum overlap Ratio Alt"])) 
        self.stackwidget.addWidget(self.formfunc("Worst-Case Scenario Autofocus Parameters",["Steps Searching Range", "Searching Speed (steps/s)", "Drop Ratio", "Flat Noise Ratio", "Peak Magnitude Neighbour check"])) 
        self.stackwidget.addWidget(self.formfunc("Optimum Autofocus Parameters",["Steps Searching Range", "Searching Speed (steps/s)", "Drop Ratio", "Flat Noise Ratio", "Peak Magnitude Neighbour check"])) 
        self.stackwidget.addWidget(self.formfunc("AutoExposure Routine",["Exposure Limit (ms)","Standard Filter Starting Exposure (ms)", "White Standard File Location", "Effective Saturation Count (bit depth)", "Effective saturation scaling ratio", "Allowed Percentage of pixels at Saturation", "Allowed Percentage of pixels at Effective Saturation", "Bias Counts (bit depth)", "Scattering surface minimum feature size (px)", "Scattering surface maximum feature size (px)", "Scattering surface Feature limit"])) 
        return(self.stackwidget)

    def switchstack(self,i):
        """switch to given window"""
        self.stackwidget.setCurrentIndex(i)