FOLDER: AdditionalWindows
AUTHOR: John Archibald Page
DATE CREATED:18/11/2022
LAST UPDATED: 01/12/2022
_____________________________________________________________________________
PURPOSE:
This file contains classes used to create pop up windows with additional options or messages.

UPDATE HISTORY:
_____________________________________________________________________________
FOLDER FILE DIRECTORY:
PRISMS II ALPHA
|__|GUI
|__|__|AdditionalWindows
|__|__|__|ConfigGUI.py
|__|__|__|ScanGUI.py
|__|__|__|histplotGUI.py
|__|__|__|captureCubeGUI.py
|__|__|__|Connect EquipmentGUI.py

______________________________________________________________________________
FOLDER FILE FUNCTIONALITY:

ConfigGUI.py
	Pop-up that allows editting and creation of unique config file from the default that can be applied.
ScanGUI.py
	Pop-up that allows editting and creation of unique Scan file that can be ran.
histplotGUI.py
	pop-up that shows the histogram of the current image and the focus at different positions.
captureCubeGUI.py
	Pop-up that allows capture of an image cube with different exposure settings and save locations.
ConnectEquipmentGUI.py
	Pop-up of which equipment is currently crceated in this launch of PRISMS II.

_______________________________________________________________________________
FOLDER FILE WINDOW LAYOUTS:
GUI of advanced options controls, with functionality of GUI.SelfDefinedWidgets.PushButton_AdvancedOptions.py

 _Advance_Options_
|   |Scan |       |
|    =======      |
|   |Set-Up |     |
|    =======      |
|   |Config.|     |
|_________________|

These buttons lead to the following pop-ups:

Scan:
________________________
|@|Scan______________|X|             
|Pop up title&message    |  ------> Further action/ additional window                          
|________________________|                 
|Back|      |Open|Create |

Set-Up:
________________________
|@|Set-Up_____________|X|             
|Pop up title&message   |  ------> Further action/ additional window                          
|_______________________|                 
|Back|        |Open|Save|

Config.:
________________________
|@|Config.____________|X|             
|Pop up title&message   |  ------> Further action/ additional window                          
|_______________________|                 
|Back|   |Open|Create|

ConfigGUI.py
-------------------------------
setting the class to a button:
ConfigCreate_class()

means the button will launch the following window:
 _________________________________________________
|@|Create Config                                |X| 
|-------------------------------------------------|            
| _Equipment____________________  _____________   |              
|| |Main Camera|      |Focuser| ||  Switch     |  |
|| |Positional Stand| |Filter|  ||    in       |  |
||        |RGB Camera|          ||     widget  |  |
||______________________________||             |  | 
| _Interface____________________ |             |  |  
||                              ||             |  |
|||save paths|  |Coms|          ||             |  |
||______________________________||_____________|  | 
|-------------------------------------------------|                
|Back|                                |SAVE|APPLY||
--------------------------------------------------

When clicking one of the buttons on the left means that the interface
on the right will switch out to give th eoption to edit the vairable inputs
which can then be applied to prisms or saved for another time.

ScanGUI.py
------------------------------- 

setting the class to a button:
ScanCreate_class()

means the button will launch the following window:
________________________________
|@|Create Scan              |X| |
|-------------------------------|            
|_Exposure_time________________ |  
| |autoexposure|  |setexposure| |
||filter: 1 2 3 4 5 6 7 8 9 10 ||  
||Set-exp| | | | | | | | | | | ||
|_Mosacing Region_______________| 
|| FOV  |-----------|     rows ||
|| Start|           |     x    ||
|| End  |           |   Columns||
||      |-----------|     Cubes||
|_overlap______________________ |  
||thetaol, Phiol: |      |    |||
|_File_Name_&_Save_Location____ |  
||file name:     |         |   ||  
||Save location: |         |   ||
|_CRASH ROUTINE________________ |  
||Cube number: |         |  |x|||  
|------------------------------||                
|Back|                |SAVE|RUN||
--------------------------------

histplotGUI.py
--------------

typing in the values to the line edit options and clicking save saves
as a .csv file, but clicking run launches the Scan functionality with 
the current open Scan file.
one plot is the histogram of the current window, and the other is the focus amount

_______________________________________________________________
|@|Focuser Curve_____________________________________________|X|            
| HIST| FOCUS|_________________________________________________|
|                                                              |
|                                                              |
|--------------------------------------------------------------|                
|Back| Clear data | refresh data | pause/continue data capture||

captureCubeGUI.py
-----------------

________________________________
|@|Capture Cube             |X| |
|-------------------------------|            
|_Exposure_time________________ |  
| |autoexposure|  |setexposure| |
||fil: 1 2 3 4 5 6 7 8 9 10    ||  
||exp | | | | | | | | | | | |o|||
|_File_Name_&_Save_Location____ |  
||file name:     |         |   ||  
||Save location: |         ||o|||  
|------------------------------||                
|Back|                 |CAPTURE||
--------------------------------

ConnectEquipmentGUI.py
----------------------



