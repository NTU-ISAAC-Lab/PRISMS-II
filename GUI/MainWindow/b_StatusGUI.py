"""
NAME: b_StatusGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 17/11/2022 
DATE LAST UPDATED: 23/11/2022

PURPOSE:
To create the widgets for, and format the layout of, a terminal GUI. 
 __Status_______________
| _______________________|                                                           
||LastMove___________|...| -> pop-up with log list
|------------------------|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets

class StatusGUI_class():
    """Make the GUI for the Terminal"""
    def __init__(self):
        self.MaingroupBox = self.BuildStatus()

    def BuildStatus(self):
        """Build the main layout for th terminal GUI"""
        #initiate buttons
        inputLine = self.StatusTextbox()
        lcButton = self.logpopupButton()
        # vertical orientation, as shown in the diagram
        inputLayout = QtWidgets.QHBoxLayout()
        #add the widgets
        inputLayout.addWidget(inputLine, 8)
        inputLayout.addWidget(lcButton, 1)
        #make Group box
        terminalgroupbox = QtWidgets.QGroupBox("Status")
        terminalgroupbox.setLayout(inputLayout)
        return(terminalgroupbox)
        
    def StatusTextbox(self):
        """input commands to the input line to write to terminal"""
        inputline = QtWidgets.QLineEdit()
        inputline.setStyleSheet("font-size: 10pt;")
        inputline.setReadOnly(True)
        return(inputline)

    def logpopupButton(self):
        """opens a message pop-up of the list of available commands"""
        lcbutton = QtWidgets.QPushButton("...")
        lcbutton.setToolTip('Operation Log...')
        return(lcbutton)