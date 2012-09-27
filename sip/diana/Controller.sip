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

%Import std/std.sip

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
  void plotCommands(const std::vector<miutil::miString>&);
  void setPlotWindow(const int, const int);
  void plot(bool over =true, bool under =true);
  Area getMapArea();
  void getPlotTimes(std::vector<miutil::miTime>& /GetWrapper/,std::vector<miutil::miTime>& /GetWrapper/,
                    std::vector<miutil::miTime>& /GetWrapper/,std::vector<miutil::miTime>& /GetWrapper/,
                    std::vector<miutil::miTime>& /GetWrapper/);
  %MethodCode
  sipCpp->getPlotTimes(*a0, *a1, *a2, *a3, *a4);
  #define getPlotTimes_REPLACE_VALUES(arg, wrapper) \
    PyList_SetSlice(wrapper, 0, PyList_GET_SIZE(wrapper), NULL); \
    for (unsigned int i = 0; i < arg->size(); ++i) { \
      miutil::miTime *t = new miutil::miTime(arg->at(i)); \
      PyObject *tobj; \
      if ((tobj = sipConvertFromNewType(t, sipType_miutil_miTime, NULL)) == NULL) \
          delete t; \
      else \
          PyList_Append(wrapper, tobj); \
  }
  
  getPlotTimes_REPLACE_VALUES(a0, a0Wrapper)
  getPlotTimes_REPLACE_VALUES(a1, a1Wrapper)
  getPlotTimes_REPLACE_VALUES(a2, a2Wrapper)
  getPlotTimes_REPLACE_VALUES(a3, a3Wrapper)
  getPlotTimes_REPLACE_VALUES(a4, a4Wrapper)
  %End
/*  vector<AnnotationPlot*> getAnnotations();
  vector<Rectangle> plotAnnotations();
  void getCapabilitiesTime(set<miutil::miTime>& okTimes,
                           set<miutil::miTime>& constTimes,
                           const vector<miutil::miString>& pinfos,
                           bool allTimes=true);
*/
  bool setPlotTime(miutil::miTime&);
  bool updatePlots();
  void keepCurrentArea(bool);

  void archiveMode( bool );
};

