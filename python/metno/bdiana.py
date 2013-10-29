
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
import os, sys

from metlibs import FieldRequest, milogger
from diana import Colour, Controller, LocalSetupParser, PaintGL, PaintGLContext, \
                  SpectrumManager

from PyQt4.QtCore import QRect, QSize, QSizeF
from PyQt4.QtGui import QApplication, QColor, QImage, QPainter, QPrinter
from PyQt4.QtSvg import QSvgGenerator

class BDianaError(Exception):
    pass

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
        self.renderHints = QPainter.RenderHints()
    
    def setup(self, setup_path):
    
        """Parses the setup file specified by setup_path, returning True if
        successful or False if unsuccessful.
        """

        # There must already be a running QApplication for this to work.
        if not QApplication.instance():
            self.application = QApplication([])
        
        if not LocalSetupParser.parse(setup_path):
            return False
        
        self.controller = Controller()
        if not self.controller.parseSetup():
            return False

        return True
    
    def addField(self, name, file_name, format = "netcdf", clear = False, top = False):
    
        line = "m=%s t=fimex f=%s format=%s" % (name, file_name, format)
        
        fm = self.controller.getFieldManager()
        errors = []
        if not fm.updateFileSetup([line], errors, clear, top):
            return errors
    
    def getFieldModels(self):
    
        """Returns a list of objects describing the model groups and the
        models contained within them."""

        return self.controller.initFieldDialog()
    
    def getModels(self):
    
        models = set()
        for group in self.getFieldModels():
            for model in group.modelNames:
                models.add(model)

        return models
    
    def getFields(self, model):

        fields = set()
        model, refTime, fieldGroups = self.controller.getFieldGroups(model, False)
        
        for group in fieldGroups:
            for field in group.fieldNames:
                fields.add(field)
        
        return fields
    
    def getFieldTimes(self, model, field):
    
        req = FieldRequest()
        req.modelName = model
        req.paramName = field
        return self.controller.getFieldTime([req])
    
    def prepare(self, input_file, archive = False):
    
        """Prepares input from the specified input_file for plotting.
        """
        #self.controller.getFieldManager().updateSources()
        self.controller.archiveMode(archive)
        self.controller.keepCurrentArea(False)
        
        dt = datetime.now()
        self.controller.setPlotTime(dt)
        
        self.controller.plotCommands(input_file.read_plot_commands())
    
    def setPlotCommands(self, plot_commands):
    
        inp = InputFile()
        inp.lines = ["PLOT"] + plot_commands + ["ENDPLOT"]
        self.prepare(inp)
    
    def getPlotTimes(self):

        """Returns a list of available plot times for the currently selected
        input file.
        """
        times = []

        for plot_type, t in self.controller.getPlotTimes().items():
            times += t

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
    
    def _plot(self, width, height, paint_device, plot_object, plot_method):
    
        plot_object.setPlotWindow(width, height)
        
        wrapper = PaintGL()
        context = PaintGLContext()
        context.makeCurrent()
        
        painter = QPainter()
        painter.begin(paint_device)
        painter.setRenderHints(self.renderHints)
        context.begin(painter)
        context.viewport = QRect(0, 0, width, height)

        value = plot_method()
        transform = context.transform
        
        context.end()
        painter.end()

        return paint_device, value, transform
    
    def plotImage(self, width, height, image_format = QImage.Format_ARGB32_Premultiplied):
    
        """Plots the data specified in the current input file as an image with
        the specified width and height, and with an optionally specified image
        format.
        """
        image = QImage(width, height, image_format)
        image.fill(QColor(0, 0, 0, 0))
        return self._plot(width, height, image, self.controller, self.controller.plot)[0]
    
    def plotPDF(self, width, height, output_file):

        """Plots the data specified in the current input file as a page in a
        PDF file with the given width and height, writing the output to the
        specified output file.
        """
        pdf = QPrinter()
        pdf.setOutputFormat(QPrinter.PdfFormat)
        pdf.setOutputFileName(output_file)
        pdf.setPaperSize(QSizeF(width, height), QPrinter.DevicePixel)
        pdf.setFullPage(True)
        return self._plot(width, height, pdf, self.controller, self.controller.plot)[0]
    
    def plotSVG(self, width, height, output_file):

        """Plots the data specified in the current input file as a page in a
        PDF file with the given width and height, writing the output to the
        specified output file.
        """
        printer = QPrinter()
        svg = QSvgGenerator()
        svg.setFileName(output_file)
        svg.setSize(QSize(width, height))
        svg.setViewBox(QRect(0, 0, width, height))
        svg.setResolution(printer.resolution())
        return self._plot(width, height, svg, self.controller, self.controller.plot)[0]
    
    def plotAnnotationImages(self, width, height, image_format = QImage.Format_ARGB32_Premultiplied):
    
        """Plots the annotations for the product specified in the current input
        file on an image with the specified width and height, and optionally
        specified image format. Each annotation image is yielded by this
        generator method.
        """
        image = QImage(width, height, image_format)
        image, rectangles, annotationTransform = self._plot(width, height, image,
                                        self.controller, self.controller.plotAnnotations)
        
        for rectangle in rectangles:
            sr = QRect(rectangle.x1, rectangle.y1, rectangle.width(), rectangle.height())
            dr = annotationTransform.mapRect(sr)
            yield image.copy(dr)

    def getAnnotations(self):
    
        """Returns the annotations for the product specified.
        """
        annotations = []

        for plot in self.controller.getAnnotations():
        
            for ann in plot.getAnnotations():
            
                annotation = {}
                for text in ann.vstr:
                
                    while text:

                        key, text = self._parse_key(text)
                        if text == "":
                            # No key=value pair.
                            annotation["title"] = key
                            continue
                        
                        value, text = self._parse_value(text)
                        if key == "table":
                            value = self._parse_table(value)
                        elif "colour" in key:
                            value = Colour(value)

                        annotation[key] = value

                annotations.append(annotation)
        
        return annotations

    def _parse_key(self, text):

        key = ""
        for i in range(len(text)):
            c = text[i]
            if c != "=":
                key += c
            else:
                return key, text[i+1:]
        
        return key, ""

    def _parse_value(self, text):

        value = ""
        in_string = False
        for i in range(len(text)):
            c = text[i]
            if c == '"':
                in_string = not in_string
            elif c == ",":
                if in_string:
                    value += c
                else:
                    return value, text[i+1:]
            else:
                value += c

        return value, ""

    def _parse_table(self, text):

        pieces = text.split(";")
        title = pieces.pop(0)
        rows = []
        for i in range(0, len(pieces), 3):
            rows.append((Colour(pieces[i]), pieces[i+2]))

        return {"title": title, "rows": rows}

    def prepareSpectrum(self, input_file, as_field = False):
    
        """Prepares input from the specified input_file for plotting.
        """
        self.spectrumManager = SpectrumManager()
        commands = input_file.read_spectrum_commands()
        options = self.spectrumManager.getOptions()
        options.readOptions(commands)
        models, observations, station = input_file.parse_spectrum_commands(commands)
        self.spectrumManager.setSelectedModels(models, observations, as_field)
        self.spectrumManager.setModel()
        self.spectrumManager.setStation(station)
    
    def getSpectrumTime(self):

        return self.spectrumManager.getTime()

    def setSpectrumTime(self, spectrum_time):

        self.spectrumManager(spectrum_time)

    def plotSpectrum(self, width, height, image_format = QImage.Format_ARGB32_Premultiplied):
    
        """Plots the wave spectrum for the product specified in the current input
        file on an image with the specified width and height, and optionally
        specified image format.
        """
        image, success, transform = self._plot(width, height, image_format,
                                               self.spectrumManager, self.spectrumManager.plot)

        return image


