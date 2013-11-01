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

struct SatFileInfo
{
%TypeHeaderCode
#include "diCommonTypes.h"
%End

  miutil::miString name;
  miutil::miString formattype; //mitiff or hdf5
  miutil::miString metadata;
  miutil::miString channelinfo;
  miutil::miString paletteinfo;
  int hdf5type;
  miutil::miTime time;
  //miutil::miClock clock;
  int day;
  bool opened;
  std::vector<miutil::miString> channel;
  miutil::miString default_channel;
  bool palette;
  std::vector<Colour> col;
  miutil::miString fileformat;
  SatFileInfo();
};

struct SatValues
{
%TypeHeaderCode
#include "diCommonTypes.h"
%End

    miutil::miString channel;
    float value; ///<rgb
    miutil::miString text; ///<palette
};

