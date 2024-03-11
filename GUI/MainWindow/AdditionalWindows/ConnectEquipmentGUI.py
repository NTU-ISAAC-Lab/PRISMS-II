"""
Name: ConnectEquipmentGUI.py
Author: John Archibald Page
Created: 31/05/2023
Last Updated: 31/05/2023

Purpose: 
    Depending on what has connected, state the functionality of the launch.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets
from GUI.SelfDefinedWidgets.AdvancedOptions import AdvancedOptions_Widget
from ConnectWidget.advancedOptions.ConnectEquipment import ConnectEquipment_class

class ConnectEquipmentGUI_class():
    """GUI to show which equipment is connected for a launch"""
    def __init__(self):
        ce = ConnectEquipment_class()
        self.runpopup(ce.name,ce.available)

    def runpopup(self,name,available):
        """Pop-up window confirmation of choice for a given PRISMS II launch"""
        #gui title
        title="PRISMS II: Equipment Connection"
        #html table of the coms results
        mes = "<table><tr><th>  Component  </th><th>  Connected?  </th></tr>"
        for i in range(len(name)):
            mes += "<tr><td>  {}  <td></td>  {}   </td></tr>".format(name[i],available[i])
        mes += "</table>"
        #make buttons for bottom of the GUI
        but2 = QtWidgets.QPushButton("Cancel")
        but3 = QtWidgets.QPushButton("Confirm")
        #define the functions for the buttons
        func2, func3 = lambda: exit(), lambda: self.window.close()
        #define the messagetitle
        mes_title = "All Components Connected!" if all(x == True for x in available) else "WARNING! Not all Components Connected...<br> Continue with reduced functionnality?"
        #create the gui window
        self.window = AdvancedOptions_Widget(title, mes_title, mes, but2, func2, but3, func3, backoveride = True)
        #show the window
        self.window.show()