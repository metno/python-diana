from datetime import datetime
from OpenGL.GL import *
from metno.diana import *

from PyQt4.QtCore import QEvent, QPointF
from PyQt4.QtGui import QColor, QPolygonF

class TestManager(Manager):

    def __init__(self):

        Manager.__init__(self)
        TestManager.instance = self
        
        self.points = [QPointF(60, 10), QPointF(65, 15), QPointF(70, 10), QPointF(65, 5)]
        self.area = None

    def parseSetup(self):

        #print "parseSetup", self
        return True
    
    def processInput(self, lines):

        print "processInput", lines
        return True

    def sendMouseEvent(self, event, res):

        print "sendMouseEvent", self, event, res

        if event.type() == QEvent.MouseButtonPress:
            xmap, ymap = self.plotm.PhysToMap(event.x(), event.y())
            print xmap, ymap
            self.points.append((xmap, ymap))
            res.repaint = True

    def sendKeyboardEvent(self, event, res):

        print "sendKeyboardEvent", self, event, res
        pass
    
    def getTimes(self):
    
        today = datetime.today()
        return [datetime(today.year, today.month, today.day, 12, 0, 0)]
    
    def prepare(self, time):

        #print "prepare", time
        return True

    def changeProjection(self, newArea):

        #print "changeProjection", self, newArea
        self.area = newArea
        return True

    def plot(self, under, over):
    
        if not under:
            return
        
        ctx = PaintGL.instance().currentContext
        painter = ctx.painter
        plotm = PlotModule.instance()
        area = plotm.getCurrentArea()
        plot_size = plotm.getPlotSize()
        plot_width, plot_height = plotm.getPlotWindow()
        
        painter.save()
        painter.setBrush(QColor(160, 240, 160))
        points = []
        for point in self.points:
            ok, x, y = plotm.GeoToPhys(point.x(), point.y(), area, plot_size)
            if ok:
                points.append(QPointF(x, plot_height - y))
        polygon = QPolygonF(points)
        painter.drawPolygon(polygon)
        painter.restore()
    
    def setPlotModule(self, pm):

        self.plotm = pm

