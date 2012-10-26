/*
 python-diana - Python API for Diana - A Free Meteorological Visualisation Tool

 Copyright (C) 2012 met.no

 Contact information:
 Norwegian Meteorological Institute
 Box 43 Blindern
 0313 OSLO
 NORWAY
 email: diana@met.no

 This file is part of python-diana

 python-diana is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 python-diana is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with python-diana; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

class MovieMaker
{
%TypeHeaderCode
#include "MovieMaker.h"
%End

public:
  MovieMaker(const std::string &filename, const std::string &format,
             float delay);
  %Docstring
  Sets the file name for the finished animation, the format it will be saved
  in, and the delay to use between frames.
  %End
  ~MovieMaker();

  std::string outputFile() const;
  %Docstring
  Returns the name of the file that will be created by the movie maker.
  %End
  std::string outputFormat() const;
  %Docstring
  Returns the format of the file that will be created by the movie maker.
  %End

  bool addImage(const QImage &image);
  %Docstring
  Adds a new image to the animation, returning True if successful or False if
  unsuccessful.
  %End
};
