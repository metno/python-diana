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

class ObsManager
{
%TypeHeaderCode
#include "diObsManager.h"
%End

public:
    struct patternInfo {
        TimeFilter filter;
        std::string pattern;
        bool archive;
        std::string fileType;
    };

    struct FileInfo {
        std::string filename;
        miutil::miTime   time;
        std::string filetype;
    };

    struct ProdInfo {
//      ObsFormat obsformat; // ObsFormat is private
        std::string dialogName;
        std::string plotFormat;
        std::vector<ObsManager::patternInfo> pattern;
        std::vector<ObsManager::FileInfo> fileInfo;
        std::vector<std::string> headerinfo;
        std::string timeInfo;
        int timeRangeMin;
        int timeRangeMax;
        float current;
        bool synoptic;
        std::string headerfile;
        std::string metaData;
/*  #ifdef ROADOBS
        std::string stationfile;
        std::string databasefile;
        int daysback;
    #endif */
        bool useFileTime;
        std::vector<std::string> parameter;
    };

    ObsManager();
    ObsPlot* createObsPlot(const std::string&);
    bool prepare(ObsPlot *,miutil::miTime);

    std::vector<miutil::miTime> getObsTimes(const std::vector<std::string>& obsTypes);
    bool obs_mslp();
    void updateObsPositions(const std::vector<ObsPlot*> oplot);
    ObsPositions& getObsPositions();
    void clearObsPositions();
    void archiveMode(bool on);
    bool timeListChanged;

    std::map<std::string, ObsManager::ProdInfo> getProductsInfo() const;
};
