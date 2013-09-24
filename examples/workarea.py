#!/usr/bin/env python

#import readline, rlcompleter
import datetime, sys
from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import QApplication, QDockWidget, QMainWindow, \
                        QTreeWidget, QTreeWidgetItem
from metno.diana import *

class Window(QMainWindow):

    iso_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, controller, parent = None):

        QMainWindow.__init__(self, parent)
        
        self.controller = controller
        
        self.timesList = QTreeWidget()
        self.timesList.setColumnCount(1)
        self.timesList.setHeaderHidden(True)

        self.timesList.currentItemChanged.connect(self.setPlotTime)

        timesDock = QDockWidget(self.tr("Times"))
        timesDock.setWidget(self.timesList)
        self.addDockWidget(Qt.LeftDockWidgetArea, timesDock)
        
        dockMenu = self.menuBar().addMenu(self.tr("Windows"))
        dockMenu.addAction(timesDock.toggleViewAction())

        work_area = WorkArea(controller)
        self.setCentralWidget(work_area)

    def plot(self):

        l = ['AREA name=model/sat-area',
             'MAP backcolour=white map=Gshhs-Auto contour=on '
             'cont.colour=black cont.linewidth=1 cont.linetype=solid '
             'cont.zorder=1 land=on land.colour=flesh land.zorder=0 '
             'lon=off lat=off frame=off',
             'FIELD  model=HIRLAM.12KM.00(12) plot=T.2M colour=red plottype=contour linetype=solid linewidth=1 base=0 frame=1 line.interval=2 extreme.type=None extreme.size=1 extreme.radius=1 palettecolours=off patterns=off table=0 repeat=0 value.label=1 line.smooth=0 field.smooth=0 label.size=1 grid.lines=0 grid.lines.max=0 undef.masking=0 undef.colour=255:255:255:255 undef.linewidth=1 undef.linetype=solid grid.value=0 colour_2=off dim=1 unit=celsius', 'AREA name=model/sat-area']

        self.controller.plotCommands(l)

        times = self.controller.getPlotTimes()
        self.updateTimes(times)
        
        for key, values in times.items():
            if values:
                self.selectTime(values[-1])
                break
        else:
            self.controller.updatePlots()
            self.update()
    
    def setPlotTime(self, current):
    
        time = current.data(0, Qt.UserRole).toPyObject()
        self.controller.setPlotTime(time)
        self.controller.updatePlots()
        self.update()

    def updateTimes(self, times):
    
        t = []
        self.timesList.clear()

        for key, values in times.items():
        
            for value in values:
                t.append((value, key))

        t.sort()

        for value, key in t:
        
            item = QTreeWidgetItem()
            item.setText(0, value.strftime(self.iso_format))
            item.setData(0, Qt.UserRole, value)
            self.timesList.addTopLevelItem(item)

        self.timesList.resizeColumnToContents(0)

    def selectTime(self, time):
    
        i = 0
        while i < self.timesList.topLevelItemCount():

            item = self.timesList.topLevelItem(i)
            if item.text(0) == time.strftime(self.iso_format):
                self.timesList.setCurrentItem(item)
                return

            i += 1


if __name__ == "__main__":

    app = QApplication(sys.argv)
    paintgl = PaintGL()
    
    LocalSetupParser.parse("/etc/diana/diana.setup-COMMON")

    c = Controller()
    #c.addManager("drawing", DrawingManager.instance())
    if not c.parseSetup():
        sys.exit(1)

    window = Window(c)
    window.plot()
    window.resize(800, 512)
    window.show()

    sys.exit(app.exec_())
    #readline.parse_and_bind("tab: complete")
