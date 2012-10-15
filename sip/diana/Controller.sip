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

%ModuleHeaderCode
  #define REPLACE_LIST_VALUES(arg, wrapper, TYPE, SIP_TYPE) \
    PyList_SetSlice(wrapper, 0, PyList_GET_SIZE(wrapper), NULL); \
    for (unsigned int i = 0; i < arg->size(); ++i) { \
      TYPE *t = new TYPE(arg->at(i)); \
      PyObject *tobj; \
      if ((tobj = sipConvertFromNewType(t, SIP_TYPE, NULL)) == NULL) \
          delete t; \
      else \
          PyList_Append(wrapper, tobj); \
  }

  #define REPLACE_SET_VALUES(arg, wrapper, TYPE, SIP_TYPE) \
    PySet_Clear(wrapper); \
    { \
      std::set<TYPE>::iterator it; \
      for (it = arg->begin(); it != arg->end(); ++it) { \
        TYPE *t = new TYPE(*it); \
        PyObject *tobj; \
        if ((tobj = sipConvertFromNewType(t, SIP_TYPE, NULL)) == NULL) \
          delete t; \
        else \
          PySet_Add(wrapper, tobj); \
    } \
  }
%End

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
  %Docstring
  Controller.parseSetup() -> bool

  Asks each of the manager components to parse the setup file, returning True
  if successful or False if an error occurred. The setup file must have previously
  been parsed by LocalSetupParser.parse().
  %End

  void plotCommands(const std::vector<miutil::miString>&);
  %Docstring
  Controller.plotCommands(list commands)

  Prepares the plot for creation using the list of command strings, but does not
  actually create the plot.
  %End

  void setPlotWindow(const int, const int);
  %Docstring
  Controller.setPlotWindow(int width, int height)

  Defines the size in pixels of the plot window to be painted on. This is usually
  the same size as the output device later used to record the plot.
  %End

  void plot(bool over =true, bool under =true);
  %Docstring
  Controller.plot(bool over=True, bool under=True)

  Paints the plot onto the current output device. The over and under arguments
  determine whether or not the overlay and underlay will be plotted. Typically,
  the default values should be used.
  %End

  Area getMapArea();
  %Docstring
  Controller.getMapArea() -> Area

  Returns the map area defined in map units.
  %End

  void getPlotTimes(std::vector<miutil::miTime>& fieldtimes /GetWrapper/,
                    std::vector<miutil::miTime>& sattimes /GetWrapper/,
                    std::vector<miutil::miTime>& obstimes /GetWrapper/,
                    std::vector<miutil::miTime>& objtimes /GetWrapper/,
                    std::vector<miutil::miTime>& ptimes /GetWrapper/);
  %Docstring
  Controller.getPlotTimes(list fieldtimes, list sattimes, list obstimes, list objtimes, list ptimes)

  Replaces the items in the lists supplied to contain the available times for fields,
  satellite images, observations, objects and products.
  %End
  %MethodCode
  sipCpp->getPlotTimes(*a0, *a1, *a2, *a3, *a4);
  REPLACE_LIST_VALUES(a0, a0Wrapper, miutil::miTime, sipType_miutil_miTime)
  REPLACE_LIST_VALUES(a1, a1Wrapper, miutil::miTime, sipType_miutil_miTime)
  REPLACE_LIST_VALUES(a2, a2Wrapper, miutil::miTime, sipType_miutil_miTime)
  REPLACE_LIST_VALUES(a3, a3Wrapper, miutil::miTime, sipType_miutil_miTime)
  REPLACE_LIST_VALUES(a4, a4Wrapper, miutil::miTime, sipType_miutil_miTime)
  %End

/*  vector<AnnotationPlot*> getAnnotations();
  vector<Rectangle> plotAnnotations();
  void getCapabilitiesTime(set<miutil::miTime>& okTimes,
                           set<miutil::miTime>& constTimes,
                           const vector<miutil::miString>& pinfos,
                           bool allTimes=true);
*/
  bool setPlotTime(miutil::miTime&);
  %Docstring
  Controller.setPlotTime(miTime time) -> bool

  Sets the time information for the current plot, returning True if successful
  or False if not.
  %End

  bool updatePlots();
  %Docstring
  Controller.updatePlots() -> bool

  Updates the information for the plot, ensuring that the latest information is
  used and unused resources are released. Returns True if successful or False if
  an error occurred.
  %End

  void keepCurrentArea(bool);
  %Docstring
  Controller.keepCurrentArea(bool keep)

  If the keep argument is True, the controller should keep the current area for
  subsequent plots. If it is False, an appropriate area for the extent of the
  data will be used instead.
  %End

  void archiveMode( bool );

  void getAllFieldNames(std::vector<miutil::miString>& fieldNames /GetWrapper/,
                        std::set<std::string>& fieldprefixes /GetWrapper/,
                        std::set<std::string>& fieldsuffixes /GetWrapper/);
  %MethodCode
  sipCpp->getAllFieldNames(*a0, *a1, *a2);
  REPLACE_LIST_VALUES(a0, a0Wrapper, miutil::miString, sipType_miutil_miString)
  REPLACE_SET_VALUES(a1, a1Wrapper, std::string, sipType_std_string)
  REPLACE_SET_VALUES(a2, a2Wrapper, std::string, sipType_std_string)
  %End
};