class InputFile:

    """Represents an input file for use with a BDiana instance."""

    def __init__(self, input_path = None):
    
        if input_path is not None:
            self.read(input_path)
        else:
            self.lines = []
            self.parameters = {}
    
    def read(self, input_path):
    
        self.lines = open(input_path).readlines()
        self.parameters = self.read_input_parameters()
    
    def fromString(self, text):

        self.lines = text.split("\n")
        self.parameters = self.read_input_parameters()

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
    
    def read_input_parameters(self):
    
        d = {}
        
        for line in self.lines:
        
            at = line.find("#")
            
            if at != -1:
               line = line[:at]

            line = line.strip()
            if line.startswith("PLOT"):
                break
            
            pieces = line.split("=")
            if len(pieces) > 1:
                key, value = pieces[0], "=".join(pieces[1:])
                d[key.strip()] = value.strip()
        
        return d
    
    def read_commands(self, start, end):
    
        lines = []
        in_section = False
        for line in self.lines:

            at = line.find("#")
            if at != -1:
                line = line[:at]

            if line.strip().startswith("#"):
                continue
            elif line.strip().lower() == start.lower():
                in_section = True
            elif line.strip().lower() == end.lower():
                in_section = False
            elif in_section and line.strip():
                lines.append(line)
        
        return lines
    
    def read_plot_commands(self):
    
        return self.read_commands("plot", "endplot")
    
    def read_spectrum_commands(self):
    
        return self.read_commands("spectrum.plot", "endplot")

    def parse_spectrum_commands(self, commands):

        observations = False
        station = None
        models = []

        for command in commands:
        
            command = command.strip()
            if command.lower() == "observation.on":
                observations = True
            elif command.lower() == "observation.off":
                observations = False
            else:
                pieces = command.split("=")
                key, value = "".join(pieces[:1]), " ".join(pieces[1:])
                
                key = key.strip().lower()
                if key == "station":
                    station = value.strip().replace('"', '')
                elif key == "model" or key == "models":
                    models.append(value.strip())

        return models, observations, station
