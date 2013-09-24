#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from metno.diana import *

from manager import TestManager
from dialog import TestDialog

if __name__ == "__main__":

    app = QApplication(sys.argv)
    paintgl = PaintGL()
    
    LocalSetupParser.parse("/etc/diana/diana.setup-COMMON")

    c = Controller()

    m = TestManager()
    c.addManager("test", m)
    c.addManager("drawing", DrawingManager.instance())

    if not c.parseSetup():
        sys.exit(1)

    mw = DianaMainWindow(c, "1.0", "1.0", "python-diana manager test")
    d = TestDialog(mw, c)
    mw.addDialog(d)

    mw.start()
    mw.show()

    sys.exit(app.exec_())
