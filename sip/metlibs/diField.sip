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

    std::string toString() const;
    std::string toLogString() const;
    std::string getAreaString() const;
};

class Projection
{
%TypeHeaderCode
#include <diField/diProjection.h>
%End

public:
    enum pType {
      undefined_projection = 0,
      polarstereographic_60= 1,
      geographic=            2,
      spherical_rotated=     3,
      polarstereographic=    4,
      mercator=              5,
      lambert=               6,
      generic=             100
    };
    enum { speclen= 6 };

    Projection();
    Projection(const std::string& projStr, const double projResX, const double projResY);
    Projection(const std::map<std::string,std::string>& definitions, double resolutionX, double resolutionY);

    ~Projection();

    bool set_proj_definition(const std::string& projStr, const double projResX=1.0, const double projResY=1.0);
    std::string getProjDefinition() const;

    bool isDefined() const;

    bool setProjection(const std::string& projectionString, double& resolutionX, double& resolutionY);
    bool setProjectionFromLog(const std::string& logtext, double& resolutionX, double& resolutionY);
    std::string toString(bool fortranStyle=true) const;
    std::string toLogString() const;
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

struct FieldGroupInfo
{
%TypeHeaderCode
#include "diField/diCommonFieldTypes.h"
%End
  std::string modelName;
  std::string groupName;
  std::vector<std::string> fieldNames;
  std::vector<std::string> standard_names;
  std::vector<std::string> units;
  std::vector<std::string> levelNames;
  std::vector<std::string> idnumNames;
  std::string defaultLevel;
  std::string defaultIdnum;
  std::string refTime;
  std::string zaxis;
  std::string extraaxis;
  std::string grid;
  bool cdmSyntax;
  bool plotDefinitions;
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

