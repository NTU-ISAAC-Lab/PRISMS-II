"""
NAME: histplotGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 22/12/2023
DATE LAST UPDATED: 22/12/2023
 
interactive GUI plotting the image information:
    >histogram of the pixel values for exposure
    >Focus vs contrast
   
#https://www.tutorialspoint.com/pyqt/pyqt_qtabwidget.htm -> make tabs
#https://pyqtgraph.readthedocs.io/en/latest/getting_started/plotting.html -> plot data
 
_________________________________________________
|@|Focuser Curve______________________________|X|            
|                                               |
|                                               |
|                                               |
|-----------------------------------------------|                
|| refresh data |  |pause/continue data capture||
||Back|                     |Save data |        |
 
UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
from GUI.SelfDefinedWidgets.StackedWidget import StackedWidget_class
from GUI.SelfDefinedWidgets.InputLayouts import numberInput
 
class histplot_class(QtWidgets.QWidget):
    """This is a pop-up class which creates a csv. Scan file that can be ran or saved"""
    def __init__(self):
       super(histplot_class,self).__init__()
       self.sw = StackedWidget_class()
       self.buildpopup()
       self.setWindowTitle("Pixel Value and Focus Information") # title of window
       self.setWindowIcon(QtGui.QIcon('GUI/Images/Logo.png'))
       
    def buildpopup(self):
        """Build the layout of the pop up"""
        #create the tabs
        self.createTabs()
        #call in widgets to build layout
        button1, button2, button3, button4 = self.Buttons()
        #define layouts
        VLayout = QtWidgets.QVBoxLayout()
        GLayout = QtWidgets.QGridLayout()
        #build button layout
        GLayout.addWidget(button3,0,0) # refresh
        GLayout.addWidget(button4,0,1) # pause data capture
        GLayout.addWidget(button1,1,0) # back
        GLayout.addWidget(button2,1,1) # Save
        #build overall layout
        VLayout.addWidget(self.tabs) # the plots
        #add in the hist bin number
        HLayout = QtWidgets.QHBoxLayout()
        HLayout.addWidget(QtWidgets.QLabel(u"\u2316 0, 0"))
        HLayout.addWidget(numberInput(f"Histogram Bin #",  0, 2048**2, enabled = True, width = 100))
        VLayout.addLayout(HLayout) # pixel values
        VLayout.addLayout(GLayout) #buttons
        #put layout to ,main widget
        self.setLayout(VLayout)
       
    def createTabs(self):
        """Create a tabbed widget to store the histogram and the focus plots"""
        #create tabs
        self.tabs = QtWidgets.QTabWidget()
        #make the plots
        self.pixelvalue = self.intialiseplotwidget("Pixel Value Histogram",  "Frequency", "Pixel Value")
        self.stepsvsfocus = self.intialiseplotwidget("Current Focus",  "Focus Contrast Unit","Focus Steps")
        #add the widgets to the tabs
        self.tabs.addTab(self.pixelvalue,' Pixel Val Hist')
        self.tabs.addTab(self.stepsvsfocus,'Foc step vs Foc Contrast')
 
    def intialiseplotwidget(self, title, xlab, ylab):
        """Initalises the widget that the camera will be appended to"""
        #initalise main widget
        self.glw = pg.GraphicsLayoutWidget()
        #set the cursor settings
        cursor = QtCore.Qt.CrossCursor
        self.glw.setCursor(cursor)
        #add the plot
        self.plot = self.glw.addPlot()
        self.plot.setLabel('left', text = xlab)
        self.plot.setLabel('bottom', text = ylab)
        self.plot.setTitle(title = title)
        return(self.glw)
 
    def Buttons(self):
        """Build the buttons needed for the advanced options. if button already has function then put func# = False"""
        #back
        button1 = QtWidgets.QPushButton("Back")
        button1.setFixedWidth(350)
        button1.clicked.connect(lambda: self.hide())

        #Save data
        button2 = QtWidgets.QPushButton(u"Save")
        button2.setFixedWidth(350)
        button2.setToolTip("Save a plot and data") 

        #refresh data
        button3 = QtWidgets.QPushButton("\u27F3")
        button3.setFixedWidth(350)
        button2.setToolTip("Refresh data") 
        button3.setCheckable(True)

        #pause/play button
        play, pause = QtWidgets.QPushButton(u"Start Capture \u23F5"), QtWidgets.QPushButton(u"Stop Cature\u25A0")
        play.setFixedWidth(350); pause.setFixedWidth(350)
        play.setStyleSheet("color: rgb(0, 255, 0)"); pause.setStyleSheet("color: rgb(255, 0, 0)")
        play.setToolTip("Continue data capture"); pause.setToolTip("Pause data capture") 
        
        #make the buttons switch out in a stack
        button4 = self.sw.stackWidget(play)
        button4.addWidget(pause)
        button4.setCurrentIndex(1)
        return(button1, button2, button3, button4)