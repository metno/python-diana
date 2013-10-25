from PyQt4.QtCore import *
from PyQt4.QtGui import *
from metno.diana import *

from manager import TestManager

class TestDialog(DataDialog):

    def __init__(self, parent, controller):

        DataDialog.__init__(self, parent, controller)
        
        self._action = QAction(self.tr("&Test mode"), self)
        self._action.setShortcut(self.tr("Ctrl+Shift+T"))
        self._action.setCheckable(True)
        self._action.toggled.connect(TestManager.instance.setEnabled)

        updateButton = QPushButton(self.tr("&Update times"))
        updateButton.clicked.connect(self.updateTimes)

        layout = QVBoxLayout(self)
        layout.addWidget(updateButton)
    
    def name(self):

        return "TestDialog"

    def action(self):
    
        return self._action

    def updateTimes(self):
    
        tm = TestManager.instance
        times = tm.getTimes()
        self.emitTimes.emit("test", times)
