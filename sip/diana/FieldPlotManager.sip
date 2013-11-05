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

class FieldPlotManager
{
%TypeHeaderCode
#include "diFieldPlotManager.h"
%End

public:
  FieldPlotManager(FieldManager *fm);

  struct PlotField {
    std::string name;
    std::string fieldgroup;
    std::string plot;
    std::vector<std::string> input;
    std::set< std::string > vcoord;
  };

  SIP_PYLIST getAllFieldNames() [void (std::vector<std::string>&)];
  %MethodCode
  std::vector<std::string> a0;
  sipCpp->getAllFieldNames(a0);
  FILL_LIST_VALUES(a0, a0Wrapper, std::string, sipType_std_string)

  sipRes = a0Wrapper;
  %End

  std::vector<std::string> getFields();
  std::vector<std::string> getPlotFields();
};
