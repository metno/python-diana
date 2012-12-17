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

class SatManager
{
%TypeHeaderCode
#include "diSatManager.h"
%End

public:
    struct subProdInfo {
      std::vector<miutil::miString> pattern;
      std::vector<SatFileInfo> file;
    };

  SatManager();

  SIP_PYDICT getProductsInfo() const [std::map<miutil::miString, std::map<miutil::miString,SatManager::subProdInfo> > ()];
  %MethodCode
  std::map<miutil::miString, std::map<miutil::miString,SatManager::subProdInfo> > m = sipCpp->getProductsInfo();

  PyObject *d = PyDict_New();
  if (d == NULL) {
      sipIsErr = 1;

  } else {
      std::map<miutil::miString, std::map<miutil::miString,SatManager::subProdInfo> >::iterator it = m.begin();
      for (it = m.begin(); it != m.end(); ++it) {

          const sipTypeDef *td = sipFindType("std::map<miutil::miString,SatManager::subProdInfo>");
          if (td == NULL) {
              sipIsErr = 1;
              break;
          }
          miutil::miString *t1 = new miutil::miString(it->first);
          std::map<miutil::miString,SatManager::subProdInfo> *t2 = new std::map<miutil::miString,SatManager::subProdInfo>(it->second);
          PyObject *tobj1 = sipConvertFromNewType(t1, sipType_miutil_miString, Py_None);
          PyObject *tobj2 = sipConvertFromNewType(t2, td, Py_None);

          if ((tobj1 == NULL) || (tobj2 == NULL) || (PyDict_SetItem(d, tobj1, tobj2) < 0)) {
              Py_DECREF(d);
              if (tobj1)
                  Py_DECREF(tobj1);
              else
                  delete t1;
              if (tobj2)
                  Py_DECREF(tobj2);
              else
                  delete t2;

              sipIsErr = 1;
              break;
          }

          Py_DECREF(tobj1);
          Py_DECREF(tobj2);
      }
  }
  sipRes = d;
  %End

private:
  SatManager &operator=(const SatManager &);
};
