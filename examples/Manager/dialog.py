from PyQt4.QtCore import *
from PyQt4.QtGui import *
from metno.diana import *

from manager import TestManager

class TestDialog(DataDialog):

    #emitTimes = pyqtSignal("miutil::miString", "std::vector<miutil::miTime>")

    def __init__(self, parent, controller):

        DataDialog.__init__(self, parent, controller)
        
        self._action = QAction(self.tr("&Test mode"), self)
        self._action.setShortcut(self.tr("Ctrl+Shift+T"))

        updateButton = QPushButton(self.tr("&Update times"))
        updateButton.clicked.connect(self.updateTimes)

        layout = QVBoxLayout(self)
        layout.addWidget(updateButton)

    def action(self):
    
        print self, "action"
        return self._action

    def updateTimes(self):
    
        tm = TestManager.instance
        times = tm.getTimes()
        self.emitTimes.emit("test", times)
        #self.applyData.emit()
