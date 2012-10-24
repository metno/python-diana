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

class SpectrumManager
{
%TypeHeaderCode
#include "diSpectrumManager.h"
%End

public:
  SpectrumManager();
  ~SpectrumManager();

  void parseSetup();
  SpectrumOptions* getOptions();
  void setPlotWindow(int w, int h);

  void setModel();
  void setStation(const miutil::miString& station);
  void setTime(const miutil::miTime& time);
  miutil::miString setStation(int step);
  miutil::miTime setTime(int step);

  const miutil::miTime getTime();
  const miutil::miString getStation();
  const miutil::miString getLastStation();
  const std::vector<miutil::miString>& getStationList();
  const std::vector<float>& getLatitudes();
  const std::vector<float>& getLongitudes();
  const std::vector<miutil::miTime>& getTimeList();

  std::vector<miutil::miString> getModelNames();
  std::vector<miutil::miString> getModelFiles();
  void setFieldModels(const std::vector<miutil::miString>& fieldmodels);
  void setSelectedModels(const std::vector<miutil::miString>& models,
			 bool obs, bool field);
  void setSelectedFiles(const std::vector<miutil::miString>& files,
			bool obs, bool field);

  std::vector<miutil::miString> getSelectedModels();

  bool plot();
};
