"""
NAME: MainWindow.py
AUTHOR: John Archibald Page
DATE CREATED: 17/11/2022 
DATE LAST UPDATED: 01/12/2022

PURPOSE:
    To create the main window widget that iscales depending on the screen size it is launched on.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import os
from PyQt5 import QtGui, QtWidgets
import screeninfo
import re

class MainWindow_class(QtWidgets.QMainWindow):
    """Create a main window that scales depending on the screen hardware used."""
    def __init__(self,WidthRatio=1,HeightRatio=1,icon=False):
        super(MainWindow_class,self).__init__()
        self.setWindowTitle("PRISMS II")
        self.setAcceptDrops(True)
        self.BuildWindow(WidthRatio,HeightRatio,icon)
        if icon == False:
            self.setWindowIcon(QtGui.QIcon(os.getcwd()+'//GUI//Images//Logo.png'))
        else:
            self.setWindowIcon(QtGui.QIcon(icon))

    def BuildWindow(self,WidthRatio=1,HeightRatio=1,icon=False):
        # get the screen dimensions
        x0 = int(re.search(r'x=(\d+)',str(screeninfo.get_monitors())).group(1))
        y0 = int(re.search(r'y=(\d+)',str(screeninfo.get_monitors())).group(1))
        x1 = int(re.search(r'width=(\d+)',str(screeninfo.get_monitors())).group(1))
        y1 = int(re.search(r'height=(\d+)',str(screeninfo.get_monitors())).group(1))
        # get dimensions to cover % of screen based on width & height ratios
        x0, x1, y0, y1 = ((1-WidthRatio)/2)*x1, (WidthRatio)*x1, ((1-HeightRatio)/2)*y1, (HeightRatio)*y1  
        # set geometry for the window
        self.setGeometry(int(x0),int(y0),int(x1),int(y1))
        # set Window icon
        if icon != False:
            self.setWindowIcon(QtGui.QIcon(icon))
        else:
            pass
