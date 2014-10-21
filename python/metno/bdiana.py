
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

"""The bdiana module provides a class that can be used to access plotting
functionality of the Diana meteorological visualisation tool.
"""

from datetime import datetime
import os, sys

from metlibs import FieldRequest, milogger
from diana import Colour, Controller, LocalSetupParser, ObsPlot, PaintGL, \
                  PaintGLContext, PlotModule, SpectrumManager

from metno.versions import diana_version, python_diana_version

from PyQt4.QtCore import QRect, QSize, QSizeF
from PyQt4.QtGui import QApplication, QColor, QImage, QPainter, QPicture, QPrinter
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
    produced by calling the plotImage() method with the desired width and
    height values, measured in pixels. Alternatively, the plotPDF() and
    plotSVG() methods can be used to create PDF and SVG files respectively.
    """

    def __init__(self, log_level = 2, file_name = "", object_name = ""):
    
        """Creates a BDiana instance, optionally specifying the level of
        logging to be used, the file to use for logging output, and the name
        to use for the instance in the log.
        """

        self.logHandler = milogger.LogHandler.initLogHandler(log_level, file_name)
        self.logHandler.setObjectName(object_name or sys.argv[0])

        self.controller = None
        self.spectrumManager = None
        self.renderHints = QPainter.RenderHints()
    
    def default_setup_file(self):

        return "/etc/diana/%s/diana.setup-COMMON" % diana_version

    def setup(self, setup_path = None):
    
        """Parses the setup file specified by setup_path, returning True if
        successful or False if unsuccessful.
        """
        
        # There must already be a running QApplication for this to work.
        if not QApplication.instance():
            self.application = QApplication([])
        
        if not setup_path:
            setup_path = self.default_setup_file()

        if not LocalSetupParser.parse(setup_path):
            return False
        
        self.controller = Controller()
        if not self.controller.parseSetup():
            return False

        self.spectrumManager = SpectrumManager()
        return True
    
    def addModel(self, name, file_name, format = "netcdf", clear = False, top = False):
    
        """Adds a new model to Diana's collection, registering it with the given name.
        Model information is loaded from the file specified by file_name which is, by
        default, understood to be in NetCDF format. Use the format keyword argument
        to specify an alternative file format.
        
        The clear keyword argument is used to clear the list of models registered with
        Diana. The top keyword argument is used to place the new model at the top of
        the list of models when shown in Diana's field dialog."""
        
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
    
        """Returns a set of available models."""

        models = set()
        for group in self.getFieldModels():
            for model in group.modelNames:
                models.add(model)

        return models
    
    def getFields(self, model):

        """Returns the available fields for the given model.
        Models can be obtained using the getModels() method."""
        
        fields = set()

        # Find the reference times first.
        refTimes = self.controller.getFieldReferenceTimes(model)
        if not refTimes:
            return fields
        
        refTimes = list(refTimes)
        refTimes.sort()

        model, fieldGroups = self.controller.getFieldGroups(model, refTimes[-1], False)
        
        for group in fieldGroups:
            for field in group.fieldNames:
                fields.add(field)
        
        return fields
    
    def getFieldTimes(self, model, field):
    
        """Returns the available times for the given model and field.
        Models and fields can be obtained using the getModels() and getFields() methods."""

        req = FieldRequest()
        req.modelName = model
        req.paramName = field
        return self.controller.getFieldTime([req])
    
    def getObsTypes(self):
    
        """Returns the available observation types."""

        obs_manager = self.controller.getObservationManager()
        return map(lambda p: p.dialogName, obs_manager.getProductsInfo().values())
    
    def getObsParameters(self, type):

        """Returns the available parameters for the given observation type."""

        obs_manager = self.controller.getObservationManager()
        info = obs_manager.getProductsInfo()

        for product in info.values():
            if product.dialogName == type:
                return product.parameter

        return []
    
    def getObsTimes(self, type):
    
        """Returns the available times for the given type of observation.
        Acceptable types can be found by calling getObsTypes() and include
        Synop, Metar, Pressure, Ocean and Tide."""

        obs_manager = self.controller.getObservationManager()
        return obs_manager.getObsTimes(["OBS data=" + type])
    
    def getObsPositions(self, type, time):
    
        """Returns an object containing information about the positions of
        observations of the given type for the specified time."""

        obs_manager = self.controller.getObservationManager()
        op = obs_manager.createObsPlot("OBS data=" + type + " devfield=true")
        obs_manager.prepare(op, time)
        obs_manager.updateObsPositions([op])
        return obs_manager.getObsPositions()

    def getSatProducts(self):
    
        """Returns the available satellite and radar products as a dictionary
        of products, each of which contains a dictionary of subproducts."""
        
        sat_manager = self.controller.getSatelliteManager()
        return sat_manager.getProductsInfo()
    
    def getSatTimes(self, product, subproduct):
    
        """Returns the available times for the given satellite/radar product
        and subproduct."""

        sat_manager = self.controller.getSatelliteManager()
        sat_manager.prepareSat(["SAT " + product + " " + subproduct])
        return sat_manager.getSatTimes()

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
    
        """Sets a list of plot commands to be used for plotting. These are
        defined in the plotcommands module.

        A call to this method must be followed by a call to setPlotTime() with
        an appropriate time."""

        inp = InputFile()
        inp.lines = ["PLOT"] + map(str, plot_commands) + ["ENDPLOT"]
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
    
        """Returns the plot area that will be displayed in the plot."""

        return self.controller.getMapArea()
    
    def getPlotSize(self):

        """Returns the exact rectangle that will be displayed in the plot.
        Note that this may be different to the rectangle supplied by getPlotArea()
        since Diana adjusts the plot extent to preserve the aspect ratio of the
        map data."""

        return PlotModule.instance().getPlotSize()
    
    def getLatLonFromXY(self, cx, cy):
    
        """Returns the latitude and longitude of a point in the current plot
        specified by the point (cx, cy) where cx and cy are size-independent
        horizontal and vertical coordinates measured from the bottom-left
        corner of the plot. The values of cx and cy must be in the range
        [0.0, 1.0]."""

        area = self.getPlotArea()
        p = area.P()
        r = area.R()
        pr = pyproj.Proj(p.getProjDefinition())
        
        x = r.x1 + (r.x2 - r.x1) * cx
        y = r.y1 + (r.y2 - r.y1) * cy
        lon, lat = pr(x, y, inverse = True)
        return lat, lon
    
    def getXYFromLatLon(self, latitude, longitude):

        """Returns the size-independent coordinates of a point in the current
        plot that corresponds to the specified latitude and longitude, where a
        coordinate of (0.0, 0.0) corresponds to the bottom-left corner of the
        plot and (1.0, 1.0) corresponds to the top-right corner. The coordinate
        may contain values outside the range [0.0, 1.0] if the latitude and
        longitude specified do not lie within the current plot."""
        
        area = self.getPlotArea()
        p = area.P()
        r = area.R()
        pr = pyproj.Proj(p.getProjDefinition())

        x, y = pr(lon, lat)
        cx = (x - r.x1)/(r.x2 - r.x1)
        cy = (y - r.y1)/(r.y2 - r.y1)
        return cx, cy
    
    def _plot(self, width, height, paint_device, plot_object = None, plot_method = None):
    
        if not plot_object:
            plot_object = self.controller
        if not plot_method:
            plot_method = plot_object.plot

        plot_object.setPlotWindow(width, height)
        
        wrapper = PaintGL()
        context = PaintGLContext()
        context.makeCurrent()
        
        painter = QPainter()
        painter.begin(paint_device)
        painter.setRenderHints(self.renderHints)
        painter.setClipRect(QRect(0, 0, width, height))
        context.begin(painter)
        context.viewport = QRect(0, 0, width, height)

        value = plot_method()
        transform = context.transform
        
        context.end()
        painter.end()

        return paint_device, value, transform
    
    def plotImage(self, width, height, image_format = QImage.Format_ARGB32_Premultiplied,
                  _plotting_object = None):
    
        """Plots the data specified in the current input file as an image with
        the specified width and height, and with an optionally specified image
        format. Returns the image produced."""

        image = QImage(width, height, image_format)
        image.fill(QColor(0, 0, 0, 0))
        return self._plot(width, height, image, _plotting_object)[0]
    
    def plotPDF(self, width, height, output_file, units = "pixels", _plotting_object = None):

        """Plots the data specified in the current input file as a page in a
        PDF file with the given width and height, writing the output to the
        specified output file. The optional units argument specifies the units
        used to measure the plot size; by default, pixels are used, but "cm",
        "mm" and "in" are also acceptable.
        
        Returns the QPrinter object used to write the file."""

        pdf = QPrinter()
        pdf.setOutputFormat(QPrinter.PdfFormat)
        pdf.setOutputFileName(output_file)
        
        if units == "in":
            width = pdf.logicalDpiX() * width
            height = pdf.logicalDpiY() * height
        elif units == "cm":
            width = pdf.logicalDpiX() * (width / 2.54)
            height = pdf.logicalDpiY() * (height / 2.54)
        elif units == "mm":
            width = pdf.logicalDpiX() * (width / 25.4)
            height = pdf.logicalDpiY() * (height / 25.4)
        elif units != "pixels":
            raise BDianaError, "Unknown units specified to plotPDF: %s" % units

        pdf.setPaperSize(QSizeF(width, height), QPrinter.DevicePixel)
        pdf.setFullPage(True)
        return self._plot(width, height, pdf, _plotting_object)[0]
    
    def plotSVG(self, width, height, output_file, _plotting_object = None):

        """Plots the data specified in the current input file as a page in a
        PDF file with the given width and height, writing the output to the
        specified output file. Returns the SVG object produced."""

        printer = QPrinter()
        svg = QSvgGenerator()
        svg.setFileName(output_file)
        svg.setSize(QSize(width, height))
        svg.setViewBox(QRect(0, 0, width, height))
        svg.setResolution(printer.resolution())
        return self._plot(width, height, svg, _plotting_object)[0]
    
    def plotPicture(self, width, height, _plotting_object = None):
    
        """Plots a picture with the given width and height. Returns the
        picture object produced. Pictures can be used as intermediate
        output and combined to produce final products."""

        picture = QPicture()
        picture.setBoundingRect(QRect(0, 0, width, height))
        return self._plot(width, height, picture, _plotting_object)[0]

    def plotAnnotationImages(self, width, height, image_format = QImage.Format_ARGB32_Premultiplied):
    
        """Plots the annotations for the product specified in the current input
        file on an image with the specified width and height, and optionally
        specified image format. Each annotation image is yielded by this
        generator method."""

        image = QImage(width, height, image_format)
        image, rectangles, annotationTransform = self._plot(width, height, image,
                                        self.controller, self.controller.plotAnnotations)
        
        for rectangle in rectangles:
            sr = QRect(rectangle.x1, rectangle.y1, rectangle.width(), rectangle.height())
            dr = annotationTransform.mapRect(sr)
            yield image.copy(dr)

    def getAnnotations(self):
    
        """Returns a list of annotations for the product specified."""

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
    
    # Spectrum plot methods - perhaps these should be in a separate namespace

    def getSpectrumModels(self):
    
        """Returns the list of available wave spectrum models."""

        return self.spectrumManager.getModelNames()

    def setSpectrumModel(self, model, as_field = False):
    
        """Sets a single wave spectrum model to use."""

        self.setSpectrumModels([model], as_field)

    def setSpectrumModels(self, models, as_field = False):
    
        """Sets the wave spectrum models to use."""

        self.spectrumManager.setSelectedModels(models, as_field)
        self.spectrumManager.setModel()
    
    def getSpectrumStations(self):
    
        """Returns the list of stations for which spectrum data is available."""
        
        return self.spectrumManager.getStationList()

    def setSpectrumStation(self, station):
    
        """Sets the station for which spectrum data will be obtained."""

        self.spectrumManager.setStation(station)
    
    def getSpectrumTimes(self):
    
        """Returns the available times for which spectrum data is available."""

        return self.spectrumManager.getTimeList()

    def setSpectrumTime(self, spectrum_time):
    
        """Sets the spectrum time to use for the wave spectrum plot."""

        self.spectrumManager.setTime(spectrum_time)

    def plotSpectrumImage(self, width, height, image_format = QImage.Format_ARGB32_Premultiplied):
    
        """Plots the wave spectrum for the currently selected models and station
        on an image with the specified width and height, and optionally specified
        image format.
        """

        return self.plotImage(width, height, image_format, self.spectrumManager)

    def plotSpectrumPDF(self, width, height, output_file):
    
        """Plots the wave spectrum for the currently selected models and station
        as a page in a PDF file with the given width and height, writing the output
        to the specified output file."""

        return self.plotPDF(width, height, output_file, self.spectrumManager)


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
