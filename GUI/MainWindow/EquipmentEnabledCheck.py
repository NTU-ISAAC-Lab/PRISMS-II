"""
NAME: EquipmentEnabledCheck.py
AUTHOR: John Archibald Page
DATE CREATED: 01/12/2022 
DATE LAST UPDATED: 05/12/2022

PURPOSE:
    To check the connected is equal to true, if not a placeholder widget is put into place and widgets are not connected.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from ConnectWidget.advancedOptions.ConnectEquipment import ConnectEquipment_class

class EquipmentEnabledCheck_class():
    """Build the GUI for the camera settings, contating controls for Focus and Exposure"""
    def __init__(self,position,filter,camera,Focus, Exposure):
        super(EquipmentEnabledCheck_class,self).__init__()
        self.ce = ConnectEquipment_class()
        self.widgetstoDisable(position,filter,camera,Focus, Exposure)

    def widgetstoDisable(self,position,filter,camera,Focus, Exposure):
        """Assign component widgets to disable"""
        connectedvalue = self.ce.available
        #filter: just filter groupbox
        if connectedvalue[2]==False:
            self.switchtoPlaceHolder(filter)
        #position: just position groupbox
        if connectedvalue[1]==False:
            self.switchtoPlaceHolder(position)
        #just Focus: Focus
        if connectedvalue[3]==False:
            self.switchtoPlaceHolder(Focus)
        #Just Main camera: toggles, exposure
        if connectedvalue[0]==False: # and connectedvalue[4]==False
            self.switchtoPlaceHolder(camera)
            self.switchtoPlaceHolder(Exposure)
        #Just RGB Camera: RGB toggle
        #if connectedvalue[0]==True and connectedvalue[4]==False:
        #    self.switchtoPlaceHolder(camera)

    def switchtoPlaceHolder(self,stackwidget):
        """Effectively disables the widget while putting in a place holder to show where it was"""
        stackwidget.setCurrentIndex(1)