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

%ModuleCode
#include "diMapMode.h"
%End

enum cursortype {
  keep_it,
  normal_cursor,
  edit_cursor,
  edit_move_cursor,
  edit_value_cursor,
  draw_cursor,
  paint_select_cursor,
  paint_move_cursor,
  paint_draw_cursor,
  paint_add_cursor,
  paint_remove_cursor,
  paint_forbidden_cursor
};

enum actiontype {
  no_action,
  pointclick,
  rightclick,
  browsing,
  quick_browsing,
  objects_changed,
  fields_changed,
  keypressed,
  doubleclick
};

struct EventResult {
%TypeHeaderCode
#include "diMapMode.h"
%End
  bool repaint;
  bool enable_background_buffer;
  bool update_background_buffer;
  cursortype newcursor;
  actiontype action;
  EventResult();
};

