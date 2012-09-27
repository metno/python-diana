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

%Import qt/qt.sip

class PaintGLContext
{
    %TypeHeaderCode
    #include "PaintGL/paintgl.h"
    %End

public:
    PaintGLContext();
    virtual ~PaintGLContext();

    void makeCurrent();
    void begin(QPainter *painter);
    bool isPainting() const;
    void end();
};

class PaintGL
{
    %TypeHeaderCode
    #include "PaintGL/paintgl.h"
    %End

public:
    PaintGL();
    ~PaintGL();

    static PaintGL *instance() /Factory/;
    PaintGLContext *currentContext;
};

