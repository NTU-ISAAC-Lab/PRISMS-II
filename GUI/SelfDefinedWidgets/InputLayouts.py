"""
NAME: inputLayouts.py
AUTHOR: John Archibald Page
DATE CREATED: 12/12/2022 
DATE LAST UPDATED: 12/12/2022

PURPOSE:
    input options that are used throughout the GUI

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets, QtGui

class labelledInput(QtWidgets.QHBoxLayout):
    """Labelled input box"""
    def __init__(self, title, tip,  minlim = False, maxlim = False, enabled = True, width = False, colours = False):
        super(labelledInput,self).__init__()
        mainlabel = QtWidgets.QLabel(title)
        #set colours of the labels, useful for the first and last cube labels
        if colours != False:
            mainlabel.setStyleSheet("color: "+colours)
        #the brackets and inputs
        if (minlim != False and maxlim != False):
            input = numberInput(tip, minlim, maxlim, enabled = enabled, width = width)
        else:
            input = textInput(tip, enabled = enabled, width = width)
        #build the format
        self.addWidget(mainlabel)
        self.addWidget(input)
        
class buttonInput(QtWidgets.QHBoxLayout):
    """input box with a return button"""
    def __init__(self, tip, title = u"GO",  minlim = False, maxlim = False, enabled = True, width = False, colours = False):
        super(buttonInput,self).__init__()
        returnbutton = QtWidgets.QPushButton(title)
        #set colours of the labels, useful for the first and last cube labels
        if colours != False:
            returnbutton.setStyleSheet("color: "+colours)
        #the brackets and inputs
        if (minlim != False and maxlim != False):
            input = numberInput(tip, minlim, maxlim, enabled = enabled, width = width)
        else:
            input = textInput(tip, enabled = enabled, width = width)
        #build the format
        self.addWidget(input)
        self.addWidget(returnbutton)
        
class bracketInput(QtWidgets.QHBoxLayout):
    """The format used for positional inputs .i.e. (azi,alt) with a go button"""
    def __init__(self, title, tip1, tip2, tip3 = "Move to position", buttontitle = "GO", width = False, minlim1 = -360, maxlim1 = 360, minlim2 = -360, maxlim2 = 360, enabled = True,  colours = False):
        super(bracketInput,self).__init__()
        if buttontitle != False: # chose to have a button
            returnbutton = QtWidgets. QPushButton(buttontitle)
            returnbutton.setToolTip(tip3)
        if type(title) == str:
            mainlabel = QtWidgets.QLabel(title)
            #set colours of the labels, useful for the first and last cube labels
            if colours != False:
                mainlabel.setStyleSheet("color: "+colours)
        else: # in case a button is used instead
            mainlabel = title
        #the brackets and inputs
        labelbrackets = [QtWidgets.QLabel("("), QtWidgets.QLabel(u"\N{DEGREE SIGN} , "), QtWidgets.QLabel(u"\N{DEGREE SIGN})")]
        input1 = numberInput(tip1,  minlim1, maxlim1, enabled = enabled, width = width)
        input2 = numberInput(tip2,  minlim2, maxlim2, enabled = enabled, width = width)
        #build the brackets format
        self.addWidget(mainlabel)
        self.addWidget(labelbrackets[0])
        self.addWidget(input1)
        self.addWidget(labelbrackets[1]) 
        self.addWidget(input2)
        self.addWidget(labelbrackets[2]) 
        if buttontitle != False: # chose to have a button
            self.addWidget(returnbutton) 
        
class numberInput(QtWidgets.QLineEdit):
    """input box with number format"""
    def __init__(self, tip,  minlim, maxlim, enabled = True,  width = False):
        super(numberInput,self).__init__()
        #set the validator of the input
        dv = QtGui.QDoubleValidator(minlim, maxlim, 2) # [0, 5] with 2 decimals of precision
        dv.setNotation(QtGui.QDoubleValidator.StandardNotation) # no scientifc notation accepted
        self.setValidator(dv)
        #is the enabled flag is false these lineedits will not be accessible
        self.setEnabled(enabled)
        #make the width a set size
        if width != False:
            self.setFixedWidth(width)
        #set the tip of the input
        self.setToolTip(tip) 
        
class textInput(QtWidgets.QLineEdit):
    """input box with text format"""
    def __init__(self, tip, enabled = True, width = False):
        super(textInput,self).__init__()
        #is the enabled flag is false these lineedits will not be accessible
        self.setEnabled(enabled)
        #make the width a set size
        if width != False:
            self.setFixedWidth(width)
        #set the tip of the input
        self.setToolTip(tip) 