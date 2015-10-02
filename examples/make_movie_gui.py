#!/usr/bin/env python

# Copyright (C) 2015 met.no
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

import datetime, os, sys

from PyQt4.QtCore import Qt, QTimer
from PyQt4.QtGui import *

from metno.bdiana import BDiana, InputFile
from metno.diana import MovieMaker

class Window(QWidget):

    def __init__(self, setup_file, input_file, output_file):
    
        QWidget.__init__(self)

        self.bdiana = BDiana()
        if not setup_file:
            self.setup_file = self.bdiana.default_setup_file()
        else:
            self.setup_file = str(setup_file)

        self.input_file = str(input_file)
        self.output_file = str(output_file)
        
        self.statusLine = QLabel()
        self.progressBar = QProgressBar()
        self.cancelButton = QPushButton(self.tr("Cancel"))
        self.cancelButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        self.cancelButton.clicked.connect(qApp.quit)

        layout = QVBoxLayout(self)
        layout.addWidget(self.statusLine)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.cancelButton)
        
        self.setWindowTitle(self.tr("Diana Video Export"))
        QTimer.singleShot(0, self.run)
    
    def run(self):
    
        if not self.bdiana.setup(self.setup_file):
            self.statusLine.setText(self.tr("Failed to read Diana setup file '%1' for video export.").arg(self.setup_file))
            return
        
        input_file = InputFile(self.input_file)
        self.image_width, self.image_height = input_file.getBufferSize()
        self.bdiana.prepare(input_file)
        
        self.times = self.bdiana.getPlotTimes()
        if not self.times:
            self.statusLine.setText(self.tr("No times found for the plot."))
            return
        
        try:
            frameDelay = float(input_file.parameters["frameDelay"])
        except (KeyError, ValueError):
            frameDelay = 0.5
        
        file_suffix = os.path.splitext(self.output_file)[1]
        file_type = file_suffix.lstrip(os.extsep)
        self.movie = MovieMaker(self.output_file, file_type, frameDelay)

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(self.times))
        self.progressBar.setValue(0)

        self.frame = 0
        self.statusLine.setText(self.tr("Exporting '%1'...").arg(self.output_file))

        QTimer.singleShot(0, self.addFrame)
    
    def addFrame(self):

        self.bdiana.setPlotTime(self.times[self.frame])
        image = self.bdiana.plotImage(self.image_width, self.image_height)
        self.movie.addImage(image)
        self.frame += 1
        self.progressBar.setValue(self.frame)
        
        if self.frame < len(self.times):
            QTimer.singleShot(0, self.addFrame)
        else:
            self.statusLine.setText(self.tr("Finished exporting '%1'.").arg(self.output_file))


if __name__ == "__main__":

    app = QApplication(sys.argv)

    if not 3 <= len(app.arguments()) <= 4:
    
        sys.stderr.write("Usage: %s [setup file] <input file> <movie file>\n" % sys.argv[0])
        sys.exit(1)
    
    if len(app.arguments()) == 3:
        setup_file = None
        input_file = app.arguments()[1]
        movie_file = app.arguments()[2]
    else:
        setup_file = app.arguments()[1]
        input_file = app.arguments()[2]
        movie_file = app.arguments()[3]
    
    window = Window(setup_file, input_file, movie_file)
    window.show()
    
    sys.exit(app.exec_())

