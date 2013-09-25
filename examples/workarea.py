#!/usr/bin/env python

import datetime, sys
from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import QApplication, QDockWidget, QKeySequence, QMainWindow, \
                        QTreeWidget, QTreeWidgetItem
from metno.diana import *
from metno.metlibs import FieldRequest

class Window(QMainWindow):

    iso_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, controller, parent = None):

        QMainWindow.__init__(self, parent)
        
        self.controller = controller
        
        self.modelsList = QTreeWidget()
        self.modelsList.setColumnCount(1)
        self.modelsList.setHeaderHidden(True)

        self.modelsList.currentItemChanged.connect(self._setModelFromItem)
        
        self.fieldsList = QTreeWidget()
        self.fieldsList.setColumnCount(1)
        self.fieldsList.setHeaderHidden(True)

        self.fieldsList.currentItemChanged.connect(self._setFieldFromItem)
        
        self.timesList = QTreeWidget()
        self.timesList.setColumnCount(1)
        self.timesList.setHeaderHidden(True)

        self.timesList.currentItemChanged.connect(self._setPlotTimeFromItem)
        
        modelsDock = QDockWidget(self.tr("Models"))
        modelsDock.setWidget(self.modelsList)
        self.addDockWidget(Qt.LeftDockWidgetArea, modelsDock)
        
        fieldsDock = QDockWidget(self.tr("Fields"))
        fieldsDock.setWidget(self.fieldsList)
        self.addDockWidget(Qt.RightDockWidgetArea, fieldsDock)
        
        timesDock = QDockWidget(self.tr("Times"))
        timesDock.setWidget(self.timesList)
        self.addDockWidget(Qt.LeftDockWidgetArea, timesDock)
        
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        quitAction = fileMenu.addAction(self.tr("E&xit"))
        quitAction.setShortcut(QKeySequence.Quit)

        quitAction.triggered.connect(self.close)

        dockMenu = self.menuBar().addMenu(self.tr("&Docks"))
        dockMenu.addAction(modelsDock.toggleViewAction())
        dockMenu.addAction(fieldsDock.toggleViewAction())
        dockMenu.addAction(timesDock.toggleViewAction())

        work_area = WorkArea(controller)
        self.setCentralWidget(work_area)
    
    def readModels(self):

        info_list = self.controller.initFieldDialog()
        self.modelsList.clear()

        for info in info_list:

            item = QTreeWidgetItem()
            item.setText(0, info.groupName)
            self.modelsList.addTopLevelItem(item)

            for model in info.modelNames:

                child = QTreeWidgetItem()
                child.setText(0, model)
                item.addChild(child)

    def readFields(self):
    
        model, refTime, fieldGroups = self.controller.getFieldGroups(self.model, False)
        self.fieldsList.clear()
        
        fields = set()

        for group in fieldGroups:
            if group.modelName != model:
                continue
            for field in group.fieldNames:
                fields.add(field)
        
        fields = list(fields)
        fields.sort()
        for field in fields:

            item = QTreeWidgetItem()
            item.setText(0, field)
            self.fieldsList.addTopLevelItem(item)

    def _setModelFromItem(self, current):
    
        if current:
            model = current.text(0)
            self.setModel(model)
    
    def _setFieldFromItem(self, current):
    
        if current:
            field = current.text(0)
            self.setField(str(field))

    def _setPlotTimeFromItem(self, current):
    
        if current:
            time = current.data(0, Qt.UserRole).toPyObject()
            self.setPlotTime(time)
    
    def setModel(self, model):

        self.model = str(model)
        self.readFields()
    
    def setField(self, field):
    
        self.field = field

        request = FieldRequest()
        request.modelName = self.model
        request.paramName = field
        times = self.controller.getFieldTime([request])
        times.sort()
        self.updateTimes(times)

    def setPlotTime(self, time):

        self.time = time
        self.plot()

    def _updateTimesFromPlot(self, times):
    
        t = []
        self.timesList.clear()

        for key, values in times.items():
        
            for value in values:
                t.append((value, key))

        t.sort()
        self.updateTimes(self, times)

    def updateTimes(self, times):
    
        self.timesList.clear()

        for value in times:
        
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
    
    def plot(self):
    
        self.field_plots = ["FIELD model=%s plot=%s plottype=fill_cell" % (self.model, self.field)]

        l = ['AREA name=model/sat-area',
             'MAP backcolour=white map=Gshhs-Auto contour=on '
             'cont.colour=black cont.linewidth=1 cont.linetype=solid '
             'cont.zorder=1 land=on land.colour=flesh land.zorder=0 '
             'lon=off lat=off frame=off'] + self.field_plots
        
        self.controller.plotCommands(l)

        #times = self.controller.getPlotTimes()
        #self._updateTimesFromPlot(times)
        #
        #for key, values in times.items():
        #    if values:
        #        self.selectTime(values[-1])
        #        break
        #else:
        self.controller.setPlotTime(self.time)
        self.controller.updatePlots()
        self.update()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    paintgl = PaintGL()
    
    LocalSetupParser.parse("/etc/diana/diana.setup-COMMON")

    c = Controller()
    #c.addManager("drawing", DrawingManager.instance())
    if not c.parseSetup():
        sys.exit(1)

    window = Window(c)
    window.readModels()
    #window.plot()
    window.resize(800, 512)
    window.show()

    sys.exit(app.exec_())
    
    #import readline, rlcompleter
    #readline.parse_and_bind("tab: complete")
