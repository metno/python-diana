
# Copyright (C) 2012 met.no
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from datetime import datetime
import sys

from metlibs import milogger
from diana import Controller, LocalSetupParser, PaintGL, PaintGLContext
from PyQt4.QtCore import QRect
from PyQt4.QtGui import QImage, QPainter

class BDiana:

    """Provides an API to access Diana plotting functionality.
    
    Once a BDiana instance is created, it is used in the following way.
    First, it must be configured by supplying a setup file to the setup()
    method. This provides information about the location of resources.

    Plot commands are supplied to the instance in the form of an InputFile
    object that is passed to the prepare() method.

    Data typically needs to be plotted for a given time. The getPlotTimes()
    method returns a chronologically sorted list of valid times. One of
    these must be passed to the setPlotTime() method.

    Once the plot time has been defined, an image of the plot can be
    produced by calling the plot() method with the desired width and
    height values, measured in pixels.
    """

    def __init__(self, log_level = 2, file_name = "", object_name = ""):
    
        self.logHandler = milogger.LogHandler.initLogHandler(log_level, file_name)
        self.logHandler.setObjectName(object_name or sys.argv[0])

        self.controller = None
    
    def setup(self, setup_path):
    
        """Parses the setup file specified by setup_path, returning True if
        successful or False if unsuccessful.
        """
        if not LocalSetupParser.parse(setup_path):
            return False
        
        self.controller = Controller()
        if not self.controller.parseSetup():
            return False

        return True
    
    def prepare(self, input_file, archive = False):
    
        """Prepares input from the specified input_file for plotting.
        """
        self.controller.getFieldManager().updateSources()
        self.controller.archiveMode(archive)
        
        #c.keepCurrentArea(True)
        dt = datetime.now()
        self.controller.setPlotTime(dt)
        
        self.controller.plotCommands(input_file.plot_lines)
    
    def getPlotTimes(self):

        """Returns a list of available plot times for the currently selected
        input file.
        """
        fieldtimes = []
        sattimes = []
        obstimes = []
        objtimes = []
        ptimes = []
        
        self.controller.getPlotTimes(fieldtimes, sattimes, obstimes, objtimes, ptimes)
        times = fieldtimes + sattimes + obstimes + objtimes + ptimes
        times.sort()

        return times
    
    def setPlotTime(self, plot_time):
    
        """Sets the time to use for the plot, returning True if successful or
        False if unsuccessful.

        The time to use is typically obtained using the getPlotTimes() method.
        """
        if not self.controller.setPlotTime(plot_time):
            return False
        else:
            return self.controller.updatePlots()

    def getPlotArea(self):
    
        """Returns the plot area that will be displayed in the plot.
        """
        return self.controller.getMapArea()
    
    def plot(self, width, height, image_format = QImage.Format_ARGB32_Premultiplied):
    
        """Plots the data specified in the current input file as an image with
        the specified width and height, and with an optionally specified image
        format.
        """
        self.controller.setPlotWindow(width, height)
        
        wrapper = PaintGL()
        context = PaintGLContext()
        context.makeCurrent()
        
        image = QImage(width, height, image_format)
        painter = QPainter()
        painter.begin(image)
        context.begin(painter)
        context.viewport = QRect(0, 0, width, height)

        self.controller.plot()
        
        context.end()
        painter.end()

        return image

class InputFile:

    """Represents an input file for use with a BDiana instance."""

    def __init__(self, input_path):

        lines = open(input_path).readlines()
        self.parameters = self.read_input_parameters(lines)
        self.plot_lines = self.read_plot_commands(lines)
    
    def getBufferSize(self, width = 400, height = 400):
    
        """Returns the buffer size as specified in the input file or the
        the default values specified as optional width and height arguments.

        If the buffer size in the input file is invalid, a BDianaError
        exception is raised.
        """
        try:
            if self.parameters.has_key("buffersize"):
                width, height = map(int, self.parameters["buffersize"].split("x"))
        except IndexError:
            raise BDianaError, "%s: Incorrect number of values assigned to buffersize.\n" % input_path
        except ValueError:
            raise BDianaError, "%s: Invalid value assigned to buffersize.\n" % input_path

        return width, height
    
    def read_input_parameters(self, lines):
    
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
    
    def read_plot_commands(self, lines):
    
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

