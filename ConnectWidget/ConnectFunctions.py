"""
NAME: ConnectFunctions.py
AUTHOR: John Archibald Page
DATE CREATED: 28/11/2022 
DATE LAST UPDATED: 28/11/2022

PURPOSE:
    a class of functions used for connecting buttons and threads which will be used multiple times.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from ConnectWidget.Threading.Workers import functionWorker #threading qrunnable class

class ConnectFunctions_class():
    """connect the position buttons for position"""
    def __init__(self, GUI):
        super(ConnectFunctions_class,self).__init__()
        self.GUI = GUI
        self.threadpool = QtCore.QThreadPool()
        #print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

#references
    def Textboxrefences(self, Groupbox):
        """draw the references to the different groups"""
        tblist = Groupbox.findChildren(QtWidgets.QLineEdit)
        return(tblist)
    
    def Sliderrefences(self, Groupbox):
        """draw the references to the different groups"""
        slilist = Groupbox.findChildren(QtWidgets.QSlider)
        return(slilist)
    
    def Dialrefences(self, Groupbox):
        """draw the references to the different groups"""
        dilist = Groupbox.findChildren(QtWidgets.QDial)
        return(dilist)

    def Texteditrefences(self, Groupbox):
        """draw the references to the different groups"""
        telist = Groupbox.findChildren(QtWidgets.QTextEdit)
        return(telist)

    def pushbuttonsrefences(self, Groupbox):
        """draw the references to the different groups"""
        pblist = Groupbox.findChildren(QtWidgets.QPushButton)
        return(pblist)

    def checkboxrefences(self, Groupbox):
        """draw the references to the different groups"""
        cblist = Groupbox.findChildren(QtWidgets.QCheckBox)
        return(cblist)

    def spinboxrefences(self, Groupbox):
        """draw the references to the different groups"""
        sblist = Groupbox.findChildren(QtWidgets.QSpinBox)
        return(sblist)

    def labelrefences(self, Groupbox):
        """draw the references to the different groups"""
        llist = Groupbox.findChildren(QtWidgets.QLabel)
        return(llist)

    def stackedrefences(self, Groupbox):
        """draw the references to the different groups"""
        llist = Groupbox.findChildren(QtWidgets.QStackedWidget)
        return(llist)
    
    def tablerefences(self, Groupbox):
        """draw the references to the different groups"""
        llist = Groupbox.findChildren(QtWidgets.QTableWidget)
        return(llist)
    
    def glwrefences(self, Groupbox):
        """draw the references to the different groups"""
        llist = Groupbox.findChildren(pg.GraphicsLayoutWidget)
        return(llist)
    
    def groupboxrefences(self, Groupbox):
        """draw the references to the different groups"""
        llist = Groupbox.findChildren(QtWidgets.QGroupBox)
        return(llist)
    
    def Tabrefences(self, Groupbox):
        """draw the references to the different groups"""
        llist = Groupbox.findChildren(QtWidgets.QTabWidget)
        return(llist)
    
#interacting with widgets
    def setvaluesofwidget(self,widget,val): #'toggles and line edits, have option for a list
        """Read in the check boxes and spin box values"""
        #check type of widget
        if type(widget) == list or type(widget) == tuple:
            for i in range(len(widget)):
                widgettype = type(widget[i])
                if widgettype == type(QtWidgets.QCheckBox()):
                    widget[i].setChecked(bool(val[i]))
                if widgettype == type(QtWidgets.QSpinBox()):
                    widget[i].setValue(int(val[i]))
                if widgettype == type(QtWidgets.QLineEdit()):
                    widget[i].setText(str(val[i])) 
                else: #'GUI.SelfDefinedWidgets.InputLayouts.textInput'
                    widget[i].setText(str(val[i])) 
        else:
            widgettype = type(widget)
            if widgettype == type(QtWidgets.QCheckBox()):
                widget.setChecked(bool(val))
            if widgettype == type(QtWidgets.QSpinBox()):
                widget.setValue(int(val))
            if widgettype == type(QtWidgets.QLineEdit()):
                widget.setText(str(val))
            else: #'GUI.SelfDefinedWidgets.InputLayouts.textInput'
                widget.setText(str(val)) 

    def readvaluesofwidget(self,widget): #set this for toggles and line edits, have options for a list input
        """Read in the check boxes and spin box values"""
        if type(widget) == list or type(widget) == tuple:
            val = []
            for i in range(len(widget)):
                widgettype = type(widget[i])
                if widgettype == type(QtWidgets.QCheckBox()):
                    val.append(widget[i].isChecked())
                if widgettype == type(QtWidgets.QSpinBox()) or widgettype == type(QtWidgets.QDial()):
                    val.append(widget[i].value())
                if widgettype == type(QtWidgets.QLineEdit()):
                    val.append(widget[i].text())
                else: #'GUI.SelfDefinedWidgets.InputLayouts.textInput'
                    val.append(widget[i].text())
        else:
            widgettype = type(widget)
            if widgettype == type(QtWidgets.QCheckBox()):
                val = widget.isChecked()
            if widgettype == type(QtWidgets.QSpinBox()) or widgettype == type(QtWidgets.QDial()):
                val = widget.value()
            if widgettype == type(QtWidgets.QLineEdit()):
                val = widget.text()
            else: #'GUI.SelfDefinedWidgets.InputLayouts.textInput'
                val = widget.text()
        return(val)

#connecting widgets
    def widgetconnect(self,button,func, clickedF=True, pressedF=False,releasedF=False, returnF=False, valuechangedF = False,textchangedF = False, statechangedF = False, thread = False, freeze = False):
        """Connects button/widget to functionality"""
        if thread == False:
            if clickedF != False:
                button.clicked.connect(func)
            if pressedF != False:
                button.pressed.connect(func)
            if releasedF != False:
                button.released.connect(func)
            if returnF != False:
                button.returnPressed.connect(func)
            if textchangedF != False:
                button.textChanged.connect(func)
            if valuechangedF != False:
                button.valueChanged.connect(func)
            if statechangedF != False:
                button.stateChanged.connect(func)
        else:
            if clickedF != False:
                button.clicked.connect(lambda: self.threadFunc(func, freeze))
            if pressedF != False:
                button.pressed.connect(lambda: self.threadFunc(func, freeze))
            if releasedF != False:
                button.released.connect(lambda: self.threadFunc(func, freeze))
            if returnF != False:
                button.returnPressed.connect(lambda: self.threadFunc(func, freeze))
            if textchangedF != False:
                button.textChanged.connect(lambda: self.threadFunc(func, freeze))
            if valuechangedF != False:
                button.valueChanged.connect(lambda: self.threadFunc(func, freeze))
            if statechangedF != False:
                button.stateChanged.connect(lambda: self.threadFunc(func, freeze))
            
    #connect a function to a thread while running
    def threadFunc(self, fn, freeze):
        """Makes the function passed to it run on a seprate thread, used for routines"""
        # Pass the function to execute
        worker = functionWorker(fn, self.GUI, freeze) # Any other args, kwargs are passed to the run function
        # Execute
        self.threadpool.start(worker)