"""
NAME: TextEdit_Auto_verticleExpansion.py
AUTHOR: John Archibald Page
DATE CREATED: 11/11/2022 
DATE LAST UPDATED: 11/11/2022

PURPOSE:
    Textedit box that automatically expands vertically when expanded.

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
"""
from PyQt5 import QtWidgets

class GrowingTextEdit(QtWidgets.QTextEdit):
    """To have an automatic growing verticle textedit box"""
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)  
        self.document().contentsChanged.connect(self.sizeChange)
        self.heightMin, self.heightMax = 0, 65000

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(int(docHeight))