from datetime import datetime
from OpenGL.GL import *
from metno.diana import *

from PyQt4.QtCore import QEvent, QPointF, QRectF, Qt
from PyQt4.QtGui import QColor, QFont, QFontMetricsF, QPolygonF

class TestManager(Manager):

    def __init__(self):

        Manager.__init__(self)
        TestManager.instance = self
        
        # Define locations of labels in geographic coordinates using data from Wikipedia.
        self.points = [(QPointF(59 + 57/60.0, 10 + 45/60.0), "Oslo"),
                       (QPointF(60 + 23/60.0 + 22/3600.0, 5 + 19/60.0 + 48/3600.0), "Bergen")]
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
        
        metrics = QFontMetricsF(QFont())

        painter.save()
        painter.setPen(QColor(0, 0, 160))
        painter.setBrush(QColor(255, 255, 255, 192))
        painter.setCompositionMode(painter.CompositionMode_SourceOver)

        for point, label in self.points:
            ok, x, y = plotm.GeoToPhys(point.x(), point.y(), area, plot_size)
            y = plot_height - y
            if ok:
                rect = QRectF(x, y, metrics.width(label) + 8, metrics.height() + 8)
                painter.drawRect(rect)
                painter.drawText(rect, Qt.AlignCenter, label)

        painter.restore()
    
    def setPlotModule(self, pm):

        self.plotm = pm

