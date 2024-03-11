"""
NAME: c_PositionGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 17/11/2022 
DATE LAST UPDATED: 01/12/2022

PURPOSE:
To create the buttons for position GUI, with mock up shown in Mock-up.PNG.
    _Position: (xx,xx)________________
    |             Altitude  Azimuth   |
    |    |(0,0)||______|  |______|>|  | 
    |             | u |               |
    |         ___ ===== ___           |
    |        | < ||___|| > |          |
    |         --- | d | ---           |
    |---------------------------------|
  
UPDATE HISTORY:
"""
from PyQt5 import QtWidgets, QtCore
from GUI.SelfDefinedWidgets.InputLayouts import bracketInput, numberInput

class PositionGUI_class():
    """Build the GUI for the position controls"""
    def __init__(self, sw, read):
        self.MinAzi,self.MaxAzi,self.MinAlt,self.MaxAlt = [float(i) for i in read.getConstant(["MinAzi","MaxAzi","MinAlt","MaxAlt"])]
        self.MaingroupBox = self.BuildLayout(sw)
    
    def BuildLayout(self, sw):
        """Build the Orientation of PRISMS II widgets group"""
        #make groupbox for widgets to sit in
        groupBox = QtWidgets.QGroupBox(u"Position (Azimuth\N{DEGREE SIGN}, Altitude\N{DEGREE SIGN})")

        #layout
        setzeroButton = QtWidgets.QPushButton(u"(0\N{DEGREE SIGN},0\N{DEGREE SIGN})")
        setzeroButton.setToolTip(u"Move to (0\N{DEGREE SIGN},0\N{DEGREE SIGN})")
        azialtLayout = bracketInput(setzeroButton, "Azimuth Position", "Altitude Position", width = False, minlim1 = self.MinAzi, maxlim1 = self.MaxAzi, minlim2 = self.MinAlt, maxlim2 = self.MaxAlt) 
        #main dial button grid layout, set like a 3 x 3 shown below
        glayout = self.buttonLayout()
        
        # combine the grid and Horizontal layouts using a horizontal layout:
        HLayout = QtWidgets.QVBoxLayout()
        HLayout.addLayout(azialtLayout, 3)
        HLayout.addLayout(glayout, 7)
        
        #add the layout to the group
        groupBox.setLayout(HLayout)
        stackedgroup = sw.stackplaceholderWidget(groupBox)
        return(stackedgroup)
    
    def buttonLayout(self):
        """define the layout of the position buttons"""
        #call in widgets
        leftButton,rightButton,upButton,downButton = self.Buttons()
        step = numberInput("+/- steps",  0, 5, width = 50) #hard code max steps as 5, to prevent large bad entry
        step.setText(str(1))#initalise the steps as +/-1
        #make the grid
        glayout = QtWidgets.QGridLayout()
        glayout.addWidget(upButton,0,1) # 2
        glayout.addWidget(leftButton,1,0) # 4
        glayout.addWidget(rightButton,1,2) # 6
        glayout.addWidget(step,1,1,alignment=QtCore.Qt.AlignCenter) # 5
        glayout.addWidget(downButton,2,1) # 5
        return(glayout)
    
    def Buttons(self):
        """Define the buttons of the position GUI"""
       #left button
        leftButton = QtWidgets.QPushButton(u"\u25C4")
        leftButton.setFixedWidth(50)
        leftButton.setToolTip("Rotate anticlockwise")
        #right button
        rightButton = QtWidgets.QPushButton(u"\u25BA")
        rightButton.setFixedWidth(50)
        rightButton.setToolTip("Rotate clockwise")
        #up button
        upButton = QtWidgets.QPushButton(u"\u25B2")
        upButton.setFixedWidth(50)
        upButton.setToolTip("Tilt upwards")
        #down button
        downButton = QtWidgets.QPushButton(u"\u25BC")
        downButton.setFixedWidth(50)
        downButton.setToolTip("Tilt downwards")
        return(leftButton,rightButton,upButton,downButton)