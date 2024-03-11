File: MainWindow
Author: John Archibald Page
Date Created:18/11/2022
Date Last Updated: 30/01/2024
____________________________________________________________________________________________
PURPOSE:
This file puts the groupings of the main GUI together into one, as shown in "layout.jpg", shown below:
MainWindow
 	    __________________________
        |________________________|  a_Camera
        | a            ||b______||  b_Status
        |              ||d______||  c_Position  
        |              ||e      ||  d_Filter
        |              ||_______||  e_Focuser
        |______________||  f    ||  f_AdvancedOptions
        |d     |e      ||_______||
        |      |       || STOP  ||
        ''''''''''''''''''''''''''

UPDATE HISTORY:

____________________________________________________________________________________________
FOLDER FILE DIRECTORY:
PRISMS II ALPHA
|___|GUI
|___|___|MainWindow
|___|___|___|PRISMSIIGUI.py
|___|___|___|a_CameraGUI.py
|___|___|___|b_StatusGUI.py
|___|___|___|c_PositionGUI.py
|___|___|___|d_FilterGUI.py
|___|___|___|e_FocuserGUI.py
|___|___|___|f_Exposure.py
|___|___|___|g_AOGUI.py
|___|___|___|AdditionalWindows
____________________________________________________________________________________________
FOLDER FILE FUNCTIONALITY:
PRISMSIIGUI.py
	Launches all the components of the main window and builds them into a layout.
a_CameraGUI.py
	camera interface
b_StatusGUI.py
	Status to input commands
c_PositionGUI.py
	Orientation grouping
d_FilterGUI.py
	Filter grouping
e_Focuser.py
	Focuser grouping
f_Exposure.py
	Exposure grouping
g_AOGUI.py
	Advanced Options Grouping
EquipmentEnabledCheck.py
	Check whether to hide this GUI if the equipment is not connected
____________________________________________________________________________________________
GUI COMPONENT LAYOUTS:
a_CameraGUI.py
--------------

GUI, with funcitoning 'save image' and 'set dark' buttons, using GUI.SelfDefinedWidgets.PushButton_saveopendir.py

 __Camera____________________________
|Camera Fcunationality  |toggles     |
|Pause/play|            |1:1         |
|SAVE_snapshot|         |ROI         |
|SAVE_cube|             |False Colour|
|Plotinformation|______ |____________|
|		                             |                   
|                                    |  
|  DISPLAY                           |
|                                    |          
|____________________________________|

b_StatusGUI.py
----------------

GUI of a Status

 __Status__________________             ||-----------------------||
| _____________________|...|    ---->   ||Status history         || 
										||_______________________||                                
										||Back____________________|			

c_PositionGUI.py
----------------
GUI of positon controls
	
_Orientation___________
|0,0||______||______|>|
|     | u |           |
| ___ ===== ___       |
|| < ||___|| > |      |
| --- | d | ---       |
|______---____________|        


d_FilterGUI.py
--------------

GUI of filter controls

 _Filter___________
|dial              |

e_FocuserGUI.py
----------------------

GUI of Focuser controls

 __Focus___________________
|||Auto |     |_____| > | |         
|| ______  _____  ______  |          
|||__Nr__||_____||__Fr__|_|

f_ExposureGUI.py
----------------------

GUI of Focuser controls

 __Exposure_______________
|||Auto |     |_____| > | |         
|| ______  _____  ______  |          
|||__Nr__||_____||__Fr__|_|


----------
f_AOGUI.py
----------

GUI of advanced options controls, with functionality of GUI.SelfDefinedWidgets.PushButton_AdvancedOptions.py

 _Advance_Options_
|   |Scan |       |
|    =======      |
|   |Set-Up |     |
|    =======      |
|   |Config.|     |
|_________________|
