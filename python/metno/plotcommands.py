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

    hidden = []

    def __init__(self, **kwargs):

        self.options = {}
        self.order = []
        
        for key, value in kwargs.items():
            self.setOption(key, value)

    def _add_command(self, option, value):

        if option not in self.options:
            self.order.append(option)
        
        self.options[option] = value
    
    def getOptions(self):

        return self.available.keys()

    def getAvailable(self, option):
    
        a = self.available.get(option)
        if isinstance(a, ChoiceValue):
            return a.choices
        else:
            return a
    
    def setOption(self, option, value = None):
    
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

    command = "FIELD"

    available = {"model": AnyValue,
                 "plot": AnyValue,
                 "plottype": ("contour", "contour2", "value", "symbol",
                              "alpha_shade", "alarm_box", "fill_cell", "wind",
                              "wind_temp_fl", "wind_value", "vector", "frame",
                              "direction"),
                 "antialiasing": BooleanValue,
                 "frame": (0, 1, 2, 3)}


class Map(PlotCommand):

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

    command = "OBS"

    available = {"data": ("Synop", "Metar", "List", "Pressure", "Ocean",
                          "Tide"),
                 "plot": ("Synop", "Metar", "List", "Pressure", "Ocean",
                          "Tide"),
                 "parameter": ChoiceValue("data",
                     {"Synop": ("Wind", "TTT", "TdTdTd", "PPPP", "ppp", "a",
                                "h", "VV", "N", "RRR", "ww", "W1", "W2", "Nh",
                                "Cl", "Cm", "Ch", "vs", "ds", "TwTwTw",
                                "PwaHwa", "dw1dw1", "Pw1Hw1", "TxTn", "sss",
                                "911ff", "s", "fxfx", "Id", "St.no(3)",
                                "St.no(5)", "Time"),
                      "Metar": ("Wind", "dndx", "fmfm", "TTT", "TdTdTd", "ww",
                                "REww", "VVVV/Dv", "VxVxVxVx/Dvx", "Clouds",
                                "PHPHPHPH", "Id"),
                      "List": ("Pos", "dd", "ff", "T_red", "Date", "Time",
                               "Height", "Zone", "Name", "RRR_1", "RRR_6",
                               "RRR_12", "RRR_24", "quality"),
                      "Pressure": ("Pos", "Wind", "dd", "ff", "TTT", "TdTdTd",
                                   "PPPP", "Id", "Date", "Time", "HHH", "QI",
                                   "QI_NM", "QI_RFF"),
                      "Ocean": ("Id", "PwaPwa", "HwaHwa", "depth", "TTTT",
                                "SSSS", "Date", "Time"),
                      "Tide": ("Pos", "TE", "Id", "Date", "Time")},
                      multiple = True
                      ),
                 "density": FloatValue,
                 "antialiasing": BooleanValue}

    def setOption(self, option, value = None):
    
        if option == "density" and str(value).startswith("all"):
            self._add_command(option, value)
        else:
            PlotCommand.setOption(self, option, value)


class Satellite(PlotCommand):

    command = "SAT"

    available = {"product": AnyValue,
                 "subproduct": AnyValue,
                 "channel": AnyValue,
                 "alpha": FloatValue,
                 "mosaic": (0, 1)}
    
    hidden = ["product", "subproduct", "channel"]


class Radar(Satellite):
    pass
