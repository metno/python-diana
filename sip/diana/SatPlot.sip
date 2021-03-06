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

class SatPlot : public Plot
{
%TypeHeaderCode
#include "diPoint.h"
#include "diSatPlot.h"
%End

public:
    SatPlot();
    ~SatPlot();

    Sat *satdata;

    void plot(DiGLPainter*, PlotOrder zorder);
    void setData(Sat *);
    void clearData();
    Area& getSatArea();
    double getGridResolutionX();
    double getGridResolutionY();
    void getSatAnnotation(std::string &, Colour &);
    void getSatName(std::string &);
    void getCalibChannels(std::vector<std::string>& channels);
    void values(float x,float y, std::vector<SatValues>& satval);
    %Docstring
    Returns the pixel value at the point specified by the x and y coordinates.

    bool getAnnotations(std::vector<std::string>& anno);
    %Docstring
    Returns the plot legend.
    %End

    void setSatAuto(bool, const std::string&, const std::string&);

protected:
    QImage rasterScaledImage(const GridArea&, int scale, const diutil::Rect& bbx, const diutil::Rect_v& cells);

private:
    SatPlot(const SatPlot &rhs);
};

