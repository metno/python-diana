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

%Module std

%MappedType std::string
{
    %TypeHeaderCode
    #include <string>
    %End

    %ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        if (!PyString_Check(sipPy))
            return 0;
        else
            return 1;
    }

    std::string *s = new std::string(PyString_AsString(sipPy));
    *sipCppPtr = s;

    return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
    PyObject *s = PyString_FromString(sipCpp->c_str());

    return s;
    %End
};

template<TYPE>
%MappedType std::vector<TYPE>
{
    %TypeHeaderCode
    #include <vector>
    %End

    %ConvertFromTypeCode
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    for (unsigned int i = 0; i < sipCpp->size(); ++i)
    {
        TYPE *t = new TYPE(sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewType(t, sipType_TYPE, sipTransferObj)) == NULL)
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
            if (!sipCanConvertToType(PyList_GET_ITEM(sipPy, i), sipType_TYPE, 0))
                return 0;
        }

        return 1;
    }

    std::vector<TYPE> *v = new std::vector<TYPE>();

    for (unsigned int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        TYPE *t = reinterpret_cast<TYPE *>(sipConvertToType(PyList_GET_ITEM(sipPy, i),
                                           sipType_TYPE, sipTransferObj, SIP_NOT_NONE,
                                           &state, sipIsErr));
        if (*sipIsErr)
        {
            sipReleaseType(t, sipType_TYPE, state);
            delete v;
            return 0;
        }

        v->push_back(*t);
        sipReleaseType(t, sipType_TYPE, state);
    }

    *sipCppPtr = v;

    return sipGetState(sipTransferObj);
    %End
};
