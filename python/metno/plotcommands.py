# -*- coding: utf8 -*-

# python-diana - Python API for Diana - A Free Meteorological Visualisation Tool
#
# Copyright (C) 2013 met.no
#
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# email: diana@met.no
#
# This file is part of python-diana
#
# python-diana is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# python-diana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-diana; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

### TODO: Obtain available options by parsing the relevant sections in a
### specified input file.

"""The plotcommands module contains plot command classes that are used to
describe details of a Diana plot.

Instances of each class are used with the BDiana class (see the bdiana
module) where they are passed in a list to the setPlotCommands() method.
"""

class ValueType:
    pass

class NoValue(ValueType):
    def validate(self, value):
        return None

class AnyValue(ValueType):
    def validate(self, value):
        return value

class FloatValue(ValueType):
    def validate(self, value):
        return float(value)

class QuotedValue(ValueType):
    def validate(self, value):
        return '"' + str(value) + '"'

class RectangleValue(ValueType):
    def validate(self, value):
        return ":".join(map(str, value))

class BooleanValue(ValueType):
    def validate(self, value):
        if value == True:
            return "true"
        else:
            return "false"

class ListValue(ValueType):
    def validate(self, value):
        return ",".join(map(str, value))

class ChoiceValue(ValueType):

    """Specifies an option that accepts one or more values based on the value
    of another, previously defined option.
    """

    def __init__(self, field_name, choices, multiple = False, delimiter = ","):
    
        # The field name defines the option in the plot command that contains
        # the section to use to verify this option value.
        self.field_name = field_name
        self.choices = choices
        self.multiple = multiple
        self.delimiter = delimiter
    
    def validate(self, section, value):

        if not self.multiple:
            values = [value]
        values = []
        for item in value:
            try:
                if item in self.choices[section]:
                    values.append(item)
                    if not self.multiple:
                        break
            except KeyError:
                raise ValueError, "'%s' not an appropriate value for '%s'." % (value, section)
        
        return self.delimiter.join(values)


class PlotCommand:

    """Defines a generic plot command and contains functionality common to all
    PlotCommand subclasses."""
    
    hidden = []

    def __init__(self, **kwargs):

        self.options = {}
        self.order = []
        
        for key, value in kwargs.items():
            self.setOption(key, value)
    
    def __str__(self):
        return self.text()

    def _add_command(self, option, value):

        if option not in self.options:
            self.order.append(option)
        
        self.options[option] = value
    
    def getOptions(self):
    
        """Returns a list of available options for the plot command."""
        return self.available.keys()

    def getAvailable(self, option):
    
        """Returns a list of values that can be used with the specified option."""
        a = self.available.get(option)
        if isinstance(a, ChoiceValue):
            return a.choices
        else:
            return a
    
    def setOption(self, option, value = None):
    
        """Sets the option to the specified value."""
        
        Available = self.available.get(option, AnyValue)
        
        # If the available value type is described by a value type class then
        # instantiate it and ask it to validate the value.
        if type(Available) == type(ValueType) and issubclass(Available, ValueType):
            Available = Available()

        if isinstance(Available, ChoiceValue):
            # Read the value of the option that this option depends on and
            # pass that as the section to use to verify the value supplied.
            self._add_command(option, Available.validate(self.options[Available.field_name], value))
        elif isinstance(Available, ValueType):
            self._add_command(option, Available.validate(value))
        # Otherwise, the value must be in the sequence found.
        elif Available and value in Available:
            self._add_command(option, value)

    def text(self):
    
        """Returns a textual representation of the option for use in an input
        file."""
        
        pieces = [self.command]
        for option in self.order:
            if self.available.get(option) != NoValue:
                if option in self.hidden:
                    pieces.append(str(self.options[option]))
                else:
                    pieces.append(option + "=" + str(self.options[option]))
            else:
                pieces.append(option)

        return " ".join(pieces)


class Field(PlotCommand):

    """The Field plot command describes how fields are represented in a Diana
    plot.
    
    Common options include model (the name of the model to use), plot (the
    parameter or predefined plot to show), plottype (contour, wind, vector,
    etc.) and frame (whether to show a frame around the model area).
    """
    
    command = "FIELD"

    available = {"model": AnyValue,
                 "plot": AnyValue,
                 "plottype": ("contour", "contour2", "value", "symbol",
                              "alpha_shade", "alarm_box", "fill_cell", "wind",
                              "wind_temp_fl", "wind_value", "vector", "frame",
                              "direction"),
                 "antialiasing": BooleanValue,
                 "frame": (0, 1, 2, 3),
                 "line.values": ListValue}


