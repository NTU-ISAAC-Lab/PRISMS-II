"""
NAME: d_FilterGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 18/11/2022 
DATE LAST UPDATED: 01/12/2022

PURPOSE:
To create the Filter GUI:
  _Filter__________
 |  |             |
 |     dial       |
 |________________|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    .i.e. #01/12/2022: updated the message used in the pop up
    #24/07/2023: updated the checkbox to a dial to better demonstrate the filter postiontion moving
    #03/11/2023: remove ths info button. add in a display widget instead for the threading to update
"""
from PyQt5 import QtWidgets
from GUI.SelfDefinedWidgets.valueDial import ValueDial

class FilterGUI_class():
    """Build the GUI for the filter wheel setting"""
    def __init__(self, sw, read):
        #initalise classes
        self.standfil = int(read.getConstant(["StandFil"]))
        #build the layout of the widget
        self.MaingroupBox = self.BuildLayout(sw)
    
    def BuildLayout(self, sw):
        """Build the Layout of the filter wheel gui box"""
        #call in widgets
        self.swBox = self.dial()
        #make groupbox for widgets to sit in
        groupBox = QtWidgets.QGroupBox("Filter")
        #layout Buttons
        filterLayout = QtWidgets.QVBoxLayout()
        filterLayout.addWidget(self.swBox, 9)
        #add the layout to the group
        groupBox.setLayout(filterLayout)
        stackedgroup = sw.stackplaceholderWidget(groupBox)
        return(stackedgroup)

    def dial(self):
        """A dial wheel to select the filter"""
        dialwidget = ValueDial(minimum=0, maximum=9)
        dialwidget.setValue(self.standfil) # starts off on fifth lens (4 in python indexing)
        dialwidget.setToolTip("Which filter is selected, 0-9")
        return(dialwidget)