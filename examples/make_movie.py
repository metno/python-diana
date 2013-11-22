#!/usr/bin/env python

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

import datetime, sys
from metno.bdiana import BDiana, InputFile
from metno.diana import MovieMaker

if __name__ == "__main__":

    if not 2 <= len(sys.argv) <= 3:
    
        sys.stderr.write("Usage: %s [setup file] <input file>\n" % sys.argv[0])
        sys.exit(1)
    
    b = BDiana()
    
    if len(sys.argv) == 2:
        setup_path = b.default_setup_file()
        input_path = sys.argv[1]
    else:
        setup_path = sys.argv[1]
        input_path = sys.argv[2]
    
    if not b.setup(setup_path):
        print "Failed to parse", setup_path
        sys.exit(1)
    
    input_file = InputFile(input_path)
    width, height = input_file.getBufferSize()
    b.prepare(input_file)
    
    times = b.getPlotTimes()
    if not times:
        sys.stderr.write("No times found for the specified plot description.\n")
    
    try:
        frameDelay = float(input_file.parameters["frameDelay"])
    except (KeyError, ValueError):
        frameDelay = 0.5

    print "Saving temp.avi"
    movie = MovieMaker("temp.avi", "avi", frameDelay);
    for time in times:
    
        print "Plotting", time
        b.setPlotTime(time)
        image = b.plotImage(width, height)
        movie.addImage(image)

    sys.exit()

