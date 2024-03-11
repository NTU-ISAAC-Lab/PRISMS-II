"""
NAME: histplotCON.py
AUTHOR: John Archibald Page
DATE CREATED: 25/01/2024
DATE LAST UPDATED: 06/02/2024

PURPOSE:
    To give functionality to the image plots of pixel value histogram and the focus steps vs the contrast.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
class histplotCON_class():
    """Build the functionality for the Filter controls"""
    def __init__(self, histplotGUI, CGUI, connectfunctions, save, Camera, plotWorker,  statusUpdater, savopendir):
        super(histplotCON_class,self).__init__()
        #initalise classes
        self.sv, self.cf, self.camera, self.pworker, self.su, self.saveopendir = save, connectfunctions, Camera, plotWorker, statusUpdater, savopendir
        #call in the main GUI
        self.hpGUI = histplotGUI
        #call buttons
        self.plotlaunchbutton = self.cf.pushbuttonsrefences(CGUI)[4]
        self.pausedatacaptureStack = self.cf.stackedrefences(self.hpGUI)[1] # continue/pause button
        self.saveplotbutton = self.cf.pushbuttonsrefences(self.hpGUI)[4]
        #call the plots
        self.plot1_hist = self.cf.glwrefences(self.hpGUI)[0].getItem(0, 0)
        self.plot2_focus = self.cf.glwrefences(self.hpGUI)[1].getItem(0, 0)
        #get the reference to the tabs
        self.tab = self.cf.Tabrefences(self.hpGUI)[0]
        #hist bin entry box
        self.binnum = self.cf.Textboxrefences(self.hpGUI)[0]
        self.binnum.setText("100") # initalise the number of bins as 100
        #call the pixel label
        self.pixellocatinolabel = self.cf.labelrefences(self.hpGUI)[-1] # call in plot location display label

        #connect the functionality
        try:
            self.connectpointerlocation()
            self.connectbuttons()
        except:
            self.su.updateStatus("plot failed to connect...")

    def connectbuttons(self):
        """Connect the functionality to all the buttons"""
        #launch button
        self.cf.widgetconnect(self.plotlaunchbutton, self.hpGUI.show)
        #plots buttons
        self.cf.widgetconnect(self.pausedatacaptureStack.widget(0), self.continuedatacaptureFUNC)
        self.cf.widgetconnect(self.pausedatacaptureStack.widget(1), self.pausedatacaptureFUNC)
        self.cf.widgetconnect(self.saveplotbutton, self.saveplotdateFUNC)
        self.tab.currentChanged.connect(self.showbinentry)

    #whether the hist bin box should be showing
    def showbinentry(self):
        """If the tab is changed away from histogram the bin entry will be hidden"""
        if self.tab.currentIndex() != 0:
            self.binnum.setHidden(True)
        else:
            self.binnum.setHidden(False)
            
    #save the data from the plots
    def saveplotdateFUNC(self):
        """Save the data from the plots"""    
        if self.tab.currentIndex() == 0:
            self.su.updateStatus("Saving Histogram data!")
            datlist = [[self.pworker.histmidbin[i],self.pworker.histogram[i]] for i in range(len(self.pworker.histmidbin))]
            savopendir = self.saveopendir(savediropen="save",filepurpose= "Save Histogram data", filepath = "\\OutputFiles\\PlotData\\", filetype="csv") # get the file name
            self.sv.datSave(datlist,savopendir.filename, headerlist = ["pixelVal", "Frequency"])
        else:
            self.su.updateStatus("Saving Focus plot data!")
            datlist = [[self.pworker.stepslist[i], self.pworker.focuslist[i]] for i in range(len(self.pworker.stepslist))]
            savopendir = self.saveopendir(savediropen="save",filepurpose= "Save Focus plot data", filepath = "\\OutputFiles\\PlotData\\", filetype="csv") # get the file name
            self.sv.datSave(datlist,savopendir.filename, headerlist = ["focusSteps", "focusContrast"])

    #pause and play data capture        
    def continuedatacaptureFUNC(self):
        """Flags the data capture to continue, switches button symbol"""
        self.pausedatacaptureStack.setCurrentIndex(1) #switch symbol to pause
        self.su.updateStatus("Data capture continued")

    def pausedatacaptureFUNC(self):
        """Flags the data capture to pause, switches button symbol"""
        self.pausedatacaptureStack.setCurrentIndex(0) #set symbol to continue
        self.su.updateStatus("Data capture paused")

    #update the pixel display value    
    def connectpointerlocation(self):
        """connect the location of the pointer"""
        self.plot1_hist.scene().sigMouseMoved.connect(self.mouseMovedHist) # histogram location
        self.plot2_focus.scene().sigMouseMoved.connect(self.mouseMovedFoc) # focus location

    def mouseMovedHist(self, evt):
        """Mouse moved updates what the location of the mouse is listed as on the image"""
        #return the pixel location
        mousePoint = self.plot1_hist.vb.mapSceneToView(evt)
        x, y = round(mousePoint.x(), 2), round(mousePoint.y(), 2)
        #update the label
        self.pixellocatinolabel.setText(u"\u2316 " + f"{x}, {y}")
        
    def mouseMovedFoc(self, evt):
        """Mouse moved updates what the location of the mouse is listed as on the image"""
        #return the pixel location
        mousePoint = self.plot2_focus.vb.mapSceneToView(evt)
        x, y = round(mousePoint.x(), 2), round(mousePoint.y(), 2)
        #update the label
        self.pixellocatinolabel.setText(u"\u2316 " + f"{x}, {y}")