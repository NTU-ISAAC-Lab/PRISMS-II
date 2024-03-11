"""
Name: ThreadingConnecting.py
Author: John Archibald Page
Created: 25/10/2023
Last Updated: 21/11/2023

Purpose: 
    joining worker classes for updating the continuous displays, logging, and camera to update their respective threads

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtCore
from GUI.SelfDefinedWidgets.popupMessage import popupmessage_class

class ThreadingConnecting_class(QtCore.QObject):

    def __init__(self, displayWorker, cameraWorker, logWorker, emergencySTOPworker, popupWorker, plotWorker, CameraGUI, StatusGUI,PositionGUI, FilterGUI, FocuserGUI, ExposureGUI, histplotGUI, connectfunctions): #histplotGUI, plotWorker,
        super(ThreadingConnecting_class,self).__init__()
        #useful functions
        self.cf = connectfunctions
        #Worker classes: Focuser, pos, filterwheel, camera, status
        self.displayW, self.cameraW, self.logW, self.stopW, self.popupW, self.plotW = displayWorker, cameraWorker, logWorker, emergencySTOPworker, popupWorker, plotWorker
        #displays
        self.filtergroupbox, self.focusergroupbox, self.posgroupbox, self.expgroupbox =  self.cf.groupboxrefences(FilterGUI)[1], self.cf.groupboxrefences(FocuserGUI)[1], self.cf.groupboxrefences(PositionGUI)[1], self.cf.groupboxrefences(ExposureGUI)[1]
        self.statusbar = self.cf.Textboxrefences(StatusGUI)[0]
        self.imageitem = self.cf.glwrefences(CameraGUI)[0].getItem(0, 0).allChildItems()[3]
        #plots
        self.plot1_hist = self.cf.glwrefences(histplotGUI)[1].getItem(0, 0)
        self.plot2_focus = self.cf.glwrefences(histplotGUI)[0].getItem(0, 0)
        #launch all of the threads
        self.popupLaunch()
        self.displayLaunch()
        self.logLaunch()
        self.cameraLaunch()
        self.plotLaunch()

#launch basic threads       
    def popupLaunch(self):
        """attach stop routine to a thread"""
        #1) create the threads
        self.popupthread = QtCore.QThread()
        #2) move functions to the thread
        self.popupW.moveToThread(self.popupthread)
        #3) connect the buttons
        self.popupW.popupsignal.connect(popupmessage_class)
        #4) start the thread
        self.popupthread.start()
        
    def displayLaunch(self):
        """attach displays to a thread"""
        #1) create the threads
        self.displaythread = QtCore.QThread()
        #2) move functions to the thread
        self.displayW.moveToThread(self.displaythread) 
        #3) connect the buttons
        self.displayW.filtertext.connect(self.filtergroupbox.setTitle)
        self.displayW.postext.connect(self.posgroupbox.setTitle)
        self.displayW.focustext.connect(self.focusergroupbox.setTitle)
        self.displayW.exptext.connect(self.expgroupbox.setTitle)
        #4) connect the continuous functions to start when the thread starts
        self.displaythread.started.connect(self.displayW.DisplayUpdater)
        #5) start the thread
        self.displaythread.start() 

    def logLaunch(self):
        """attach log to a thread"""
        #1) create the threads
        self.logthread = QtCore.QThread() 
        #2) move functions to the thread
        self.logW.moveToThread(self.logthread)
        #3) connect the buttons
        self.logW.messageSignal.connect(self.statusbar.setText)
        self.logW.coloursignal.connect(self.statusbar.setStyleSheet)
        #4) start the thread
        self.logthread.start()
        
    def cameraLaunch(self):
        """attach camera outcoming images to a thread"""
        self.cameraW.image_acquired.connect(self.imageitem.setImage)
        #self.cameraW.image_acquired.connect(self.imageitem.addColorBar)

    def plotLaunch(self):
        """attach camera outcoming images to a thread"""
        #1) create the threads
        self.plotthread = QtCore.QThread()
        #2) move functions to the thread
        self.plotW.moveToThread(self.plotthread) 
        #3) connect the buttons
        self.plotW.pixelvalueplot.connect(self.plot1_hist.plot)
        self.plotW.focusplot.connect(self.plot2_focus.plot)
        self.plotW.hist_title.connect(self.plot1_hist.setTitle)
        self.plotW.foc_title.connect(self.plot2_focus.setTitle)
        #4) connect the continuous functions to start when the thread starts
        self.plotthread.started.connect(self.plotW.plotUpdater)
        #5) start the thread
        self.plotthread.start() 