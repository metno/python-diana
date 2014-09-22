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
      std::vector<std::string> pattern;
      std::vector<bool> archive;
      std::string formattype; //holds mitiff or hdf5
      std::string metadata;
      std::string channelinfo;
      std::string paletteinfo;
      int hdf5type;
      std::vector<SatFileInfo> file;
      std::vector<std::string> channel;
      unsigned long updateTime;
    };

    SatManager();
    bool init(const std::vector<std::string>&);
    std::vector<miutil::miTime> getSatTimes(bool updateFileList=false, bool openFiles=false);

    const std::vector<SatFileInfo> & getFiles(const std::string &,
                                              const std::string &,
                                              bool = false);
    const std::vector<Colour> & getColours(const std::string &,
                                           const std::string &);
    const std::vector<std::string>& getChannels(const std::string &satellite,
                                                     const std::string & file,
                                                     int index=-1);
    bool isMosaic(const std::string &satellite, const std::string & file);

    SIP_PYDICT getProductsInfo() const [std::map<std::string, std::map<std::string,SatManager::subProdInfo> > ()];
    %MethodCode
    std::map<std::string, std::map<std::string,SatManager::subProdInfo> > m = sipCpp->getProductsInfo();

    PyObject *d = PyDict_New();
    if (d == NULL) {
        sipIsErr = 1;

    } else {
        std::map<std::string, std::map<std::string,SatManager::subProdInfo> >::iterator it;
        for (it = m.begin(); it != m.end(); ++it) {

            std::map<std::string,SatManager::subProdInfo> productMap = it->second;

            std::string *t1 = new std::string(it->first);
            PyObject *tobj1 = sipConvertFromNewType(t1, sipType_std_string, Py_None);
            PyObject *d2 = PyDict_New();

            if ((tobj1 == NULL) || (d2 == NULL) || (PyDict_SetItem(d, tobj1, d2) < 0)) {
                Py_DECREF(d);
                if (tobj1)
                    Py_DECREF(tobj1);
                else
                    delete t1;
                if (d2)
                    Py_DECREF(d2);

                sipIsErr = 1;
                break;
            }

            std::map<std::string,SatManager::subProdInfo>::iterator it2;

            for (it2 = productMap.begin(); it2 != productMap.end(); ++it2) {
                std::string *t2 = new std::string(it2->first);
                PyObject *tobj2 = sipConvertFromNewType(t2, sipType_std_string, Py_None);
                SatManager::subProdInfo *t3 = new SatManager::subProdInfo(it2->second);
                PyObject *tobj3 = sipConvertFromNewType(t3, sipType_SatManager_subProdInfo, Py_None);

                if ((tobj2 == NULL) || (tobj3 == NULL) || (PyDict_SetItem(d2, tobj2, tobj3) < 0)) {
                    Py_DECREF(d);
                    if (tobj2)
                        Py_DECREF(tobj2);
                    else
                        delete t2;
                    if (tobj3)
                        Py_DECREF(tobj3);
                    else
                        delete t3;

                    sipIsErr = 1;
                    break;
                }
            }

            if (sipIsErr)
                break;

            Py_DECREF(tobj1);
            Py_DECREF(d2);
        }
    }
    sipRes = d;
    %End

private:
    SatManager &operator=(const SatManager &);
};
