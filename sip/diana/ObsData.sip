/*
 python-diana - Python API for Diana - A Free Meteorological Visualisation Tool

 Copyright (C) 2013 met.no

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

class ObsData
{
%TypeHeaderCode
#include "diObsData.h"
%End

public:
  //desc
  std::string dataType;
  std::string id;
  std::string name;
  float xpos;
  float ypos;
  int zone;
  miutil::miTime obsTime;

  //metar
  std::string metarId;
  bool CAVOK;              
  std::vector<std::string> REww;   ///< Recent weather
  std::vector<std::string> ww;     ///< Significant weather
  std::vector<std::string> cloud;  ///< Clouds
  std::string appendix;       ///< For whatever remains
  
  std::map<std::string,float> fdata;
  std::map<std::string,std::string> stringdata;

  //Hqc  
  std::map<std::string,std::string> flag; 
  std::map<std::string,Colour> flagColour;
};

