"""
NAME: popupMessage.py
AUTHOR: John Archibald Page
DATE CREATED: 16/11/2022 
DATE LAST UPDATED: 01/12/2022

PURPOSE:
    popupmessage_class -> To show a pop up message, with exit buttons.
    ________________________
    |@|Title______________|X| 
    |Pop up title           |             
    |Pop up message         |                 
    |_______________________|                
    |____________________|OK|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

class popupmessage_class(QtWidgets.QMessageBox):
    """Show an informative pop up message window. when called, this pop up freezes the main GUI."""
    @QtCore.pyqtSlot(str, str, str, str)
    def __init__(self, title,messagetitle, message, color):
       super(popupmessage_class,self).__init__()
       self.DefinePopup(title,messagetitle, message) # set the message, icons and title of the pop up
       self.buttonpopup() #attach ok button
       self.setWindowIcon(QtGui.QIcon('GUI/Images/Logo.png'))
       #set the background colour
       backgroundcolour_dict = {"info": "color: #b1b1b1 ; background-color: #323232", "success":"color: #323232 ; background-color: #66FF00" , "error":"color: #323232 ; background-color: #EF0107"}
       self.setStyleSheet(backgroundcolour_dict[color])
       self.exec_()
  
    def DefinePopup(self,title,messagetitle, message, windowicon=False):
        """Define what the message is and what the icon is, and what the width is in characters of the set style font."""   
        self.setWindowTitle(title) # title of window
        ##as QmessageBox does not resize easily, use white space in message title to set box width
        whitespace = len(messagetitle)
        self.setText(messagetitle+" "*whitespace) # title of message
        self.setInformativeText(message) # main message
        # set popup window icon
        if windowicon != False:
            self.setWindowIcon(QtGui.QIcon(windowicon))
        else:
            pass

    def buttonpopup(self):
        """"Add the buttons and their functionality"""
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok) # highlights the button