
"""
NAME: scrollablepopupMessage.py
AUTHOR: John Archibald Page
DATE CREATED: 24/07/2023
DATE LAST UPDATED: 24/07/2023

PURPOSE:
    popupmessage_class -> To show a pop up message, with exit buttons.
    ________________________
    |@|Title______________|X| 
    |Pop up title           |             
    ||---------------------|| 
    ||Pop up message scroll||                                
    |_______________________|                
    |____________________|OK|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets, QtCore, QtGui
from GUI.SelfDefinedWidgets.TextEdit_AutoverticleExpansion import GrowingTextEdit

class scrollPopup_Widget(QtWidgets.QWidget):
    """This is a pop-up class with an expanding message area, perfect for showing the log"""
    def __init__(self,title,messagetitle, message,backoveride=False):
       super(scrollPopup_Widget,self).__init__()
       self.buildpopup(title,messagetitle, message,backoveride)
       self.setWindowIcon(QtGui.QIcon('GUI/Images/Logo.png'))
       self.resize(500, 500)
     
    def buildpopup(self,title,messagetitle, message, backoveride=False):
        """Build the layout of the pop up"""
        #call in widgets to build layout
        label, textbox = self.DefinePopup(title,messagetitle, message)
        button1 = self.Buttons(backoveride) 
        #define layouts
        VLayout = QtWidgets.QVBoxLayout()
        HLayout = QtWidgets.QHBoxLayout()#buttons
        #build button layout
        HLayout.addWidget(button1, QtCore.Qt.AlignRight )
        #build overall layout
        VLayout.addWidget(label)
        VLayout.addWidget(textbox)
        VLayout.addLayout(HLayout)
        #put layout to ,main widget
        self.setLayout(VLayout)
 
    def DefinePopup(self,title,messagetitle, message):
        """Define what the message is and what the icon is, and what the width is in characters of the set style font."""   
        self.setWindowTitle(title) # title of window
        label = QtWidgets.QLabel(messagetitle)
        textbox = self.scrollableArea(message)
        return(label, textbox)

    def Buttons(self, backoveride = False):
        """Build the buttons needed for the advanced options. if button already has function then put func# = False"""
        #the back button which closes the current window, in this case the advanced options window
        button1=QtWidgets.QPushButton("OK")
        if backoveride == True:
            func1 = lambda: exit()
        else:
            func1 = lambda: self.hide()
        button1.clicked.connect(func1)
        return(button1)
    
    def scrollableArea(self, message):
        """Create a scrollable area that automatically grows to show the current log"""
        textbox = GrowingTextEdit()
        textbox.setMinimumHeight(50)
        #settextboxproperties
        textbox.setTextInteractionFlags(QtCore.Qt.NoTextInteraction) 
        #verticle scroll area and scroll area widget---
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(textbox)
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # switch off horizontal scroll
        vbar = scrollArea.verticalScrollBar()
        vbar.setValue(vbar.maximum()) #start at maximum verticle area
        #add the message
        textbox.setText(message)
        return(scrollArea)