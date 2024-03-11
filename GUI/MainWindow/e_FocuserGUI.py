"""
NAME: e_CameraSettings.py
AUTHOR: John Archibald Page
DATE CREATED: 25/11/2022 
DATE LAST UPDATED: 21/12/2023

PURPOSE:
    Python call in the relevent directories as stated in the savepath folder:
    __Focus: xxx steps____________________ 
    |	|Auto| 	   |_____| > |            |  
    |  |<|           |  |             |>| |
    |_____________________________________|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets
from GUI.SelfDefinedWidgets.InputLayouts import numberInput
from GUI.SelfDefinedWidgets.InputLayouts import buttonInput

class FocuserGUI_class():
    """Build the GUI for the camera settings, contating controls for Focus and Exposure"""
    def __init__(self, sw, read):
        self.maxsteps = int(read.getConstant(["FocMaxSteps"]))
        self.MaingroupBox = self.BuildMainLayout(sw)
        
    def BuildMainLayout(self, sw):
        """ Create a sublayout of the Focus and exposure interfaces:"""
        #call in widgets
        AutoButton,nrButton,frButton = self.Buttons()
        Value = buttonInput("current Focus",  minlim = 0, maxlim =self.maxsteps, width = 100)
        step = numberInput("+/- steps",  0, self.maxsteps, width = 50)
        #make groupbox for widgets to sit in
        SubgroupBox = QtWidgets.QGroupBox("Focus")
        # vertical orientation, as shown in the diagram
        glayout = QtWidgets.QGridLayout()
        #add in the horizontal layout buttons  |_____||>|  |Auto| 
        glayout.addWidget(AutoButton,0,0)
        glayout.addLayout(Value,0,1)
        glayout.addWidget(step,1,1)
        glayout.addWidget(nrButton,1,0)
        glayout.addWidget(frButton,1,2)
        #make the subgroup
        SubgroupBox.setLayout(glayout)
        stackedgroup = sw.stackplaceholderWidget(SubgroupBox)
        return(stackedgroup)

    def Buttons(self):
        """Define the buttons for the focuser and exposure subgroups"""
        #auto button
        autoButton = QtWidgets.QPushButton("Auto-Foc")
        autoButton.setToolTip("Automatically focus for all filters")
        #Nr
        nrButton = QtWidgets.QPushButton(u"\u25C4"+"Nr")
        nrButton.setToolTip("Move focuser back")
        #Fr
        frButton = QtWidgets.QPushButton("Fr"+u"\u25BA")
        frButton.setToolTip("Move focuser forward")
        #set widths
        nrButton.setFixedWidth(50)
        frButton.setFixedWidth(50)
        autoButton.setFixedWidth(100)
        return(autoButton,nrButton,frButton)