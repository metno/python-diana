#!/usr/bin/env python

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from metno import bdiana

class Window(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        quitAction = fileMenu.addAction(self.tr("E&xit"))
        quitAction.setShortcut(QKeySequence.Quit)

        imageMenu = self.menuBar().addMenu(self.tr("&Image"))
        createAction = imageMenu.addAction(self.tr("&Create"))
        createAction.setShortcut(self.tr("Ctrl+Return"))

        createAction.triggered.connect(self.createImage)
        quitAction.triggered.connect(self.close)

        self.editorDock = QDockWidget()
        self.editor = QTextEdit()
        self.editorDock.setWidget(self.editor)
        self.addDockWidget(Qt.RightDockWidgetArea, self.editorDock)

        self.displayLabel = QLabel()
        self.displayLabel.resize(600, 600)
        self.setCentralWidget(self.displayLabel)

    def createImage(self):

        inp = bdiana.InputFile()
        inp.fromString(str(self.editor.toPlainText()))
        
        b = bdiana.BDiana()
        b.setup("/etc/diana/diana.setup-COMMON")
        b.prepare(inp)

        times = b.getPlotTimes()
        if not times:
            return

        b.setPlotTime(times[-1])
        im = b.plotImage(600, 600)
        self.displayLabel.setPixmap(QPixmap.fromImage(im))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
