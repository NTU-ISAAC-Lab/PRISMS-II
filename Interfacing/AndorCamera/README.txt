SPECIFICATIONS
--------------
CAMERA
SERIES: ANDOR3
PRODUCT: Zyla 4.2 sCMOS (USB 3.0)
MODEL CODE: ZYLA-4.2-USB3-S
SERIAL NUMBER: VSC-06307
LINK: https://andor.oxinst.com/products/scmos-camera-series/zyla-4-2-scmos [Last Accessed 07/12/2022]

BRAND
NAME: Oxford Instruments Andor 
WEBSITE:https://andor.oxinst.com/ [Last Accessed 07/12/2022]
______________________________________________________________________________________________
HARDWARE
--------
With the current camera lens configuration (16/10/2023), the shortest focus distance is 2.241 m to over 17.319 m  from the camera.

______________________________________________________________________________________________
FRAMERATE & EXPOSURE
--------------------
Documented values:
	Fastest Frame rate Setting (limited by the USB 3.0): 30 Frames/s -> 1 frame every 0.033s
	Rolling Shutter Exposure time = Exposure time + 10 ms (For all rows to be exposured)
Tested values:
	Tested Average Fastest Frame rate: 27 s (found with exposure time of 0.95 ms)
	Input exposure vs time for a new image to come in: 30 ms, 60 ms, 90 ms -> 34 ms, 65 ms, 94 ms etc. so ~ exposure + 5 ms
		
______________________________________________________________________________________________
PYTHON (This is used by PRISMS II to interface with the stand)
-------
PYTHON LIBRARY: andor3
INSTALL VIA COMMANDLINE: pip install andor3
DOCUMENTATION: https://pypi.org/project/andor3/ [Last Accessed 08/12/2022]
______________________________________________________________________________________________
EXTERNAL SOFTWARE (NB! This software is not required to run PRISMS II)
-----------------
EXTERNAL SOFTWARE FOR INTERFACING: Andor Solis (a profile must be created to download this)
UTILITY: test camera is working
OS: N/A
LINK: https://andor.oxinst.com/downloads/view/andor-solis-64-bit-4.32.30065.0 [Last Accessed 08/12/2022]