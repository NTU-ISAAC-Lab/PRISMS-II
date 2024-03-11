"""
NAME: CameraCON.py
AUTHOR: John Archibald Page
DATE CREATED: 29/11/2022 
DATE LAST UPDATED: 28/07/2023

PURPOSE:
    To write functionality to the camera display and the camera saving button and darkfield.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
import pyqtgraph as pg
import math
import itertools

class CameraCON_class():
    """Build the functionality for the Filter controls"""
    def __init__(self,CGUI,camera_class,connectfunctions,connectequipment, statusUpdater, read):
        super(CameraCON_class,self).__init__()
        #initalise classes
        self.cf, self.camera, self.su, self.read  = connectfunctions, camera_class, statusUpdater, read
        #add the camera to the main display stack
        self.displaystack = self.cf.stackedrefences(CGUI)[1] #call the stackwidget currently consisting of just placeholder
        #call buttons
        self.plapaStack = self.cf.stackedrefences(CGUI)[0] # play/pause button
        self.snapshotsavebutton = self.cf.pushbuttonsrefences(CGUI)[2] # call in the save button
        self.cubesavebutton = self.cf.pushbuttonsrefences(CGUI)[3] # call in the save button
        self.plot = self.cf.glwrefences(CGUI)[0].getItem(0, 0)
        self.imageitem = self.cf.glwrefences(CGUI)[0].getItem(0, 0).allChildItems()[3]
        self.pixellocatinolabel = self.cf.labelrefences(CGUI)[-1] # call in plot location and value display label
        #call toggles
        self.ROItog = self.cf.checkboxrefences(CGUI)[0] 
        self.onetoonetog = self.cf.checkboxrefences(CGUI)[1] 
        self.falsecolourtog = self.cf.checkboxrefences(CGUI)[2]
        #list the colourmaps that will be used
        self.falsecolourmap = self.customColourmap()
        self.binarycolourmap = pg.colormap.getFromMatplotlib('binary') # from white to dark
        self.binarycolourmap.reverse() # from black to white
        #self.RGBtog = self.cf.checkboxrefences(CGUI)[3] #to toggle to the rgb camera #10/10/2023
        #check the port is available and ready to be connected to
        self.ce = connectequipment
        if self.ce.available[0] == True:
            try:
                self.connectbuttons()
                self.connectpointerlocation()
                self.ROIitem = self.createROI()
            except:
                self.su.updateStatus("Camera failed to connect...")
        else:
            self.su.updateStatus("Camera not connected...")

#button connect------------------------------------------------------------------
    def connectbuttons(self):
        """Connect the functionality to all the exposure buttons"""
        #buttons
        self.cf.widgetconnect(self.plapaStack.widget(0), self.playFUNC)
        self.cf.widgetconnect(self.plapaStack.widget(1), self.pauseFUNC)
        #toggles
        self.falsecolourtog.stateChanged.connect(self.showFalseColour)
        self.ROItog.stateChanged.connect(self.showROI)
        self.onetoonetog.stateChanged.connect(self.showonetoone)
            
#button functionality------------------------------------------------------------
    def playFUNC(self):
        """Functionality of save current set-up button"""
        self.camera.openEvent() #start stream again
        self.plapaStack.setCurrentIndex(1) #switch symbol to pause as stream is playing
        self.su.updateStatus("Camera Stream Continued!")

    def pauseFUNC(self):
        """Functionality of save current set-up button"""
        self.camera.closeEvent() #close stream
        self.plapaStack.setCurrentIndex(0) #set symbol to play, ready for stream to be played again
        self.su.updateStatus("Camera Stream Paused!")
      
#toggle functionality---------------------------------------------------------------    
    def createROI(self):
        """Shows the region of interest"""
        roi, imgshape = [int(i) for i in self.read.getConstant(["ROIW", "ROIH"])], [int(i) for i in self.read.getConstant(["ImageW","ImageH"])]
        x0, y0 = int((imgshape[0]-roi[0])//2),  int((imgshape[1]-roi[1])//2) # origin position
        #initalise painter with colours
        ROIitem = pg.ROI([x0, y0], [int(roi[0]), int(roi[1])], pen='red',movable=False,rotatable=False,resizable=False)
        self.plot.addItem(ROIitem) #show ROI
        ROIitem.hide() # initally hide this item
        return(ROIitem)

    def showROI(self):
        """Shows the region of interest is ROI is checked"""
        if self.ROItog.isChecked() == True:
            #update the roi to the one in the current config file
            roi, imgshape = [int(i) for i in self.read.getConstant(["ROIW", "ROIH"])], [int(i) for i in self.read.getConstant(["ImageW","ImageH"])]
            x0, y0 = int((imgshape[0]-roi[0])//2),  int((imgshape[1]-roi[1])//2) # origin position
            self.ROIitem.pos = [x0, y0]
            self.ROIitem.size = [int(roi[0]), int(roi[1])]
            #show the ROI
            self.ROIitem.show()
        else:
            self.ROIitem.hide()
        
    def showonetoone(self): 
        """Sets display to one to one to the ROI. Must be even to be central"""
        roi, imgshape = [int(i) for i in self.read.getConstant(["ROIW", "ROIH"])], [int(i) for i in self.read.getConstant(["ImageW","ImageH"])]
        if self.onetoonetog.isChecked() == True: # just ROI shown
            x0, x1, y0, y1 = int((imgshape[0]-roi[0])//2),   int((imgshape[0]+roi[0])//2),   int((imgshape[1]-roi[1])//2),  int((imgshape[1]+roi[1])//2)
        else: #whole display frame size
            x0, x1, y0, y1 = int(0), int(imgshape[0]), int(0), int(imgshape[1])
        self.plot.setXRange(x0, x1, padding=0)
        self.plot.setYRange(y0, y1, padding=0)

    def showFalseColour(self): 
        """switch on a false colour to get another prespective on what is being seen"""
        if self.falsecolourtog.isChecked() == True: # just ROI shown
            self.imageitem.setColorMap(self.falsecolourmap)
        else: #whole display frame size
            self.imageitem.setColorMap(self.binarycolourmap)

    def customColourmap(self):
        """custom false colourmap"""
        #"Face-based luminance matching for perceptual colormap generation" - Kindlmann et al 2002
        #the colour gradient of the main body
        colourlist_main = [
                    (255, 255, 255),     #white
                    (0*255, 0.559*255, 0.559*255),#cyan
                    (0*255, 0.592*255, 0*255),     #green
                    (0.316*255, 0.316*255, 0.991*255), #blue 
                    (0, 0, 0) #black
                    ]
        #the colour of the areas that are above effective saturation
        colourlist_Ef = [
                        (255, 102, 0), #orange caution colour of being over Ef 
                        (255, 0, 0) #red       
                    ]
        #get the colour lists that will be used for each range
        Ef = int(self.read.getConstant(["EffSat"]))
        colours_Main = self.gradientbetweencolours(colourlist_main, length =  Ef)
        colours_OverEf = self.gradientbetweencolours(colourlist_Ef, length = (2**16) - Ef)
        #combine the colourmaps
        colours = colours_Main + colours_OverEf
        #make the colourmap
        cmap_custom = pg.ColorMap(pos=None, color=colours)
        return(cmap_custom)
            
    def gradientbetweencolours(self, colourlist, length = (2**16) - 1):
        """Make a gradient between n colours"""
        try:
            #0)find out how many colours should be between each colours
            gradientlength_raw = (length - len(colourlist))/(len(colourlist) - 1)
            #1)check this is a whole number, if not put the extra gradient in the earlier part of the list
            part, full = math.modf(gradientlength_raw)
            gradientlength = [full]*len(colourlist)
            if float(part) != float(0):
                remainder = part*(len(colourlist) - 1)
                smallest_divide = 1
                #find the smallest number the remainder can be divided between while still being a whole number
                for i in range(len(colourlist)):
                    test_remainder = remainder / (i+1)
                    tr_part, tr_full = math.modf(test_remainder)
                    if tr_part == 0:
                        smallest_divide = (i+1)
                #divide the remainder through the first few colours
                for i in range(smallest_divide):
                    gradientlength[i] = gradientlength[i] + remainder/smallest_divide 
            #2)making colours fading between the colours 
            chunks = [[(colourlist[i][0] + (colourlist[i+1][0] - colourlist[i][0]) * (1/(gradientlength[i])) * j,
                        colourlist[i][1] + (colourlist[i+1][1] - colourlist[i][1]) * (1/(gradientlength[i])) * j,
                        colourlist[i][2] + (colourlist[i+1][2] - colourlist[i][2]) * (1/(gradientlength[i])) * j) for j in range(int(gradientlength[i]))] for i in range(len(colourlist) - 1)]
            #3) slot in the colour values at each end of the chunks
            colours_and_chunks = [[colourlist[i]]+chunks[i] for i in range(len(chunks))]
            colours_and_chunks.append([colourlist[-1]])
            #4) join all the colours to one length
            colours = list(itertools.chain.from_iterable(colours_and_chunks))
        except:
            raise Exception("The length must be longer than the colourlist!!!")
        return(colours)
    
    def connectpointerlocation(self):
        """connect the location of the pointer"""
        self.plot.scene().sigMouseMoved.connect(self.mouseMoved)

    def mouseMoved(self, evt):
        """Mouse moved updates what the location of the mouse is listed as on the image"""
        #bring in variables that will be used in calculations
        self.pixellocatinolabel.setStyleSheet("color: #b1b1b1;")
        fullx, fully, Ef = [int(i) for i in self.read.getConstant(["ImageW","ImageH", "EffSat"])]
        #return the pixel location
        mousePoint = self.plot.vb.mapSceneToView(evt)
        x, y = abs(fullx-int(mousePoint.x())), abs(fully-int(mousePoint.y()))
        try:
            if (x < fullx-1) and (x >=0) and (y < fully-1) and (y >=0):
                #find the value of the pixel at this location
                pixelvalue = self.camera.currentimage[int(mousePoint.x())][int(mousePoint.y())]
                #update the label
                self.pixellocatinolabel.setText(u"\u2316 " + f"{x}, {y}px; {pixelvalue}")
                #set the label colour depedning on whether the value is higher than the effective saturation but bellow full saturation (orange), or at full saturation (red)
                if int(pixelvalue) == int((2**16) - 1):
                    self.pixellocatinolabel.setStyleSheet("color: #EF0107;")
                if pixelvalue >= Ef and pixelvalue < (2**16) - 1:
                    self.pixellocatinolabel.setStyleSheet("color: #ff6600;") 
        except:
            pass