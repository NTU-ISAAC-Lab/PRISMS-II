
"""
NAME: StackedWidget.py
AUTHOR: John Archibald Page
DATE CREATED: 05/12/2022 
DATE LAST UPDATED: 05/12/2022

PURPOSE:
    To set a widget to be stacked, used for enabling and disabling widgets
    
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets

class StackedWidget_class():
    """Set widget to be stacked"""
    def __init__(self):
        super(StackedWidget_class,self).__init__()

    def PlaceHolder(self,widget):
        """This is a place holder for when the serial for a device is not connected"""
        #create group box with placeholder widget
        vbox = QtWidgets.QVBoxLayout()
        if type(widget)==QtWidgets.QGroupBox: # groupbox
            groupbox = QtWidgets.QGroupBox(widget.title())
            #the placeholder is just a label
            placeholderwidget = QtWidgets.QLabel("SERIAL PORT NOT CONNECTED...")
        else: # Checkbox
            groupbox = QtWidgets.QGroupBox("RGB")
            #the placeholder is just a label
            placeholderwidget = QtWidgets.QLabel()
        groupbox.setLayout(vbox)
        vbox.addWidget(placeholderwidget)
        #set the stylesheet
        placeholderwidget.setStyleSheet("background-color: rgba(143, 143, 143, 0);font-family:Arial, Helvetica, sans-serif;color:white;font: bold 16px;border-style: outset;")
        return(groupbox)

    def stackWidget(self,widget,stacked = False):
        """Make a widget part of a stake with the placeholder, which can be switched in"""
        if stacked == False:
            stackedwidget = QtWidgets.QStackedWidget()
        else:
            stackedwidget = stacked
        stackedwidget.addWidget(widget)
        return(stackedwidget)

    def stackplaceholderWidget(self,widget):
        """Makes new stacked widget to use as a placeholder"""
        stackedwidget = QtWidgets.QStackedWidget()
        stackedwidget.addWidget(widget)
        stackedwidget.addWidget(self.PlaceHolder(widget))
        return(stackedwidget)