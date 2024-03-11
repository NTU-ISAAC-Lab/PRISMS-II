"""
NAME: a_CameraGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 17/11/2022 
DATE LAST UPDATED: 11/07/2023

PURPOSE:
To create the buttons Camera GUI, with format shown below:
 __Camera_______________________
|Image Options | |Toggles |     |
|Play/Pause|   | | |ROI   |     |      
|SAVE_IMAGE|   | | |1:1   |     |      
|SAVE_CUBE|    | |              |
|-------------------------------|                  
|  DISPLAY  FRAME               |          

NOTE:
https://stackoverflow.com/questions/76618105/pyqt-pyqtgraph-window-resize-causes-colormap-to-reset-to-grayscale

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    #10/10/2023: strip back the labels for the saturation and the contrast metrics as currently not essential
    #07/11/2023: add in the graphic user interface and have seprate from camera threading
"""
from PyQt5 import QtWidgets,  QtCore
from qtwidgets import Toggle
import pyqtgraph as pg

class CameraGUI_class():
    """Build the GUI for the camera settings, conatating controls for Focus and Exposure"""
    def __init__(self, sw, read):
        self.sw = sw
        #get the input values
        imgshape = read.getConstant(["ImageW","ImageH"])
        self.x0, self.x1, self.y0, self.y1 = int(0), int(imgshape[0]), int(0), int(imgshape[1])
        self.MaingroupBox = self.BuildMainLayout()

    def BuildMainLayout(self):
        """Build the main camera GUI layout"""
        MaingroupBox = QtWidgets.QGroupBox("Camera")
        #MaingroupBox.setMinimumSize(600, 600)
        VLayout = QtWidgets.QVBoxLayout() 
        MaingroupBox.setLayout(VLayout)
        #initiate the sub groups
        savelablayout = self.BuildsavlabLayout()
        dFramewidget = self.intialiseplotwidget()
        #set subgroups into the maingroup
        VLayout.addLayout(savelablayout, 1)
        VLayout.addWidget(dFramewidget, 20)
        VLayout.addWidget(QtWidgets.QLabel(u"\u2316 0, 0px; 0"), 1)
        #switch out for placeholder if rgb and main not connected
        stackedgroup = self.sw.stackplaceholderWidget(MaingroupBox)
        return(stackedgroup)
    
    def intialiseplotwidget(self):
        """Initalises the widget that the camera will be appended to"""
        #initalise main widget
        self.glw = pg.GraphicsLayoutWidget()#size=(2048,2048))
        #set the cursor settings
        cursor = QtCore.Qt.CrossCursor
        self.glw.setCursor(cursor)
        # add the plot and hide the plotting access
        self.plot = self.glw.addPlot()
        self.plot.setAspectLocked(lock=True, ratio=1)
        self.plot.hideAxis('bottom') 
        self.plot.hideAxis('left')
        #stops zooming out too far from the plot
        self.plot.getViewBox().setLimits(xMin=-self.x1/2, xMax=self.x1*1.5, yMin=-self.y1/2, yMax=self.y1*1.5)
        self.plot.getViewBox().setAspectLocked(lock=True, ratio=1) 
        self.plot.getViewBox().setBackgroundColor("#d7801a")
        #flip the axis
        self.plot.invertY(True) #Y axis by default is flipped
        self.plot.invertX(True) #X axis by default is flipped
        #set the range
        self.plot.setXRange(self.x0, self.x1, padding=0)
        self.plot.setYRange(self.y0, self.y1, padding=0)
        #self.plot.getViewBox().setAspectLocked(lock=True, ratio=1)
        ###Create the image item and add it to the plot###
        self.image = pg.ImageItem()
        self.plot.addItem(self.image)
        return(self.glw)
        
    def BuildsavlabLayout(self):
        """Build the buttons stored at the top of the widget:
        Image Options | Toggles |_Image_Statistics """
        #call in widgets
        imagebuttons = self.BuildimagebuttonLayout()
        toggles = self.BuildtoggleLayout()
        # Horizontal orientation, as shown in the diagram
        HLayout = QtWidgets.QHBoxLayout()
        #add the horizontal widgets |  save  |  label #  | 
        HLayout.addWidget(imagebuttons)
        HLayout.addWidget(toggles)
        #add alignment within layout
        return(HLayout)
    
    def BuildimagebuttonLayout(self):
        """Build the camera controlls buttons
        |Stream Options_|              
        ||Play/Pause|   |
        |SAVE_IMAGE|    |
        |SAVE_CUBE|     |
        |Plot Information||
        |---------------|"""
        #call in widgets
        saveButton,savecubeButton,plapaStack, plotbutton = self.Buttons()
        #make groupbox for widgets to sit in
        SubgroupBox = QtWidgets.QGroupBox("Stream Options")
        # Horizontal orientation, as shown in the diagram
        VLayout = QtWidgets.QVBoxLayout()
        #add the buttons to the vertical layout
        VLayout.addWidget(plapaStack)
        VLayout.addWidget(saveButton)
        VLayout.addWidget(savecubeButton)
        VLayout.addWidget(plotbutton)
        SubgroupBox.setLayout(VLayout)
        return(SubgroupBox)
    
    def BuildtoggleLayout(self):
        """Build the bottom region of the Camera GUI where the checkboxes can be toggled:
        |__Toggles_______|                  
        ||___| ROI       |
        ||___| 1:1       |
        |----------------|
        """
        #call in widgets
        ROIToggle,D1Toggle, FCToggle = self.toggles() #,RGBToggle, satToggle
        #define some labels to have alongside 
        ROIlab, D1lab, FClab =  QtWidgets.QLabel("ROI"), QtWidgets.QLabel("1:1"), QtWidgets.QLabel("False Colour")
        ROIlab.setStyleSheet("font-size: 12pt;"); D1lab.setStyleSheet("font-size: 12pt;"); FClab.setStyleSheet("font-size: 12pt;")
        #make groupbox for widgets to sit in
        SubgroupBox = QtWidgets.QGroupBox("Toggles")
        # Horizontal orientation, as shown in the diagram
        gridlayout = QtWidgets.QGridLayout()
        H1Layout, H2Layout, H3Layout = QtWidgets.QHBoxLayout(), QtWidgets.QHBoxLayout(), QtWidgets.QHBoxLayout()
        #add the buttons to the vertical layout
        H1Layout.addWidget(ROIToggle); H1Layout.addWidget(ROIlab)
        H2Layout.addWidget(D1Toggle); H2Layout.addWidget(D1lab)
        H3Layout.addWidget(FCToggle); H3Layout.addWidget(FClab)
        gridlayout.addLayout(H1Layout, 0,0); gridlayout.addLayout(H2Layout,1,0); gridlayout.addLayout(H3Layout,0,1)
        #add vertical layouts
        SubgroupBox.setLayout(gridlayout)
        #switch out for placeholder if rgb and main not connected
        stackedgroup = self.sw.stackplaceholderWidget(SubgroupBox)
        return(stackedgroup)

    def toggles(self):
        """The toggles for the camera GUI"""
        #ROI: Region of interest, shows a rectangular area that the focus is calculated from
        ROIToggle = Toggle()	
        ROIToggle.setToolTip("Show ROI on main camera")
        #Display 1:1: shows just the ROI area as the full camera widget area
        D1Toggle = Toggle()
        D1Toggle.setToolTip("Show just ROI as 1:1 display")
        #RGB: switches to false colour
        FCToggle = Toggle("False Colour")
        FCToggle.setToolTip("Show image in flase colour to better pick features")
        #update the layout direction of the toggles so the label lies to the right of the checkbox
        ROIToggle.setLayoutDirection(QtCore.Qt.LeftToRight)
        D1Toggle.setLayoutDirection(QtCore.Qt.LeftToRight)
        #resize toggles
        FCToggle.setFixedSize(QtCore.QSize(75, 50))
        ROIToggle.setFixedSize(QtCore.QSize(75, 50))
        D1Toggle.setFixedSize(QtCore.QSize(75, 50))
        return(ROIToggle,D1Toggle, FCToggle)
    
    def Buttons(self):
        """Define the buttons used for the whole camera GUI, of which there is only 'save image' and 'set'"""
        #save button
        plotButton = QtWidgets.QPushButton(u"Plot Information \U0001F4C8")
        plotButton.setToolTip("Plot histogram or focus contrast of image")
        plotButton.setStyleSheet("QPushButton{font-size: 10pt;}")
        #save button
        saveButton = QtWidgets.QPushButton("Save Snapshot ■")
        saveButton.setToolTip("Saves current screen as .TIF, with .DAT")
        saveButton.setStyleSheet("QPushButton{font-size: 10pt;}")
        #save button
        savecubeButton = QtWidgets.QPushButton("Save Image Cube ❏" )
        savecubeButton.setToolTip("Saves current screen as .TIF, with .DAT")
        savecubeButton.setStyleSheet("QPushButton{font-size: 10pt;}")
        #pause/play button
        playButton = QtWidgets.QPushButton(u"Start \u23F5")
        playButton.setStyleSheet("QPushButton{ color: rgb(0, 255, 0);font-size: 10pt;}")
        playButton.setToolTip("Continue camera stream")
        pauseButton = QtWidgets.QPushButton(u"Stop \u25A0")
        pauseButton.setStyleSheet("QPushButton{ color: rgb(255, 0, 0);font-size: 10pt;}")
        pauseButton.setToolTip("Pause camera stream") 
        #make set size
        plapaStack = self.sw.stackWidget(playButton)
        plapaStack.addWidget(pauseButton)
        plapaStack.setCurrentIndex(1)
        return(saveButton,savecubeButton,plapaStack, plotButton)