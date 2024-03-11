"""
Name: Workers.py
Author: John Archibald Page
Created: 27/11/2023
Last Updated: 27/11/2023

Purpose: 
    Make a QRunnable class that will take in routines and put them on a seprate thread before running them.

Source:
    https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtCore
import logging as log
import numpy as np
from Routines.autoFocusing.contrastAlgorithum import contrastAlgorithums_class as  contrastAlgorithums#contrast algorithums: LAPV, LAPM, TENG, MLOG
import re

class functionWorker(QtCore.QRunnable):
    '''
    Worker thread: used to make any function into a QRunnable that can be threaded
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, fn, GUI, freeze, *args, **kwargs):
        super(functionWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn, self.GUI, self.freeze = fn, GUI, freeze
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        '''Initialise the runner function with passed args, kwargs. freezes the GUI while threaded if freeze == True'''
        try:
            if self.freeze == True:
                for i in self.GUI:
                    i.setEnabled(False)
            self.fn(*self.args, **self.kwargs)
            if self.freeze == True:
                for i in self.GUI:
                    i.setEnabled(True)
        except:
            for i in self.GUI:
                i.setEnabled(True)

class popupWorker(QtCore.QObject):
    """Write a pop-up message as a threaded worker"""
    popupsignal = QtCore.pyqtSignal(str, str, str, str)
    
    def __init__(self):
        super(popupWorker,self).__init__() 

    def create(self, windowtitle, messagetitle, message, messagetype):
        """sends signals to create a pop-up window"""
        self.popupsignal.emit(windowtitle, messagetitle, message, messagetype)
        #if this is an error message it will fail the routine
        if messagetype == "error":
            raise Exception(f"ERROR: {messagetitle}")

class currentStatusWorker(QtCore.QObject):
    """Write a message to the staus bar by emitting a signal which will be on its own thread seprate from the main process"""
    messageSignal, coloursignal = QtCore.pyqtSignal(str), QtCore.pyqtSignal(str)
    
    def __init__(self):
        super(currentStatusWorker,self).__init__() 

    def updateStatus(self,message, messagetype = "info"):
        """Formats the widget vals to be saved to a .csv"""
        messagetypedolourdict = {"info":"color: #b1b1b1; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);",
                                 "fail":"color: #323232 ; background-color: #EF0107",
                                 "success":"color: #323232 ; background-color: #66FF00",
                                 "routine":'color: #000000; background-color: #ffa02f' }
        #Add to the log
        log.info(message)
        #emit as a thread
        self.messageSignal.emit(message)
        self.coloursignal.emit(messagetypedolourdict[messagetype])

class DisplayWorker(QtCore.QObject):
    """Signals for all of the displays that will be updated continuously (.i.e. position, focus, filter)"""
    postext, focustext, exptext, filtertext = QtCore.pyqtSignal(str), QtCore.pyqtSignal(str), QtCore.pyqtSignal(str), QtCore.pyqtSignal(str)

    def __init__(self, filint, focint, posint, filterdriver, posdriver, Focdriver, camera):
        super(DisplayWorker, self).__init__()
        #interfacing
        self.focint, self.posint, self.filterint = focint, posint, filint
        #drivers
        self.focdriver, self.posdriver, self.filterdriver, self.camera =  Focdriver, posdriver, filterdriver,  camera

    def DisplayUpdater(self):
        """Keeps updating all the displays while running"""
        curthread = QtCore.QThread.currentThread() # the current thread this function is being ran on
        while True:
            curthread.usleep(10)#usleep takes int of microseconds to wait, so convert ms to us
            #focuser
            try:
                focusval = int(self.focint.position(self.focdriver))
                focuserpos = str(focusval)
                if focuserpos == "None" or focuserpos == "":
                    pass
                else:
                    self.focustext.emit("Focus: " + focuserpos +" steps")
            except:
                print("focuser briefly inaccessible...")
            #position
            try:
                aziposval, altposval = self.posint.currentposition(self.posdriver)
                azipos, altpos = str(round(float(aziposval),2)), str(round(float(altposval),2))
                self.postext.emit("Position: ( " + azipos +"\N{DEGREE SIGN} , "+ altpos +"\N{DEGREE SIGN} )")
            except:
                print("Mount briefly inaccessible...")
            #filter wheel
            try:
                filterpos = str(self.filterint.readFilterWheel(self.filterdriver))
                if filterpos == "None":
                    pass
                else:
                    self.filtertext.emit("Filter: " + filterpos)
            except:
                print("filter wheel briefly inaccessible...")
            #camera
            try:
                self.exptext.emit("Exposure: " + str(round(self.camera.currentExposure(),2))+" ms")
            except:
                print("exposure briefly inaccessible...")

class PlotWorker(QtCore.QObject):
    """This will release the current plot values to the pop-out"""
    pixelvalueplot, focusplot, hist_title, foc_title = QtCore.pyqtSignal(np.ndarray,np.ndarray), QtCore.pyqtSignal(list,list), QtCore.pyqtSignal(str), QtCore.pyqtSignal(str)
 
    def __init__(self, read, FocuserGUI, camera, ExposureGUI, hpGUI, connectfunctions):
        super(PlotWorker, self).__init__()
        #drivers
        self.read, self.FocGUI, self.ExpGUI, self.camera, self.cf = read, FocuserGUI, ExposureGUI, camera, connectfunctions
        #call buttons
        self.pausedatacaptureStack = self.cf.stackedrefences(hpGUI)[1] # continue/pause button
        self.refreshplotbutton = self.cf.pushbuttonsrefences(hpGUI)[0] # refresh the data
        self.savebutton = self.cf.pushbuttonsrefences(hpGUI)[3] # save the data button
        #call the plots
        self.plot1_hist = self.cf.glwrefences(hpGUI)[1].getItem(0, 0)
        self.plot2_focus = self.cf.glwrefences(hpGUI)[0].getItem(0, 0)
        #get the reference to the tabs
        self.tab = self.cf.Tabrefences(hpGUI)[0]
        #hist bin entry box
        self.binnum = self.cf.Textboxrefences(hpGUI)[0]
        #initalise the starting data values
        self.focuslist, self.stepslist = [], []
        #initalise a cehck to see if these values have updated
        self.expcheck1, self.foccheck1, self.bincheck1 = 0, 0, 0

    def plotUpdater(self):
        """Keeps updating all the plots while running"""
        curthread = QtCore.QThread.currentThread() # the current thread this function is being ran on
        while True:
            curthread.usleep(1)#usleep takes int of microseconds to wait, so convert ms to us
            #if the capturing data is not paused, run
            if self.pausedatacaptureStack.currentIndex() == 1:
                array = np.array(self.camera.currentimage) # the current image
                #if the refresh plot button is checked, reset the check button and set the lists to zero
                try: self.refresh(array)
                except: pass
                #pixel value Histogram
                try: self.Histogramplot(array)
                except: pass
                #steps vs Focus
                try:  self.Focusplot(array)
                except: pass 
            else:
                pass # the plotting machine is paused
                
    def Histogramplot(self, array,  maxsat = ((2**16)-1), refresh = False):
        """Keeps updating all the plots while running"""
        #first check whether the exposure has updated, if it has updated then change the histogram plot
        self.expcheck2 = float(re.findall(r'\d+\.\d+', self.ExpGUI.widget(0).title())[0])
        self.bincheck2 = int(self.binnum.text())
        #if exposure, bin number have changed or refresh flag is true, grab new data
        if self.expcheck2 != self.expcheck1 or self.bincheck2 != self.bincheck1 or refresh == True:
            # wait for exposure to update and state update
            self.camera.wait_for_new_Image() 
            self.hist_title.emit(f"Image Histogram; Current Exposure: {self.expcheck2} ms") # plot title stating exposure
            self.plot1_hist.clear() # clear existing plot
            #get the bin number
            binnum = int(self.binnum.text())
            histstep = maxsat/binnum #get the bin step for the histogram
            #find the histogram and the mid bin value
            self.histogram, bin_edges = np.histogram(array, bins=binnum)
            self.histmidbin = np.arange((histstep/2), maxsat+(histstep/2), histstep)
            # emit what is to be plotted
            self.pixelvalueplot.emit(self.histmidbin, self.histogram) 
        #update the check
        self.expcheck1, self.bincheck1 = self.expcheck2, self.bincheck2
            
    def Focusplot(self, array):
        """Keeps updating all the plots while running"""
        #get the roi to find the focus
        roiw,roih,fullw,fullh = [int(i) for i in self.read.getConstant(["ROIW", "ROIH", "ImageW","ImageH"])]
        ROIarray = array[(fullw-roiw)//2:(fullw+roiw)//2, (fullh-roih)//2:(fullh+roih)//2] # for focus
        #check if the focuser steps has moved, if so grab focus value
        self.foccheck2 = int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0])
        #if the focus has updated then grab more data
        if self.foccheck2 !=  self.foccheck1:
            self.foc_title.emit(f"Current Focus: {self.foccheck2} steps") # plot title
            
            #if the focus steps already exists, replace the contrast value
            if int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0]) in self.stepslist: 
                self.focuslist[np.where(self.stepslist == int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0]))] = contrastAlgorithums.TENG(ROIarray)
                #emit the signal
                self.focusplot.emit(self.stepslist,self.focuslist)
            
            #if this is a new data point then addit to the data point list
            if int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0]) not in self.stepslist:
                self.plot2_focus.clear()
                self.stepslist.append(int(re.findall(r'\d+', self.FocGUI.widget(0).title())[0]))
                self.focuslist.append(contrastAlgorithums.TENG(ROIarray))
                #re-arrange list to be in order
                index = sorted(range(len(self.stepslist)), key=lambda k: self.stepslist[k])
                self.stepslist, self.focuslist = [self.stepslist[i] for i in index], [self.focuslist[i] for i in index]
                #emit the signal
                self.focusplot.emit(self.stepslist,self.focuslist)
            
            #update the check if this is a new focus position point
            self.foccheck1 = self.foccheck2 

    def refresh(self, array):
        """Refreshes the data that is being shown if the button is clicked"""
        if self.refreshplotbutton.isChecked() == True:
            #histogram
            if self.tab.currentIndex() == 0:
                self.plot1_hist.clear() # clear the histogram
                self.Histogramplot(array, refresh = True) # update the plot
            #focusplot
            if self.tab.currentIndex() == 1:
                self.focuslist, self.stepslist = [], []
                self.plot2_focus.clear() # clear the focus plot
            #reset the check button
            self.refreshplotbutton.setChecked(False)