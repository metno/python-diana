#!/usr/bin/env python

import readline, rlcompleter, sys
from PyQt4.QtGui import *
from metno.diana import *

if __name__ == "__main__":

    app = QApplication(sys.argv)
    paintgl = PaintGL()
    
    LocalSetupParser.parse("/etc/diana/setup/diana.setup-COMMON")

    c = Controller()
    #c.addManager("drawing", DrawingManager.instance())
    if not c.parseSetup():
        sys.exit(1)

    mw = DianaMainWindow(c, "0.00.0", "0.00.0", "python-diana")
    mw.start()
    mw.show()

    #sys.exit(app.exec_())
    readline.parse_and_bind("tab: complete")
