from datetime import datetime
from OpenGL.GL import *
from metno.diana import *

from PyQt4.QtCore import QEvent

class TestManager(Manager):

    def __init__(self):

        Manager.__init__(self)
        self.enabled = False
        TestManager.instance = self

        self.points = []

    def parseSetup(self):

        #print "parseSetup", self
        return True

    def sendMouseEvent(self, event, res):

        #print "sendMouseEvent", self, event, res

        if event.type() == QEvent.MouseButtonPress:
            xmap, ymap = self.plotm.PhysToMap(event.x(), event.y())
            print xmap, ymap
            self.points.append((xmap, ymap))
            res.repaint = True

    def sendKeyboardEvent(self, event, res):

        #print "sendKeyboardEvent", self, event, res
        pass
    
    def getTimes(self):
    
        today = datetime.today()
        return map(lambda hour:
                   datetime(today.year, today.month, today.day, hour, 0, 0),
                   range(12))
    
    def prepare(self, time):

        print "prepare", time
        return True

    def changeProjection(self, newArea):

        print "changeProjection", self, newArea
        return True

    def plot(self, under, over):
    
        if not under:
            return

        glColor3i(0, 0, 0)
        glBegin(GL_POLYGON)
        for point in self.points:
            glVertex2f(*point)
        glEnd()
    
    def setPlotModule(self, pm):

        self.plotm = pm

    def isEnabled(self):

        return self.enabled

    def setEnabled(self, enable):
    
        self.enabled = enable
