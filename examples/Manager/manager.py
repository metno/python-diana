from datetime import datetime
from OpenGL import GL
from metno.diana import *

class TestManager(Manager):

    def __init__(self):

        Manager.__init__(self)
        self.enabled = False

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
        return True

    def plot(self, under, over):

        print "plot", self, under, over
        GL.glPushMatrix()
        plotRect = self.plotm.getPlotSize()
        w, h = self.plotm.getPlotWindow()
        #GL.glTranslatef(editRect.x1, editRect.y1, 0.0);
        #            glScalef(plotRect.width()/w, plotRect.height()/h, 1.0);
        #              editItemManager->draw();
        GL.glPopMatrix()
    
    def setPlotModule(self, pm):

        self.plotm = pm

    def isEnabled(self):

        return self.enabled

    def setEnabled(self, enable):

        self.enabled = enable
