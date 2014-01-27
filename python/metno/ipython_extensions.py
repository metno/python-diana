
# python-diana - Python API for Diana - A Free Meteorological Visualisation Tool
#
# Copyright (C) 2012 met.no
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

from PyQt4.QtCore import QBuffer
from PyQt4.QtGui import QImage, QImageWriter, QPainter, QPicture
from IPython.core.display import Image

def embed(im):

    """Converts a QImage or QPicture object into an ipython Image object for
    embedding into an ipython notebook.
    """

    if isinstance(im, QPicture):
        pic = im
        im = QImage(im.width(), im.height(), QImage.Format_ARGB32_Premultiplied)
        p = QPainter()
        p.begin(im)
        p.drawPicture(0, 0, pic)
        p.end()

    w = QImageWriter()
    buf = QBuffer()
    buf.open(buf.WriteOnly)
    w.setFormat("png")
    w.setDevice(buf)
    w.write(im)
    return Image(data=str(buf.buffer()), format="png", embed=True)
