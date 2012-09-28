#!/usr/bin/env python

from datetime import datetime
import sys

from metlibs import milogger
from diana import Controller, LocalSetupParser, PaintGL, PaintGLContext
from qt import QImage, QPainter, QRect

def read_plot_commands(lines):

    plot_lines = []
    in_plot = False
    for line in lines:
        if line.strip().startswith("#"):
            continue
        elif line.strip().startswith("PLOT"):
            in_plot = True
        elif line.strip().startswith("ENDPLOT"):
            in_plot = False
        elif in_plot and line.strip():
            plot_lines.append(line)
    
    return plot_lines

if __name__ == "__main__":

    if not 2 <= len(sys.argv) <= 3:
    
        sys.stderr.write("Usage: %s [setup file] <plot commands file>\n" % sys.argv[0])
        sys.exit(1)
    
    elif len(sys.argv) == 2:
    
        setup_path = "/etc/diana/diana.setup-COMMON"
        input_path = sys.argv[1]
    
    else:
        setup_path = sys.argv[1]
        input_path = sys.argv[2]
    
    logHandler = milogger.LogHandler.initLogHandler(2, "")
    logHandler.setObjectName("simple_plot")
    
    if not LocalSetupParser.parse(setup_path):
        print "LocalSetupParser failed to parse", setup_path
        sys.exit(1)
    
    c = Controller()
    if not c.parseSetup():
        print "Controller failed to parse", setup_path
        sys.exit(1)
    
    c.getFieldManager().updateSources()
    c.archiveMode(False)
    
    wrapper = PaintGL()
    context = PaintGLContext()
    context.makeCurrent()
    
    image = QImage(400, 400, QImage.Format_ARGB32_Premultiplied)
    painter = QPainter()
    painter.begin(image)
    context.begin(painter)
    context.viewport = QRect(0, 0, 400, 400)
    
    c.setPlotWindow(400, 400)
    #c.keepCurrentArea(True)
    dt = datetime.now()
    c.setPlotTime(dt)
    
    lines = open(input_path).readlines()
    plot_lines = read_plot_commands(lines)
    c.plotCommands(plot_lines)
    
    fieldtimes = []
    sattimes = []
    obstimes = []
    objtimes = []
    ptimes = []
    c.getPlotTimes(fieldtimes, sattimes, obstimes, objtimes, ptimes)
    print "Plotting for time", fieldtimes[-1]
    c.setPlotTime(fieldtimes[-1])
    
    print "Update plots:", c.updatePlots()
    print c.getMapArea().toLogString()
    c.plot();
    
    print "Plotted"
    context.end()
    painter.end()
    
    print "Saving"
    image.save("temp.png")
    
    print "Exiting"
    sys.exit()

