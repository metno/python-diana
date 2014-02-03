from PyQt4.QtCore import *
from PyQt4.QtGui import *
from metno.diana import *

from manager import TestManager

class TestDialog(DataDialog):

    def __init__(self, parent, controller):

        DataDialog.__init__(self, parent, controller)
        
        self._action = QAction(self.tr("&Show Places"), self)
        self._action.setShortcut(self.tr("Ctrl+Shift+T"))
        self._action.setCheckable(True)
        self._action.toggled.connect(TestManager.instance.setEnabled)

        applyButton = QPushButton(self.tr("&Apply"))
        applyButton.clicked.connect(self.apply)
        editButton = QPushButton(self.tr("&Edit"))
        editButton.clicked.connect(self.toggleEditing)
        updateButton = QPushButton(self.tr("&Update times"))
        updateButton.clicked.connect(self.updateTimes)

        layout = QVBoxLayout(self)
        layout.addWidget(applyButton)
        layout.addWidget(editButton)
        layout.addWidget(updateButton)
    
    def name(self):
    
        # Indicate that the dialog handles PLACES plot commands.
        return "PLACES"

    def action(self):
    
        return self._action

    def updateTimes(self):
    
        tm = TestManager.instance
        times = tm.getTimes()
        self.emitTimes.emit("PLACES", times)

    def getOKString(self):
    
        lines = ["PLACES %f,%f,%s" % (59 + 57/60.0, 10 + 45/60.0, "Oslo"),
                 "PLACES %f,%f,%s" % (60 + 23/60.0 + 22/3600.0, 5 + 19/60.0 + 48/3600.0, "Bergen")]
        return lines
    
    def putOKString(self, lines):
    
        TestManager.instance.processInput(lines)

    def toggleEditing(self):

        tm = TestManager.instance
        tm.setEditing(not tm.isEditing())

    def apply(self):

        TestManager.instance.setEnabled(True)
        self.applyData.emit()
