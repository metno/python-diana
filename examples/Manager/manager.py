from datetime import datetime
from OpenGL.GL import *
from metno.diana import *

class TestManager(Manager):

    def __init__(self):

        Manager.__init__(self)
        self.enabled = False
        TestManager.instance = self
        self.editRect = PlotModule.instance().getPlotSize()

    def parseSetup(self):

        #print "parseSetup", self
        return True

    def sendMouseEvent(self, event, res):

        #print "sendMouseEvent", self, event, res
        pass

    def sendKeyboardEvent(self, event, res):

        #print "sendKeyboardEvent", self, event, res
        pass
    
    def getTimes(self):
    
        print "getTimes", self
        today = datetime.today()
        return map(lambda hour:
                   datetime(today.year, today.month, today.day, hour, 0, 0),
                   range(12))
    
    def prepare(self, time):

        print "prepare", time
        return True

    def changeProjection(self, newArea):

        #print "changeProjection", self, newArea
        self.editRect = PlotModule.instance().getPlotSize()
        return True

    def plot(self, under, over):

        print "plot", self, under, over
        glPushMatrix()
        plotRect = self.plotm.getPlotSize()
        w, h = self.plotm.getPlotWindow()
        glTranslatef(self.editRect.x1, self.editRect.y1, 0.0)
        glScalef(plotRect.width()/w, plotRect.height()/h, 1.0)
        print self.editRect.x1, self.editRect.y1
        print plotRect.x1, plotRect.y1
        glColor3i(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex2f(0, 0)
        glVertex2f(100, 0)
        glVertex2f(0, 100)
        glVertex2f(100, 100)
        glVertex2f(0, 0)
        glEnd()
        glPopMatrix()
    
    def setPlotModule(self, pm):

        self.plotm = pm

    def isEnabled(self):

        return self.enabled

    def setEnabled(self, enable):
    
        self.enabled = enable
