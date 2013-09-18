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

%Module(name=metno.std, keyword_arguments="Optional")

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

template<TYPE>
%MappedType std::set<TYPE>
{
    %TypeHeaderCode
    #include <set>
    %End

    %ConvertFromTypeCode
    PyObject *l;

    if ((l = PySet_New(NULL)) == NULL)
        return NULL;

    std::set<TYPE>::iterator it;
    for (it = sipCpp->begin(); it != sipCpp->end(); ++it)
    {
        TYPE *t = new TYPE(*it);
        PyObject *tobj;

        if ((tobj = sipConvertFromNewType(t, sipType_TYPE, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;
            return NULL;
        }

        PySet_Add(l, tobj);
    }

    return l;
    %End

    %ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        if (!PySet_Check(sipPy))
            return 0;

        PyObject *iter = PyObject_GetIter(sipPy);
        if (!iter)
            return 0;

        PyObject *item;
        while ((item = PyIter_Next(iter)))
        {
            int ok = sipCanConvertToType(item, sipType_TYPE, 0);

            Py_DECREF(item);

            if (!ok) {
                Py_DECREF(iter);
                return 0;
            }
        }

        Py_DECREF(iter);
        return 1;
    }

    std::set<TYPE> *v = new std::set<TYPE>();

    PyObject *iter = PyObject_GetIter(sipPy);
    if (!iter)
        return 0;

    PyObject *item;
    while ((item = PyIter_Next(iter)))
    {
        int state;
        TYPE *t = reinterpret_cast<TYPE *>(sipConvertToType(item, sipType_TYPE,
                                           sipTransferObj, SIP_NOT_NONE,
                                           &state, sipIsErr));
        Py_DECREF(item);

        if (*sipIsErr)
        {
            sipReleaseType(t, sipType_TYPE, state);
            delete v;
            Py_DECREF(iter);
            return 0;
        }

        v->insert(*t);
        sipReleaseType(t, sipType_TYPE, state);
    }

    Py_DECREF(iter);
    *sipCppPtr = v;

    return sipGetState(sipTransferObj);
    %End
};

template<TYPE1, TYPE2>
%MappedType std::map<TYPE1, TYPE2>
{
    %TypeHeaderCode
    #include <map>
    %End

    %ConvertFromTypeCode
    PyObject *d;

    if ((d = PyDict_New()) == NULL)
        return NULL;

    std::map<TYPE1,TYPE2>::iterator it;
    for (it = sipCpp->begin(); it != sipCpp->end(); ++it)
    {
        TYPE1 *t1 = new TYPE1(it->first);
        const sipTypeDef *td1 = sipFindType("TYPE1");
        if (td1 == NULL) {
            sipIsErr = 1;
            delete t1;
            break;
        }

        TYPE2 *t2 = new TYPE2(it->second);
        const sipTypeDef *td2 = sipFindType("TYPE2");
        if (td2 == NULL) {
            sipIsErr = 1;
            delete t1;
            delete t2;
            break;
        }

        PyObject *tobj1 = sipConvertFromNewType(t1, td1, Py_None);
        PyObject *tobj2 = sipConvertFromNewType(t2, td2, Py_None);

        if ((tobj1 == NULL) || (tobj2 == NULL) || (PyDict_SetItem(d, tobj1, tobj2) < 0))
        {
            Py_DECREF(d);
            if (tobj1)
                Py_DECREF(tobj1);
            else
                delete t1;
            if (tobj2)
                Py_DECREF(tobj2);
            else
                delete t2;

            return NULL;
        }

        Py_DECREF(tobj1);
        Py_DECREF(tobj2);
    }

    return d;
    %End

    %ConvertToTypeCode
    PyObject *key;
    PyObject *value;
    SIP_SSIZE_T i = 0;

    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &key, &value))
        {
            if (!sipCanConvertToType(t1obj, sipType_TYPE1, SIP_NOT_NONE))
                return 0;

            if (!sipCanConvertToType(t2obj, sipType_TYPE2, SIP_NOT_NONE))
                return 0;
        }

        return 1;
    }

    std::map<TYPE1, TYPE2> *m = new std::map<TYPE1, TYPE2>();

    while (PyDict_Next(sipPy, &i, &key, &value))
    {
        int state1, state2;
        
        const sipTypeDef *td1 = sipFindType("TYPE1");
        const sipTypeDef *td2 = sipFindType("TYPE2");
        if (td1 == NULL || td2 == NULL) {
            delete m;
            return 0;
        }
        TYPE1 *t1 = reinterpret_cast<TYPE1 *>(sipConvertToType(t1obj, td1, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));
        TYPE2 *t2 = reinterpret_cast<TYPE2 *>(sipConvertToType(t2obj, td2, sipTransferObj, SIP_NOT_NONE, &state2, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseType(t1, sipType_TYPE1, state1);
            sipReleaseType(t2, sipType_TYPE2, state2);

            delete m;
            return 0;
        }

        m->insert(*t1, *t2);

        sipReleaseType(t1, sipType_TYPE1, state1);
        sipReleaseType(t2, sipType_TYPE2, state2);
    }

    *sipCppPtr = m;

    return sipGetState(sipTransferObj);
    %End
};

template<TYPE>
%MappedType std::vector<TYPE*>
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
        TYPE *t = sipCpp->at(i);
        PyObject *tobj;

        if ((tobj = sipConvertFromType(t, sipType_TYPE, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
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

    std::vector<TYPE*> *v = new std::vector<TYPE*>();

    for (unsigned int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        TYPE *t = reinterpret_cast<TYPE *>(sipConvertToType(PyList_GET_ITEM(sipPy, i),
                                           sipType_TYPE, sipTransferObj, 0, 0, sipIsErr));
        if (*sipIsErr)
        {
            delete v;
            return 0;
        }

        v->push_back(t);
    }

    *sipCppPtr = v;

    return sipGetState(sipTransferObj);
    %End
};

%MappedType std::vector<float>
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
        PyObject *tobj;

        if ((tobj = PyFloat_FromDouble(sipCpp->at(i))) == NULL)
        {
            Py_DECREF(l);
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
            if (!PyFloat_Check(PyList_GET_ITEM(sipPy, i)))
                return 0;
        }

        return 1;
    }

    std::vector<float> *v = new std::vector<float>();

    for (unsigned int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        PyObject *f = PyList_GET_ITEM(sipPy, i);
        if (!f)
        {
            delete v;
            *sipIsErr = 1;
            return 0;
        }

        v->push_back(PyFloat_AsDouble(f));
    }

    *sipCppPtr = v;

    return sipGetState(sipTransferObj);
    %End
};
