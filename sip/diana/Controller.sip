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
  #define FILL_LIST_VALUES(arg, wrapper, TYPE, SIP_TYPE) \
    PyObject *wrapper = PyList_New(arg.size()); \
    for (unsigned int i = 0; i < arg.size(); ++i) { \
      TYPE *t = new TYPE(arg.at(i)); \
      PyObject *tobj; \
      if ((tobj = sipConvertFromNewType(t, SIP_TYPE, NULL)) == NULL) \
          delete t; \
      else \
          PyList_SET_ITEM(wrapper, i, tobj); \
  }

  #define FILL_SET_VALUES(arg, wrapper, TYPE, SIP_TYPE) \
    PyObject *wrapper = PySet_New(NULL); \
    { \
      std::set<TYPE>::iterator it; \
      for (it = arg.begin(); it != arg.end(); ++it) { \
        TYPE *t = new TYPE(*it); \
        PyObject *tobj; \
        if ((tobj = sipConvertFromNewType(t, SIP_TYPE, NULL)) == NULL) \
          delete t; \
        else \
          PySet_Add(wrapper, tobj); \
    } \
  }
  #define CONVERT_TYPE(obj, wrapper, TYPE, SIP_TYPE) \
    PyObject *wrapper; \
    { \
      TYPE *t = new TYPE(obj); \
      if ((wrapper = sipConvertFromNewType(t, SIP_TYPE, NULL)) == NULL) \
        delete t; \
    }
  #define FILL_DICT_VALUES(arg, wrapper, TYPE1, TYPE2) \
   PyObject *wrapper; \
   { \
     std::map<TYPE1,TYPE2>::iterator it; \
     for (it = arg.begin(); it != arg.end(); ++it) { \
       \
       TYPE1 *t1 = new TYPE1(it->first); \
       const sipTypeDef *td1 = sipFindType("TYPE1"); \
       if (td1 == NULL) { \
         sipIsErr = 1; \
         delete t1; \
         break; \
       } \
       \
       TYPE2 *t2 = new TYPE2(it->second); \
       const sipTypeDef *td2 = sipFindType("TYPE2"); \
       if (td2 == NULL) { \
         sipIsErr = 1; \
         delete t1; \
         delete t2; \
         break; \
       } \
       \
       PyObject *tobj1 = sipConvertFromNewType(t1, td1, Py_None); \
       PyObject *tobj2 = sipConvertFromNewType(t2, td2, Py_None); \
       \
       if ((tobj1 == NULL) || (tobj2 == NULL) || (PyDict_SetItem(wrapper, tobj1, tobj2) < 0)) \
       { \
         Py_DECREF(wrapper); \
         if (tobj1) \
           Py_DECREF(tobj1); \
         else \
           delete t1; \
         if (tobj2) \
           Py_DECREF(tobj2); \
         else \
           delete t2; \
         \
         sipIsErr = 1; \
         break; \
       } \
       \
       Py_DECREF(tobj1); \
       Py_DECREF(tobj2); \
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
  SatManager* getSatelliteManager();
  ObsManager* getObservationManager();

  void addManager(const std::string &name, Manager *man);
  Manager *getManager(const std::string &name);

  bool parseSetup();
  %Docstring
  Controller.parseSetup() -> bool

  Asks each of the manager components to parse the setup file, returning True
  if successful or False if an error occurred. The setup file must have previously
  been parsed by LocalSetupParser.parse().
  %End

  void plotCommands(const std::vector<std::string>&);
  %Docstring
  Controller.plotCommands(list commands)

  Prepares the plot for creation using the list of command strings, but does not
  actually create the plot.
  %End

  void plot(bool over =true, bool under =true);
  %Docstring
  Controller.plot(bool over=True, bool under=True)

  Paints the plot onto the current output device. The over and under arguments
  determine whether or not the overlay and underlay will be plotted. Typically,
  the default values should be used.
  %End

  std::vector<Rectangle> plotAnnotations();
  %Docstring
  Plots the annotations associated with the product and returns a list of
  rectangles describing the regions of the product covered by them.
  %End

  std::vector<AnnotationPlot*> getAnnotations();
  %Docstring
  Returns a list of annotation plots associated with the product.
  %End

  Area getMapArea();
  %Docstring
  Controller.getMapArea() -> Area

  Returns the map area defined in map units.
  %End

  void setPlotWindow(const int, const int);
  %Docstring
  Controller.setPlotWindow(int width, int height)

  Defines the size in pixels of the plot window to be painted on. This is usually
  the same size as the output device later used to record the plot.
  %End

  SIP_PYDICT getPlotTimes(bool updateSources = false)
        [void (std::map<std::string,std::vector<miutil::miTime> >& times,
               bool updateSources = false)];
  %Docstring
  times = Controller.getPlotTimes(updateSources = False)

  Replaces the items in the dictionary to contain the available times for fields,
  satellite images, observations, objects and products.
  %End
  %MethodCode
  std::map<std::string,std::vector<miutil::miTime> > times;
  sipCpp->getPlotTimes(times, a0);

  sipRes = PyDict_New();
  std::map<std::string,std::vector<miutil::miTime> >::iterator it;
  for (it = times.begin(); it != times.end(); ++it) {
    CONVERT_TYPE(it->first, key, std::string, sipType_std_string);
    FILL_LIST_VALUES(it->second, value, miutil::miTime, sipType_miutil_miTime);
    PyDict_SetItem(sipRes, key, value);
  }
  //FILL_DICT_VALUES(times, timesWrapper, std::string, std::vector<miutil::miTime>);
  //sipRes = timesWrapper;

  //const sipTypeDef *td1 = sipFindType("std::map<std::string,std::vector<miutil::miTime> >");
  //if (td1 == NULL) {
  //  sipIsErr = 1;
  //} else {
  //  sipRes = sipConvertFromType(&times, td1, Py_None);
  //}
  %End

/*  vector<AnnotationPlot*> getAnnotations();
  vector<Rectangle> plotAnnotations();
  void getCapabilitiesTime(set<miutil::miTime>& okTimes,
                           set<miutil::miTime>& constTimes,
                           const vector<std::string>& pinfos,
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

  void updateObs();
  %Docstring
  Updates the information held about observations.
  %End

  void keepCurrentArea(bool);
  %Docstring
  Controller.keepCurrentArea(bool keep)

  If the keep argument is True, the controller should keep the current area for
  subsequent plots. If it is False, an appropriate area for the extent of the
  data will be used instead.
  %End

  std::vector<std::string> getFieldModels();
  %Docstring
  Controller.getFieldModels()
  
  Returns the list of available field models.
  %End

  std::vector<std::string> getCalibChannels();
  %Docstring
  Returns the names of the current channels (with calibration).
  %End

  std::vector <std::string> getSatnames();
  %Docstring
  Returns the satellite names from all satellite plots.
  %End
          
  void archiveMode( bool );

  std::vector<FieldDialogInfo> initFieldDialog();
  %Docstring
  Returns a list of objects describing field model information.
  %End

  std::set<std::string> getFieldReferenceTimes(const std::string model);
  %Docstring
  Returns all reference times for the given model.
  %End

  std::string getBestFieldReferenceTime(const std::string& model, int refOffset, int refHour);
  %Docstring
  Returns the references time given by refOffset and refHour or the last reference time for the given model.
  %End

  std::vector<std::string> getAllFieldNames() [void (std::vector<std::string>& fieldNames)];
  %MethodCode
  std::vector<std::string> a0;
  sipCpp->getAllFieldNames(a0);
  sipRes = a0;
  %End

  std::vector<miutil::miTime> getFieldTime(std::vector<FieldRequest>& request);
  %Docstring
  Returns available times for the requested fields.
  %End

  std::vector<FieldGroupInfo> getFieldGroups(const std::string& modelName, std::string refTime, bool plotGroups)
    [void (const std::string& modelName,
           std::string refTime,
           bool plotGroups,
           std::vector<FieldGroupInfo>& vfgi)];
  %MethodCode
  std::vector<FieldGroupInfo> vfgi;
  sipCpp->getFieldGroups(*a0, *a1, a2, vfgi);
  sipRes = vfgi;
  %End

//  std::vector<SatPlot*> getSatellitePlots() const;
  std::vector<FieldPlot*> getFieldPlots() const;
//  std::vector<ObsPlot*> getObsPlots() const;
};

