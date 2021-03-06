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
from PyQt4.QtGui import QApplication
from metno.bdiana import BDiana, InputFile

if __name__ == "__main__":

    if not 2 <= len(sys.argv) <= 3:
    
        sys.stderr.write("Usage: %s [setup file] <input file>\n" % sys.argv[0])
        sys.stderr.write("Writes images for legends described by the input file with names\n"
                         "legend0.png, legend1.png, ...\n")
        sys.exit(1)
    
    elif len(sys.argv) == 2:
    
        setup_path = "/etc/diana/diana.setup-COMMON"
        input_path = sys.argv[1]
    
    else:
        setup_path = sys.argv[1]
        input_path = sys.argv[2]
    
    app = QApplication(sys.argv)
    bdiana = BDiana()
    
    if not bdiana.setup(setup_path):
        print "Failed to parse", setup_path
        sys.exit(1)
    
    input_file = InputFile(input_path)
    bdiana.prepare(input_file)
    
    times = bdiana.getPlotTimes()
    if times:
        bdiana.setPlotTime(times[-1])
    else:
        bdiana.setPlotTime(datetime.datetime.now())

    width, height = input_file.getBufferSize()
    
    i = 0
    for legend_image in bdiana.plotAnnotationImages(width, height):
        print "Saving legend%i.png" % i
        legend_image.save("legend%i.png" % i)
        i += 1
    
    sys.exit()

