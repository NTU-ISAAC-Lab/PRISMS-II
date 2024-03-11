"""
NAME: MainPRISMSII.py
AUTHOR: John Archibald Page
DATE CREATED: 10/10/2022 
DATE LAST UPDATED:01/06/2022

PURPOSE:
    To run the main window for PRISMS II

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from ConnectWidget.MainConnecting import MainConnecting_class 
try:
    #standard libraries and modules
    from PyQt5 import QtWidgets, QtCore, QtGui
    import os
    import sys
    #self made modules
    import Routines.statusLogging.initiateLogging as il
    from GUI.MainWindow.AdditionalWindows.ConnectEquipmentGUI import ConnectEquipmentGUI_class
    from ConnectWidget.advancedOptions.ConnectEquipment import ConnectEquipment_class
    from ConnectWidget.MainConnecting import MainConnecting_class
except:
    from PyQt5.QtWidgets import QApplication , QMessageBox
    msgapp = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error during module import!")
    msg.setInformativeText('Program will close after pressing "OK" ')
    msg.setWindowTitle("ERROR!")
    msg.exec_()
    print("Modules could not be installed correctly, halting code...")

class PRISMSII():
    """Class to launch the PRISMS II GUI"""
    def __init__(self):
        #initalise the log of how the interface has been used
        self.logger = il
        #get the information for the connections
        self.ce = ConnectEquipment_class()
        #state which equipment connected
        self.ceg = ConnectEquipmentGUI_class()
        #launch the main window
        self.Mainconnected = MainConnecting_class()

if __name__ == "__main__":
    #create application
    Application = QtWidgets.QApplication(sys.argv)
    #create splashscreen
    #grab the current thread
    curthread = QtCore.QThread.currentThread()
    # Create splashscreen
    splash_pix = QtGui.QPixmap(os.getcwd()+'//GUI//Images//Logo.png')
    splash = QtWidgets.QSplashScreen(splash_pix,QtCore.Qt.WindowStaysOnTopHint)
    # add fade to splashscreen
    opaqueness, step = 0.0, 0.1
    splash.setWindowOpacity(opaqueness)
    splash.show()
    while opaqueness < 1:
        splash.setWindowOpacity(opaqueness)
        curthread.msleep(int(step*10**3)) # 1.5 factor is a safty buffer for processing time
        opaqueness+=step
    #launch the PRISMS II program
    Window = PRISMSII()
    splash.close()#finish(Window)
    #apply the style sheet
    Application.setStyleSheet(open('PRISMSIIStyle.css').read())
    #launch event
    Application.exec_()