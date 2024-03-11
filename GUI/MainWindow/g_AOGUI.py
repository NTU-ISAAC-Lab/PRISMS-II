"""
NAME: f_AOGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 17/11/2022 
DATE LAST UPDATED: 24/07/2023

PURPOSE:
    To create the buttons for Advance Options GUI:

    _Advance_Options_
    |   |Scan |     |
    |   |Set-Up |     |
    |   |Config.|     |
    |-----------------|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    .i.e. #01/12/2022: updated the message used in the pop up
"""
from PyQt5 import QtWidgets

class AOGUI_class():
    """Build the GUI for the Advance Options controls"""
    def __init__(self):
        super(AOGUI_class,self).__init__()
        self.MaingroupBox = self.BuildLayout()

    def BuildLayout(self):
        """Build the Orientation of PRISMS II widgets group"""
        #call in widgets
        ScanButton,setupButton,configButton=self.Buttons()
        #make groupbox for widgets to sit in
        groupBox = QtWidgets.QGroupBox("Advanced Options")
        #Vertical layout
        Vlayout = QtWidgets.QVBoxLayout()
        Vlayout.addWidget(ScanButton)
        Vlayout.addWidget(setupButton) 
        Vlayout.addWidget(configButton) 
        #add the layout to the group
        groupBox.setLayout(Vlayout)
        return(groupBox)

    def Buttons(self):
        """Define the buttons"""
        #Scan button
        ScanButton = QtWidgets.QPushButton("Scan")
        ScanButton.setToolTip("Create, open, and/or run Scan file")
        #setup button
        setupButton = QtWidgets.QPushButton("Set-Up")
        setupButton.setToolTip("Save current set-up or open previous set-up")
        #config button
        configButton = QtWidgets.QPushButton("Config")
        configButton.setToolTip("Create, open, and/or run Config. file")
        #connect button functionality to clicked and enter button
        return(ScanButton,setupButton,configButton)