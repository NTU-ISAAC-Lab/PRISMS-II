File: PRISMS II ALPHA
Author: John Archibald Page
Date Created:20/11/2022
Date Last Updated: 05/06/2023
__________________________________________________________________________________________

PURPOSE:
This folder contains all of PRISMS II, which is run in a compartmentalised fashion

UPDATE HISTORY:
__________________________________________________________________________________________
FOLDER FILE DIRECTORY:

PRISMS II ALPHA
|___|ConnectSerial
|___|ConnectWidget
|___|GUI
|___|InputFiles
|___|Interfacing
|___|OutputFiles
|___|Routines
|___|MainPRISMSII.py
|___|PRISMSIIStyle.css
|___|requirements.txt
|___|README.txt
__________________________________________________________________________________________
FOLDER FILE FUNCTIONALITY:
Much of the functionality of the files in the subfolders are already described, 
or have self explanatory names. Therefore, below is a breif dummary, followed by the flow of the 
files into the main running problem

ConnectSerial
	checks drivers are available to be connected to, functinoality to connect automatically to pre-defined drivers.
ConnectWidget
	connecting the interfacing to the GUI buttons
GUI
	The main GUI and basic internal funcitonality such as saving files
InputFiles
	config, coms etc.
Interfacing
	interfacing with the equipment of PRISMS II, such as camera, focuser, filter etc.
OutputFiles
	LOGS, images, dat files
Routines
	The algoriuthms for calculating the Scan, auto exposure and auto focusing
InitiateLogging.py
	This is the config for the log files used throughout the programs
MainPRISMSII.py
	this runs the scripts
PRISMSIIStyle.css
	this defines the style of PRISMS II.
_________________________________________________________________________________
PROGRAM FLOW:
   		                            |InputFiles
     OutputFiles                            ↓
         ↑
MainPRISMSII.py <---ConnectSerial <--- |ConnectingWidgets <--- |Routines
   ↑			   ↑	      ↑			      |Interfacing
   |PRISMSIIStyle.css	   |----------|GUI