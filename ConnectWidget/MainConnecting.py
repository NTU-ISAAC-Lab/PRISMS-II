"""
NAME: MainConnecting.py
AUTHOR: John Archibald Page
DATE CREATED: 05/12/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    Connect all the GUI buttons to the interfaces. All the classes will be called here and the drivers connected

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
#GUI
from GUI.MainWindow.PRISMSIIGUI import PRISMSIIGUI_class
from GUI.SelfDefinedWidgets.scrollablepopupMessage import scrollPopup_Widget
from GUI.SelfDefinedWidgets.savediropen import savopendir_filedialog
from GUI.MainWindow.AdditionalWindows.caputureCubeGUI import captureCube_class
from GUI.SelfDefinedWidgets.AdvancedOptions import AdvancedOptions_Widget
from GUI.MainWindow.AdditionalWindows.ScanGUI import ScanCreate_class
from GUI.MainWindow.AdditionalWindows.ConfigGUI import ConfigCreate_class
from GUI.MainWindow.AdditionalWindows.histplotGUI import histplot_class
from GUI.SelfDefinedWidgets.popupMessage import popupmessage_class
#connecting groups
from ConnectWidget.StatusCON import StatusCON_class
from ConnectWidget.PositionCON import PositionCON_class
from ConnectWidget.FilterCON import FilterCON_class
from ConnectWidget.FocusCON import FocusCON_class
from ConnectWidget.CameraCON import CameraCON_class
from ConnectWidget.ExposureCON import ExposureCON_class
from ConnectWidget.advancedOptions.captureCubeCON import captureCubeCON_class
from ConnectWidget.advancedOptions.SetUpCON import SetUpCON_class
from ConnectWidget.advancedOptions.ScanCON import ScanCON_class
from ConnectWidget.advancedOptions.ConfigCON import ConfigCON_class
from ConnectWidget.advancedOptions.histplotCON import histplotCON_class 
from ConnectWidget.RoutineCON import RoutineCON_class
from ConnectWidget.EmergencySTOPCON import EmergencySTOPWorker
#threading
from ConnectWidget.Threading.ThreadingConnecting import ThreadingConnecting_class
from ConnectWidget.Threading.Workers import popupWorker, currentStatusWorker, DisplayWorker, PlotWorker
#interfacing
from Interfacing.AndorCamera.AndorCamera import AndorCamera_class
from Interfacing.MoonliteFocuser.MoonliteFocuser import Moonlite_class
from Interfacing.ZaberStand.ZaberStand import ZaberStand_class
from Interfacing.FilterWheel.FilterWheel import FilterWheel_class
#from Interfacing.StandaStand.StandaStand import StandaStand_class # connected in the positionCON connecting
#functions
from ConnectWidget.advancedOptions.ConnectEquipment import ConnectEquipment_class
from ConnectWidget.ConnectFunctions import ConnectFunctions_class
from Interfacing.CSV.SaveCSV import Save_class
from Interfacing.CSV.ReadCSV import Read_class
#standard modules
import os

class MainConnecting_class():
    """Calls in the buttons, then connects each grouping individually."""
    def __init__(self):
        super(MainConnecting_class,self).__init__()
        #-1)initalise the config path for the set-up
        os.environ["CONFIGFILEPATH"] = os.getcwd() + "\\InputFiles\\Config\\DEFAULT.CSV"
        #0) useful functions
        self.ce = ConnectEquipment_class()
        self.save = Save_class()
        self.read = Read_class()
        self.statusUpdater = currentStatusWorker() 
        #1) GUI and widgets
        self.histplot = histplot_class()
        self.cubeCaptureWindow = captureCube_class()
        self.Scanwindow = ScanCreate_class(self.read)
        self.configwindow = ConfigCreate_class()
        self.PRISMSIIwindow = PRISMSIIGUI_class(self.read)
        Camera,Status,Position,Filter,Focuser,Exposure,AO,self.STOP = self.GUICall()
        #2) functions fiunctions to connect GUI
        self.cf = ConnectFunctions_class([Position,Filter,Focuser,Exposure])
        #3) interfacing with equipment
        self.focuserint = Moonlite_class()
        self.positionint = ZaberStand_class(self.read)
        self.filterint = FilterWheel_class()
        self.cameradriver = AndorCamera_class(self.read) 
        #4)connect functionality to the buttons that are connected
        self.callDrivers()
        self.CheckConnect(Position.widget(0),Filter.widget(0),Camera.widget(0),Focuser.widget(0),Exposure.widget(0))
        
        #try to connect funcitons that depend on other functionality
        #5)workers
        try: self.emergencythread = EmergencySTOPWorker(self.focuserint, self.positionint, self.posdriver, self.focusdriver,  self.STOP, self.cf, self.statusUpdater, [Position,Filter,Focuser,Exposure])
        except: self.statusUpdater.updateStatus("Emergency stop not connected...", messagetype ="fail")
        try: self.displaythread = DisplayWorker(self.filterint, self.focuserint, self.positionint, self.filterdriver, self.posdriver, self.focusdriver, self.cameradriver)
        except: self.statusUpdater.updateStatus("display thread not connected...", messagetype ="fail")
        try: self.popupworker = popupWorker()
        except: self.statusUpdater.updateStatus("popup Worker not connected...", messagetype ="fail")
        try: self.plotworker = PlotWorker(self.read, Focuser, self.cameradriver, Exposure, self.histplot, self.cf)
        except: self.statusUpdater.updateStatus("Plot worker not connected...", messagetype ="fail")
        #6)connect the advanced options and routines only dependant on the GUI and interfacing
        try: self.histplotCON = histplotCON_class(self.histplot, Camera, self.cf, self.save, self.cameradriver, self.plotworker, self.statusUpdater, savopendir_filedialog) 
        except: self.statusUpdater.updateStatus("Plot functionality not connected...", messagetype ="fail")
        try: self.capturecubeCON = captureCubeCON_class(Camera, self.cubeCaptureWindow, self.cf,self.save,self.read, savopendir_filedialog)
        except: self.statusUpdater.updateStatus("Capture image cube not connected...", messagetype ="fail")
        try: self.ScanCON = ScanCON_class(self.capturecubeCON, Focuser, AO, self.Scanwindow, Position, self.cf,self.save,self.read, savopendir_filedialog, AdvancedOptions_Widget)
        except: self.statusUpdater.updateStatus("Scan routine not connected...", messagetype ="fail")
        try: self.StatusCON = StatusCON_class(Status,scrollPopup_Widget,self.cf)
        except: self.statusUpdater.updateStatus("Status updater not connected...", messagetype ="fail")  

        #7)call in routines requiring interfacing with equipment
        try: self.threading = ThreadingConnecting_class(self.displaythread, self.cameradriver, self.statusUpdater,self.emergencythread, self.popupworker, self.plotworker, Camera, Status, Position, Filter, Focuser, Exposure, self.histplot, self.cf)
        except: self.statusUpdater.updateStatus("Main Threads not connected...", messagetype ="fail")
        try: self.setupCON = SetUpCON_class(AO, self.statusUpdater, self.save, self.read, self.cf, AdvancedOptions_Widget, savopendir_filedialog, self.cameradriver, self.FocCON, self.FilCON, self.PosCON, Position, Filter, Focuser, Exposure)
        except: self.statusUpdater.updateStatus("Set up not connected...", messagetype ="fail")
        try: self.ConfigCON = ConfigCON_class(self.cameradriver, AO, self.configwindow, self.cf, self.save,self.read, savopendir_filedialog, AdvancedOptions_Widget)
        except: self.statusUpdater.updateStatus("Config not connected...", messagetype ="fail")
        try: self.routine = RoutineCON_class(Filter, Camera, self.cubeCaptureWindow, Position, Focuser, Exposure, self.Scanwindow, self.cameradriver, self.focusdriver, self.FocCON, self.FilCON, self.ScanCON, self.PosCON, self.read, self.save, self.cf,  savopendir_filedialog, self.setupCON, self.statusUpdater, self.popupworker)
        except: self.statusUpdater.updateStatus("Routines not connected...", messagetype ="fail")
        
        #launch main window
        self.statusUpdater.updateStatus("Ready...", messagetype ="success")
        self.RunMainWindow()

    def GUICall(self):
        """Call in all the GUI to assign the buttons to."""
        self.PRISMSII = PRISMSIIGUI_class(self.read)
        #find each of the GUI
        Status =  self.PRISMSII.Status.MaingroupBox
        AOI = self.PRISMSII.AO.MaingroupBox
        STOP = self.PRISMSII.STOP # stacked button
        Camera = self.PRISMSII.Camera.MaingroupBox
        Position = self.PRISMSII.Position.MaingroupBox
        Filter = self.PRISMSII.Filter.MaingroupBox
        Focuser = self.PRISMSII.Focus.MaingroupBox
        Exposure = self.PRISMSII.Exposure.MaingroupBox
        return(Camera,Status,Position,Filter,Focuser,Exposure,AOI,STOP)

    def RunMainWindow(self):
        """Launches the main window after the buttons have been connected"""
        self.PRISMSII.MainWindow.show()

    def callDrivers(self):
        """Connect to the drivers"""
        #camera
        if self.ce.available[0] == True:
            try:
                self.cameradriver = AndorCamera_class(self.read) # initalise camera widget 
                self.cameradriver.launchCamera()
            except: 
                pass
        #azi-alt stand
        if self.ce.available[1] == True:
            try: self.posdriver = self.positionint.connectStand()
            except: pass
        #filter
        if self.ce.available[2] == True:
            try: self.filterdriver = self.ce.connectDriver(self.ce.deviceava[2]) 
            except: pass
        #focuser
        if self.ce.available[3] == True:
            try: self.focusdriver = self.ce.connectDriver(self.ce.deviceava[3]) 
            except: pass

    def CheckConnect(self,Position,Filter,Camera,Focuser,Exposure):
        """Checks whether they are connected, if not then do not connect the buttons"""
        self.ce.available # convert to boolean
        checkpower = [True,True,True,True]
        try: #maincamera and exposure groupboxes
            if self.ce.available[0]==True:
                self.camCON = CameraCON_class(Camera,self.cameradriver, self.cf, self.ce,self.statusUpdater, self.read)
                self.expCON = ExposureCON_class(Exposure, self.cameradriver, self.cf,self.ce, self.statusUpdater, self.read)
        except:
            self.ce.available[0]=False
            checkpower[0]=False
        try:
            if self.ce.available[1]==True: #position: just position groupbox
                self.PosCON = PositionCON_class(Position, self.positionint, self.cf, self.ce, self.posdriver,self.statusUpdater, self.read, self.STOP)
        except:
            self.ce.available[1]=False
            checkpower[1]=False
        try:    
            if self.ce.available[2]==True: #filter: just filter groupbox
                self.FilCON = FilterCON_class(Filter, self.cf, self.ce, self.filterint,  self.filterdriver,self.statusUpdater)
        except:
            self.ce.available[2]=False
            checkpower[2]=False
        try:    
            if self.ce.available[3]==True: #focus: just focus groupbox
                self.FocCON = FocusCON_class(Focuser,self.cf,self.focuserint,self.ce ,self.focusdriver,self.statusUpdater, self.read, self.STOP)
        except:
            self.ce.available[3]=False
            checkpower[3]=False
        if False in checkpower:
            self.popup = popupmessage_class("CONNECTING ERROR...", "Equipment not plugged in :(", f"Your USBs are connected, but some of your power is not...", "error")