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

%ModuleHeaderCode
  #define CONVERT_TYPE(obj, wrapper, TYPE, SIP_TYPE) \
    PyObject *wrapper; \
    { \
      TYPE *t = new TYPE(obj); \
      if ((wrapper = sipConvertFromNewType(t, SIP_TYPE, NULL)) == NULL) \
        delete t; \
    }
%End

class PlotModule
{
%TypeHeaderCode
#include "diPlotModule.h"
%End

public:
  PlotModule();
  ~PlotModule();

  const Area& getCurrentArea();
  const Rectangle& getPlotSize();

  SIP_PYTUPLE getPlotWindow() [void (int &width, int &height)];
  %MethodCode
  int w, h;
  sipCpp->getPlotWindow(w, h);

  PyObject *widthWrapper = PyInt_FromLong(w);
  PyObject *heightWrapper = PyInt_FromLong(h);

  sipRes = PyTuple_New(2);
  PyTuple_SET_ITEM(sipRes, 0, widthWrapper);
  PyTuple_SET_ITEM(sipRes, 1, heightWrapper);
  %End

  SIP_PYTUPLE PhysToMap(const float, const float) [void (const float, const float, float &, float &)];
  %MethodCode
  float xmap, ymap;
  sipCpp->PhysToMap(a0, a1, xmap, ymap);

  PyObject *xmapWrapper = PyFloat_FromDouble(xmap);
  PyObject *ymapWrapper = PyFloat_FromDouble(ymap);

  sipRes = PyTuple_New(2);
  PyTuple_SET_ITEM(sipRes, 0, xmapWrapper);
  PyTuple_SET_ITEM(sipRes, 1, ymapWrapper);
  %End

  bool PhysToGeo(const float x, const float y, float& lat, float& lon, Area area, Rectangle r);
  bool GeoToPhys(const float, const float, float&, float&, Area area, Rectangle r);

  static PlotModule *instance();

private:
  PlotModule &operator=(PlotModule &);
  PlotModule(PlotModule &);
};
