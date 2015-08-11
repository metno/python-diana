/*
 python-diana - Python API for Diana - A Free Meteorological Visualisation Tool

 Copyright (C) 2015 met.no

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

class DiPaintGLCanvas : public DiGLCanvas
{
%TypeHeaderCode
#include "diPaintGLPainter.h"
%End

public:
  DiPaintGLCanvas(QPaintDevice* device);
  ~DiPaintGLCanvas();

  QPaintDevice* device() const;
};

class DiPaintGLPainter : public DiGLPainter
{
%TypeHeaderCode
#include "diPaintGLPainter.h"
%End

public:
  typedef int             GLint;      /* 4-byte signed */
  typedef int             GLsizei;    /* 4-byte signed */

  DiPaintGLPainter(DiPaintGLCanvas* canvas);
  ~DiPaintGLPainter();

  void Viewport(GLint x, GLint y, GLsizei width, GLsizei height);

  void begin(QPainter *painter);
  bool isPainting() const;
  void end();

  QTransform transform;
  QRect viewport;
};

