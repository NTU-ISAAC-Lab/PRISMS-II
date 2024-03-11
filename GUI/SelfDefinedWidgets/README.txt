FOLDER: SelfDefinedWidgets
AUTHOR: John Archibald Page
DATE CREATED:18/11/2022
LAST UPDATED: 01/12/2022
_____________________________________________________________________________

PURPOSE:
This folder contains self defined widgets to be used in PRISMS II interface.

UPDATE HISTORY:

_____________________________________________________________________________
FOLDER FILE DIRECTORY:
PRISMS II ALPHA
|__|GUI
|__|__|SelfDefinedWidgets
|__|__|__|MainWindow.py
|__|__|__|TextEdit_AutoverticleExpansion.py
|__|__|__|popupMessage.py
|__|__|__|savediropen.py
|__|__|__|AdvancedOptions.py
______________________________________________________________________________
FOLDER FILE FUNCTIONALITY:
AdvancedOptions.py
	Window with 3 option buttons and a message. the functionality of buttons is defined when class is called.
MainWindow.py
	A main window pop up that can have compoents appended to it as it scales depending on screen hardware.
TextEdit_AutoverticleExpansion.py
	A vertical exapnding text box that can be used as a terminal.
popupMessage.py
	Creates a pop up message with more information.
savediropen.py
	Creates a pop up to save a file in a given location under a given name with given name.

_______________________________________________________________________________
FOLDER FILE WINDOW LAYOUTS:
------------------
AdvancedOptions.py
------------------
Define a button that will launch the pop up with the following class:
>PRISMS II ALPHA/GUI/SelfDefinedWidgets/
PushButton_AdvancedOptions.AOPushButton(label,title,messagetitle, message,button1,func1,button2,func2,button3,func3,col=True)

Click button:
|label|
--->
Launches pop-up:
_______________________________
|@|Title_____________________|X|             
|Pop up title&message          |                          
|______________________________|                 
|button1|      |Button2|button3|
-------------------------------

Where buttons# have functionality func#


---------------
popupMessage.py 
---------------
Define a button that will launch the pop up with the following class:
>PRISMS II ALPHA/GUI/SelfDefinedWidgets/
PushButton_popupMessage.moreinfoPushButton(messagefile)

Where message file has the following format:

title, Terminal: Serial Port Full Names
messagetitle, Serial Port Full Name
message,No Ports Available...
windowicon,False
width,300

Where the window icon can be set to something unique

Click button:
|...|
--->
Launches pop-up:
________________________
|@|Title______________|X| 
|messagetitle           |             
|message                |                 
|_______________________|                
|____________________|OK|
<--------width---------->

--------------
savediropen.py
--------------
Launches a normal directory pop up to save a file

savopendir_class(savediropen,icon,filepurpose, filepath, filetype)

where 

savediropen can be "open", "save" or "dir"

icon can be a unique icon

filepurpose will be printed as the window title with the type of window
.i.e. "Save " + filepurpose = "Save Config. file"

filepath = where the directory initially opens to

filetype can either be "csv" or "image"
_______________________________________________________________________________

FILE DEPENDANTS:

-------------
MainWindow.py
-------------
GUI.MainWindow.PRISMSIIGUI.py
---------------------------------
TextEdit_AutoverticleExpansion.py 
---------------------------------
GUI.MainWindow.b_TerminalGUI.py

------------------------------------
AdvancedOptions.py
------------------------------------
GUI.LaunchWindow.LaunchSavefile.py
	
---------------------------------
popupMessage.py 
--------------------------------- 
GUI.SelfDefinedWidgets.PushButton_popupMessage.py
GUI.LaunchWindow.LaunchSavefile.py

--------------------------------
savediropen.py
--------------------------------
GUI.SelfDefinedWidgets.PushButton_saveopendir.py 

_______________________________________________________________________________
FILE DEPENDANCIES:

------------------------------------
AdvancedOptions.py
------------------------------------
from PyQt5 import QtWidgets, QtCore

---------------------------------
popupMessage.py 
--------------------------------- 
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

--------------------------------
savediropen.py
--------------------------------
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon

-------------
MainWindow.py
-------------
from PyQt5 import QtGui, QtWidgets
import screeninfo
import re

---------------------------------
TextEdit_AutoverticleExpansion.py 
---------------------------------
from PyQt5 import QtWidgets
