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

class Controller
{
%TypeHeaderCode
#include "diController.h"
%End

public:
  Controller();
  ~Controller();

  FieldManager* getFieldManager();

  bool parseSetup();
/*  void plotCommands(const vector<miutil::miString>&);
  void plot(bool over =true, bool under =true);
  vector<AnnotationPlot*> getAnnotations();
  vector<Rectangle> plotAnnotations();
  void setPlotWindow(const int, const int);
  void getPlotTimes(vector<miutil::miTime>& fieldtimes,vector<miutil::miTime>& sattimes,
                    vector<miutil::miTime>& obstimes,vector<miutil::miTime>& objtimes,
                    vector<miutil::miTime>& ptimes);
  void getCapabilitiesTime(set<miutil::miTime>& okTimes,
                           set<miutil::miTime>& constTimes,
                           const vector<miutil::miString>& pinfos,
                           bool allTimes=true);

  bool setPlotTime(miutil::miTime&);*/
  bool updatePlots();
};

