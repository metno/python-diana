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

%ModuleHeaderCode
  #define FILL_ARRAY_PYTHON_VALUES(array, size, wrapper, TYPE, PY_CONVERT_METHOD) \
    wrapper = PyList_New(size); \
    for (unsigned int i = 0; i < size; ++i) { \
      PyObject *tobj; \
      if ((tobj = PY_CONVERT_METHOD(array[i])) == NULL) { \
          Py_DECREF(wrapper); \
          wrapper = NULL; \
          break; \
      } else \
          PyList_SET_ITEM(wrapper, i, tobj); \
  }
%End

struct SatFileInfo
{
%TypeHeaderCode
#include "diCommonTypes.h"
%End

  std::string name;
  std::string formattype; //mitiff or hdf5
  std::string metadata;
  std::string channelinfo;
  std::string paletteinfo;
  int hdf5type;
  miutil::miTime time;
  //miutil::miClock clock;
  int day;
  bool opened;
  std::vector<std::string> channel;
  std::string default_channel;
  bool palette;
  std::vector<Colour> col;
  std::string fileformat;
  SatFileInfo();
};

struct SatValues
{
%TypeHeaderCode
#include "diCommonTypes.h"
%End

    std::string channel;
    float value; ///<rgb
    std::string text; ///<palette
};

struct ObsPositions
{
%TypeHeaderCode
#include "diCommonTypes.h"
%End

    Area obsArea;
    int numObs;
    float* xpos
    {
    %GetCode
        FILL_ARRAY_PYTHON_VALUES(sipCpp->xpos, sipCpp->numObs, sipPy, float, PyFloat_FromDouble)
    %End
    %SetCode
        sipPy = NULL;
    %End
    };

    float* ypos
    {
    %GetCode
        FILL_ARRAY_PYTHON_VALUES(sipCpp->ypos, sipCpp->numObs, sipPy, float, PyFloat_FromDouble)
    %End
    %SetCode
        sipPy = NULL;
    %End
    };

    float* values
    {
    %GetCode
        FILL_ARRAY_PYTHON_VALUES(sipCpp->values, sipCpp->numObs, sipPy, float, PyFloat_FromDouble)
    %End
    %SetCode
        sipPy = NULL;
    %End
    };

    bool convertToGrid;
    ObsPositions();
};

