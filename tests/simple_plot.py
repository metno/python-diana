#!/usr/bin/env python

from datetime import datetime
import sys

from metlibs import milogger
from diana import Controller, LocalSetupParser, PaintGL, PaintGLContext
from qt import QImage, QPainter, QRect

def read_input_parameters(lines):

    d = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        elif line.startswith("PLOT"):
            break
        
        pieces = line.split("=")
        if len(pieces) > 1:
            key, value = pieces[0], "=".join(pieces[1:])
            d[key] = value
    
    return d

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
    
    lines = open(input_path).readlines()
    parameters = read_input_parameters(lines)
    plot_lines = read_plot_commands(lines)
    
    try:
        width, height = map(int, parameters.get("buffersize", "400x400").split("x"))
    except IndexError:
        sys.stderr.write("%s: Incorrect number of values assigned to buffersize.\n" % input_path)
        sys.exit(1)
    except ValueError:
        sys.stderr.write("%s: Invalid value assigned to buffersize.\n" % input_path)
        sys.exit(1)
    
    # Perform the plot.
    
    c.getFieldManager().updateSources()
    c.archiveMode(False)
    
    wrapper = PaintGL()
    context = PaintGLContext()
    context.makeCurrent()
    
    image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
    painter = QPainter()
    painter.begin(image)
    context.begin(painter)
    context.viewport = QRect(0, 0, width, height)
    
    c.setPlotWindow(width, height)
    #c.keepCurrentArea(True)
    dt = datetime.now()
    c.setPlotTime(dt)
    
    c.plotCommands(plot_lines)
    
    fieldtimes = []
    sattimes = []
    obstimes = []
    objtimes = []
    ptimes = []
    c.getPlotTimes(fieldtimes, sattimes, obstimes, objtimes, ptimes)
    times = fieldtimes + sattimes + obstimes + objtimes + ptimes
    times.sort()
    if times:
        print "Plotting for time", times[-1]
        c.setPlotTime(times[-1])
    
    c.updatePlots()
    #c.getMapArea().toLogString()
    c.plot();
    
    context.end()
    painter.end()
    
    image.save("temp.png")
    
    sys.exit()

