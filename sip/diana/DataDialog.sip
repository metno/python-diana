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

class DataDialog : public QDialog
{
%TypeHeaderCode
#include "qtDataDialog.h"
%End

public:
  DataDialog(QWidget *parent, Controller *ctrl);
  virtual ~DataDialog();

  virtual QAction *action() const;
  virtual std::string name() const = 0;

  virtual void updateDialog() = 0;
  virtual std::vector<miutil::miString> getOKString() = 0;
  virtual void putOKString(const std::vector<miutil::miString>& vstr) = 0;

public slots:
  virtual void updateTimes() = 0;

signals:
  void emitTimes(const miutil::miString &, const std::vector<miutil::miTime> &);
  void emitTimes(const miutil::miString &, const std::vector<miutil::miTime> &, bool);
  void applyData();
  void hideData();
  void showsource(const std::string, const std::string="");
};

