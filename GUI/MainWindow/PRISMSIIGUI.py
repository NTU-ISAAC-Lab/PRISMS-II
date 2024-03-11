"""
NAME: PRISMSIIGUI.py
AUTHOR: John Archibald Page
DATE CREATED: 18/11/2022 
DATE LAST UPDATED: 01/12/2022

PURPOSE:
To inset the PRISMS II with the grouping files Mock-up images and below.
If certain components are not connected to serial, then the buttons are replaced with blank widgets
________________________
|_____________________|X|  a_Camera
||______________||b____||  b_status
||              || d   ||  c_Position  
||              ||_____||  d_Filter
|| a            ||  c  ||  e_Focus
||              ||     ||  f_Exposure
||              ||_____||  g_AdvancedOptions
||______________|| g   ||
|| f    ||   e  ||_____||
||______||______||STOP  |
|_______________||______|

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
#PYQT modules
from PyQt5 import QtWidgets
import os
#self-made GUI clases
from GUI.MainWindow.a_CameraGUI import CameraGUI_class
from GUI.MainWindow.b_StatusGUI import StatusGUI_class
from GUI.MainWindow.c_PositionGUI import PositionGUI_class
from GUI.MainWindow.d_FilterGUI import FilterGUI_class
from GUI.MainWindow.e_FocuserGUI import FocuserGUI_class
from GUI.MainWindow.f_ExposureGUI import ExposureGUI_class
from GUI.MainWindow.g_AOGUI import AOGUI_class
#mainwindow
from GUI.SelfDefinedWidgets.MainWindow import MainWindow_class
#check what is connected
from GUI.MainWindow.EquipmentEnabledCheck import EquipmentEnabledCheck_class as EEC
#selfdiefined classes
from GUI.SelfDefinedWidgets.StackedWidget import StackedWidget_class

class PRISMSIIGUI_class():
    """Build the GUI for PRISMSII"""
    def __init__(self, read):
        #super(PRISMSIIGUI_class,self).__init__()
        self.sw, self.read = StackedWidget_class(), read
        #OS Options
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"  
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        self.cWidget = self.BuildLayout()
        # Frame Customisation
        self.FrameShape = QtWidgets.QFrame.Box
        self.FrameShadow = QtWidgets.QFrame.Raised
        self.MainWindow = MainWindow_class(0.5,0.9)
        #set central widget and the layout to this
        self.MainWindow.setCentralWidget(self.cWidget) 
        
    def BuildLayout(self):
        """Build the layout of PRISMS II Main Window"""
        ##call in components
        #components that alway exist
        self.Status = StatusGUI_class()
        self.AO = AOGUI_class()
        self.STOP = self.StopButton()
        #components that need to be enabled
        self.Camera = CameraGUI_class(self.sw, self.read) 
        self.Position = PositionGUI_class(self.sw, self.read)
        self.Filter = FilterGUI_class(self.sw, self.read)
        self.Focus = FocuserGUI_class(self.sw, self.read)
        self.Exposure = ExposureGUI_class(self.sw)  
        ##Check what has been connected in the config file##
        self.EnabCheck = EEC(self.Position.MaingroupBox,self.Filter.MaingroupBox,self.Camera.MaingroupBox,self.Focus.MaingroupBox,self.Exposure.MaingroupBox)
        #create a new camera settings group
        self.CameraSettings = QtWidgets.QGroupBox("Camera Settings")
        HLayout_0 = QtWidgets.QHBoxLayout()
        HLayout_0.addWidget(self.Exposure.MaingroupBox)
        HLayout_0.addWidget(self.Focus.MaingroupBox)
        self.CameraSettings.setLayout(HLayout_0)
        
        ##Build up the layout piecewise
        #first column
        VLayout_1 = QtWidgets.QVBoxLayout()
        VLayout_1.addWidget(self.Camera.MaingroupBox,5)
        VLayout_1.addWidget(self.CameraSettings,1)
        
        #second column
        VLayout_2 = QtWidgets.QVBoxLayout()
        VLayout_2.addWidget(self.Status.MaingroupBox,1)
        VLayout_2.addWidget(self.Filter.MaingroupBox,5)
        VLayout_2.addWidget(self.Position.MaingroupBox,4)
        VLayout_2.addWidget(self.AO.MaingroupBox,3)
        VLayout_2.addWidget(self.STOP,2)

        #Horizontal orientation [1] and [2] : [3]
        HLayout_3 = QtWidgets.QHBoxLayout()
        HLayout_3.addLayout(VLayout_1, 5)
        HLayout_3.addLayout(VLayout_2, 6)
        
        ##assign main layout to central widget
        cWidget = QtWidgets.QWidget()
        cWidget.setLayout(HLayout_3)
        return(cWidget)

    def StopButton(self):
        """Define the emergency stop button"""
        #go/stop button
        goButton = QtWidgets.QPushButton(u"Go")
        goButton.setStyleSheet("background-color: green; font-size: 36pt;")
        goButton.setToolTip("Release Equipment")
        stopButton = QtWidgets.QPushButton(u"STOP!")
        stopButton.setStyleSheet("background-color: red; font-size: 36pt;")
        stopButton.setToolTip("Stop equipment in emergency!") 
        #set to one widget
        gostopStack = self.sw.stackWidget(goButton)
        gostopStack.addWidget(stopButton)
        gostopStack.setCurrentIndex(1)
        return(gostopStack)
    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dial = PRISMSIIGUI_class()
    dial.show()
    sys.exit(app.exec_())