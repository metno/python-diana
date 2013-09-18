#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from metno.diana import *

import manager

if __name__ == "__main__":

    app = QApplication(sys.argv)
    paintgl = PaintGL()
    
    LocalSetupParser.parse("/etc/diana/diana.setup-COMMON")

    c = Controller()

    m = manager.TestManager()
    c.addManager("test", m)
    c.addManager("drawing", DrawingManager.instance())

    if not c.parseSetup():
        sys.exit(1)

    mw = DianaMainWindow(c, "1.0", "1.0", "python-diana manager test")

    testToolBar = mw.addToolBar("Test")
    testAction = testToolBar.addAction("Enable test mode")
    testAction.setCheckable(True)
    testAction.setChecked(False)

    testAction.toggled.connect(m.setEnabled)

    mw.start()
    mw.show()

    sys.exit(app.exec_())
