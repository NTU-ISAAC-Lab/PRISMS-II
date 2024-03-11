"""
NAME: f_Exposure.py
AUTHOR: John Archibald Page
DATE CREATED: 25/11/2022 
DATE LAST UPDATED: 03/11/2023

PURPOSE:
    GUI for adjusting the exposure:
    _Exposure__________
    |     | u |       |
    | ___  ___  ___   |
    || AE||___||___|  |
    |     | d |       |
    |_________________|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets
from GUI.SelfDefinedWidgets.InputLayouts import numberInput
from GUI.SelfDefinedWidgets.InputLayouts import buttonInput

class ExposureGUI_class():
    """Build the GUI for the camera settings, contating controls for Focus and Exposure"""
    def __init__(self, sw):
        super(ExposureGUI_class,self).__init__()
        self.MaingroupBox = self.BuildMainLayout(sw)
        
    def BuildMainLayout(self, sw):
        """ Create a sublayout of the Focus and exposure interfaces"""
        upButton, downButton, AutoButton = self.Buttons()
        Value = buttonInput("current Exposure",  minlim = 0, maxlim =1000, width = 100)
        step = numberInput("+/- steps",  0, 1000, width = 50)
        #make groupbox for widgets to sit in
        SubgroupBox = QtWidgets.QGroupBox("Exposure (ms)")
        glayout = QtWidgets.QGridLayout() 
        glayout.addWidget(AutoButton,0,0)
        glayout.addLayout(Value,0,1)
        glayout.addWidget(step,1,1)
        glayout.addWidget(downButton,1,0)
        glayout.addWidget(upButton,1,2)
        SubgroupBox.setLayout(glayout)
        stackedgroup = sw.stackplaceholderWidget(SubgroupBox)
        return(stackedgroup)

    def Buttons(self):
        """Define the buttons for the focuser and exposure subgroups"""
        #up button
        upButton = QtWidgets.QPushButton(u"\u25BA")
        upButton.setToolTip("Increase exposure")
        #down button
        downButton = QtWidgets.QPushButton(u"\u25C4")
        downButton.setToolTip("Decrease Exposure")
        #auto button
        autoButton = QtWidgets.QPushButton("Auto-Exp")
        autoButton.setToolTip("Automatically calculates maximum exposure below a threshold saturation level")
        #widget size
        autoButton.setFixedWidth(100)
        upButton.setFixedWidth(50)
        downButton.setFixedWidth(50)
        return(upButton, downButton, autoButton)