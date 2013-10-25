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

%MappedType miutil::miString
{
    %TypeHeaderCode
    #include <puTools/miString.h>
    %End

    %ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        if (!PyString_Check(sipPy))
            return 0;
        else
            return 1;
    }

    miutil::miString *s = new miutil::miString(PyString_AsString(sipPy));
    *sipCppPtr = s;

    return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
    PyObject *s = PyString_FromString(sipCpp->c_str());

    return s;
    %End
};

%MappedType miutil::miTime
{
    %TypeHeaderCode
    #include <puTools/miTime.h>
    #include <datetime.h>
    %End

    %ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        if (!PyDateTimeAPI)
            PyDateTime_IMPORT;

        if (!PyDateTime_Check(sipPy))
            return 0;
        else
            return 1;
    }

    miutil::miTime *t = new miutil::miTime();
    t->setTime(int(PyDateTime_GET_YEAR(sipPy)),
               int(PyDateTime_GET_MONTH(sipPy)),
               int(PyDateTime_GET_DAY(sipPy)),
               int(PyDateTime_DATE_GET_HOUR(sipPy)),
               int(PyDateTime_DATE_GET_MINUTE(sipPy)),
               int(PyDateTime_DATE_GET_SECOND(sipPy)));
    *sipCppPtr = t;

    return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
    if (!PyDateTimeAPI)
        PyDateTime_IMPORT;

    PyObject *t = PyDateTime_FromDateAndTime(sipCpp->year(), sipCpp->month(),
                                             sipCpp->day(), sipCpp->hour(),
                                             sipCpp->min(), sipCpp->sec(), 0);

    return t;
    %End
};

%MappedType std::vector<miutil::miTime>
{
%TypeHeaderCode
#include <vector>
#include <puTools/miTime.h>
%End

    %ConvertFromTypeCode
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    for (unsigned int i = 0; i < sipCpp->size(); ++i)
    {
        miutil::miTime *t = new miutil::miTime(sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewType(t, sipType_miutil_miTime, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;
            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
    %End

    %ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (unsigned int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
        {
            if (!sipCanConvertToType(PyList_GET_ITEM(sipPy, i), sipType_miutil_miTime, 0))
                return 0;
        }

        return 1;
    }

    std::vector<miutil::miTime> *v = new std::vector<miutil::miTime>();

    for (unsigned int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        miutil::miTime *t = reinterpret_cast<miutil::miTime *>(sipConvertToType(PyList_GET_ITEM(sipPy, i),
                                           sipType_miutil_miTime, sipTransferObj, SIP_NOT_NONE,
                                           &state, sipIsErr));
        if (*sipIsErr)
        {
            sipReleaseType(t, sipType_miutil_miTime, state);
            delete v;
            return 0;
        }

        v->push_back(*t);
        sipReleaseType(t, sipType_miutil_miTime, state);
    }

    *sipCppPtr = v;

    return sipGetState(sipTransferObj);
    %End
};

