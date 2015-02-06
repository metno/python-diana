#!/usr/bin/env python

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

import cgi, datetime, os, sys, urlparse
import pyproj

from metno import bdiana, plotcommands

Projection = '+proj=merc +lon_0=0w +datum=WGS84 +units=m'

class Tile:

    """Handles requests for tiles."""

    def process(self, argument):
    
        zoom, x, y_ext = argument.split("/")
        y, suffix = y_ext.split(".")
        zoom, x, y = int(zoom), int(x), int(y)
        if not 0 <= zoom <= 15:
            raise ValueError
        if not 0 <= x < 2**zoom:
            raise ValueError
        if not 0 <= y < 2**zoom:
            raise ValueError
    
        file_path = self.tile(zoom, x, y)
        return open(file_path, "rb").read()
    
    def tile(self, zoom, x, y):
    
        try:
            os.mkdir("tiles")
        except OSError:
            pass
        
        zoom_path = os.path.join("tiles", str(zoom))
        try:
            os.mkdir(zoom_path)
        except OSError:
            pass
        
        x_path = os.path.join(zoom_path, str(x))
        try:
            os.mkdir(x_path)
        except OSError:
            pass
        
        output_file = os.path.join(x_path, "%i.png" % y)
        if os.path.exists(output_file):
            return output_file
        
        lat1, lon1 = num2deg(x, y + 1, zoom)
        lat2, lon2 = num2deg(x + 1, y, zoom)
        
        p = pyproj.Proj(proj = "merc", datum = "WGS84")
        x1, y1 = p(lon1, lat1)
        x2, y2 = p(lon2, lat2)
        
        if not hasattr(self, "api"):
            self.api = bdiana.BDiana()
            if not self.api.setup():
                raise ValueError
        
        a = plotcommands.Area(proj4string = Projection,
                              rectangle = [x1, x2, y1, y2])
        
        m = plotcommands.Map()
        m.setOption("map", "Gshhs-Auto")
        m.setOption("backcolour", "white")
        m.setOption("land", "on")
        m.setOption("land.colour", "flesh")
        
        self.api.setPlotCommands([m.text(), a.text()])
        self.api.setPlotTime(datetime.datetime.now())
        self.api.plotImage(256, 256).save(output_file)

        return output_file

# From https://wiki.openstreetmap.org/wiki/Slippy_map_filenames#Python

# Lon./lat. to tile numbers

import math
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

# Tile numbers to lon./lat.

import math
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

class Handler(SimpleHTTPRequestHandler):

    def __init__(self, *args):
    
        self.tile = Tile()
        SimpleHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
    
        if self.path.count("/") == 3:
            argument = self.path[self.path.find("/") + 1:]
            try:
                data = self.tile.process(argument)
                self.send_response(200, "OK")
                self.send_header("Content-Type", 'image/png')
                self.end_headers()
                self.wfile.write(data)
            except ValueError:
                self.send_error(404, "Not found")
        else:
            self.send_error(404, "Not found")

if __name__ == "__main__":

    server = HTTPServer(('', 8000), Handler)
    server.serve_forever()