class Map(PlotCommand):

    """The Map plot command describes the background map that is used in a
    Diana plot.
    
    Common options for the map include backcolour (background colour), map (map
    dataset), land (whether the land areas are filled) and land.colour (the
    colour to use)."""
    
    command = "MAP"

    available = {"backcolour": AnyValue,
                 "map": ("Gshhs-Auto", "Euro1", "Euro2", "Euro3", "Fin",
                         "Norkart", "Norkart2", "Regioner", "Banker",
                         "Banker1", "Banker2", "Banker_test", "MinQNH",
                         "FIR", "High.Seas", "skredvarsling", "NVE_flom",
                         "Europa-TVkart", "Wvs-Auto", "Kommuner", "Fylker",
                         "Riksgrense", "Kyst", "Høyde", "Vann", "Vei",
                         "Vei2", "Vei3", "Bane", "World", "Gebco.world",
                         "Vanlig", "Norsea", "Simra_fly", "Flystriper",
                         "Approach-area"),
                 "land": ("on", "off"),
                 "land.colour": AnyValue}


class Area(PlotCommand):

    """The Area plot command describes the geographic area to include in the
    Diana plot.
    
    Common options include name (a predefined area name), proj4string (a
    description of the projection to use) and rectangle (the size of the
    projected region to show, measured in projection units).
    """
    
    command = "AREA"
    
    available = {"name": ("Europa", "Norge", "Trøndelag", "N-Norge",
                          "S-Norge", "Norge.20W", "VA-Norge", "VV-Norge",
                          "VNN-Norge", "Atlant", "SIGkart", "NyttSigkart4",
                          "SWIkart", "N.halvkule", "S.halvkule",
                          "S.halvkule+180", "N.halvkule-90", "N.halvkule+90",
                          "Hirlam-grid", "Merkator", "Geografisk", "Globalt",
                          "Infosat.1", "Analyse_min", "ENHF", "ENST", "ENHV",
                          "ENNK", "Norge.smal", "Ishav", "N-Europa",
                          "N.halvkule+65", "Troms", "H10-stor", "H10-liten",
                          "Skandinavia", "proj_hirlam", "proj_bonne",
                          "proj_van_der_grinten", "proj_eqc", "proj_obtran",
                          "proj_lambert", "EPSG-4326", "EPSG-32661",
                          "EPSG-32761", "epsg:900913", "epsg:3575"),
                 "proj4string": QuotedValue,
                 "rectangle": RectangleValue}


class Label(PlotCommand):

    """The Label plot command describes a decorative label in a Diana plot.
    
    Common options include data (which is used on its own to show the source
    of field data), text (for user-defined strings), font (the font family to
    use), halign and valign (for horizontal and vertical alignment).
    """
    
    command = "LABEL"

    available = {"data": NoValue,
                 "text": AnyValue,
                 "tcolour": AnyValue,
                 "bcolour": AnyValue,
                 "fcolour": AnyValue,
                 "anno": AnyValue,
                 "halign": ("left", "right", "center"),
                 "valign": ("top", "bottom", "center"),
                 "xoffset": FloatValue,
                 "yoffset": FloatValue,
                 "xratio": FloatValue,
                 "yratio": FloatValue,
                 "polystyle": ("fill", "border", "both", "none"),
                 "margin": FloatValue,
                 "font": AnyValue,
                 "fontname": AnyValue,
                 "fontface": AnyValue,
                 "fontsize": AnyValue,
                 "yclinewidth": AnyValue,
                 "plotrequested": BooleanValue}


class Observations(PlotCommand):

    """The Observations plot command describes a collection of observations
    in a Diana plot.
    
    Common options include data and plot (the type of observations to show),
    parameter (a comma-separated list of observation parameters) and density
    (how many observations to show in a given plot area).
    """
    
    command = "OBS"

    available = {"data": ("Synop", "Metar", "List", "Pressure", "Ocean",
                          "Tide"),
                 "plot": ("Synop", "Metar", "List", "Pressure", "Ocean",
                          "Tide"),
                 "parameter": ListValue, # use BDiana.getObsParameters()
                 "density": FloatValue,
                 "antialiasing": BooleanValue}

    def setOption(self, option, value = None):
    
        """Sets the option to the specified value."""
        if option == "density" and str(value).startswith("all"):
            self._add_command(option, value)
        else:
            PlotCommand.setOption(self, option, value)


class Satellite(PlotCommand):

    """The Satellite plot command describes satellite data in a Diana plot.
    
    Common options include product, subproduct, channel (describing the
    source and type of data), alpha (allowing the data to be shown as a
    partially-transparent image) and mosaic (which combines multiple images
    to cover larger map areas).
    """
    
    command = "SAT"

    available = {"product": AnyValue,
                 "subproduct": AnyValue,
                 "channel": AnyValue,
                 "alpha": FloatValue,
                 "mosaic": (0, 1)}
    
    hidden = ["product", "subproduct", "channel"]


class Radar(Satellite):

    """The Radar plot command is an alias of the Satellite plot command, and
    is used for convenience and improved readability in programs that handle
    radar data.
    """
    pass


class Drawing(PlotCommand):

    """The Drawing plot command describes a collection of symbols, text,
    polylines and other objects that are used to annotate a plot.
    """

    command = "DRAWING"

    available = {"file": QuotedValue}
