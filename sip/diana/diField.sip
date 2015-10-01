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

class FieldManager
{
%TypeHeaderCode
#include <string>
#include <diField/diFieldManager.h>
%End

public:
  FieldManager();
  ~FieldManager();

  bool updateFileSetup(const std::vector<std::string>& lines,
                       std::vector<std::string>& errors,
                       bool clearSources=false,
                       bool top=false);
  %Docstring
  Updates the list of field files held by the manager using the descriptions
  provided in the list of lines. Errors are returned in the list of errors
  passed to the method.

  If clearSources is True then the existing field sources are cleared before
  the new field files are read.
  If top is True then the new fields are given priority over any existing
  fields with the same names.
  %End

  void updateSources();
  void updateSource(const std::string & modelName);

  std::vector<FieldDialogInfo> getFieldDialogInfo();
  bool modelOK(const std::string& modelName);

  std::vector<std::string> getFileNames(const std::string& modelName);
};

class Area
{
%TypeHeaderCode
#include <string>
#include <diField/diArea.h>
%End

public:
    Area();
    ~Area();

    const Projection& P() const;
    const Rectangle& R() const;

    std::string getAreaString() const;
};

class GridArea : public Area
{
%TypeHeaderCode
#include <diField/diArea.h>
%End

public:
  GridArea();
  GridArea(const Area& rhs);
  GridArea(const Area& rhs, int nX, int nY, float rX, float rY);
  int gridSize() const;
  GridArea scaled(int factor) const;
};

class Projection
{
%TypeHeaderCode
#include <diField/diProjection.h>
%End

public:
    Projection();
    ~Projection();

    bool set_proj_definition(const std::string& projStr);
    std::string getProjDefinition() const;

    bool isDefined() const;
    bool isGeographic() const;
};

class Rectangle
{
    %TypeHeaderCode
    #include <diField/diRectangle.h>
    %End

public:
    Rectangle();
    Rectangle(const float x1, const float y1, const float x2, const float y2);

    float width() const;
    float height() const;

    float x1;
    float y1;
    float x2;
    float y2;

    std::string toString(bool fortranStyle=true) const;
};

struct FieldInfo
{
%TypeHeaderCode
#include "diField/diCommonFieldTypes.h"
%End
    std::string fieldName;
    std::string groupName;
    std::string standard_name;
    std::string units;
    std::vector<std::string>  vlevels;
    std::vector<std::string> elevels; //(EPS clusters, EPS single runs etc.)
    std::string default_vlevel;
    std::string default_elevel;
    std::string vcoord;
    std::string ecoord;
};

struct FieldGroupInfo
{
%TypeHeaderCode
#include "diField/diCommonFieldTypes.h"
%End
    std::string groupName;
    bool plotDefinitions;
    std::vector<std::string> fieldNames;
    std::map<std::string,FieldInfo> fields;
    FieldGroupInfo();
};


struct FieldDialogInfo
{
%TypeHeaderCode
#include "diField/diCommonFieldTypes.h"
%End
  std::string groupName;
  std::string groupType;
  std::vector<std::string> modelNames;
};

struct FieldRequest
{
%TypeHeaderCode
#include "diField/diCommonFieldTypes.h"
%End
  std::string modelName;
  std::string paramName;
  std::string zaxis;
  std::string eaxis;
  std::string taxis;
  std::string plevel;
  std::string elevel;
  std::string grid;
  std::string version;
  std::string refTime;
  miutil::miTime ptime;
  std::string unit;
  std::string palette;
  int hourOffset;
  int minOffset;
  int time_tolerance;
  int refhour;
  int refoffset;
  std::string output_time;
  bool allTimeSteps;
  bool standard_name;
  bool plotDefinition;
  bool checkSourceChanged;
  bool flightlevel;
  FieldRequest();
};

class TimeFilter
{
%TypeHeaderCode
#include "diField/TimeFilter.h"
%End

  TimeFilter();

  bool initFilter(std::string& filename, bool advanced_=false);
  bool ok();
  bool getTime(std::string name, miutil::miTime & t);

  std::string getTimeStr(std::string name);
};

