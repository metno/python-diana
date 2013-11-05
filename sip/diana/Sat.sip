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

class Sat
{
%TypeHeaderCode
#include "diSat.h"
%End

public:
    bool approved;        ///< approved for plotting
    std::string satellite;   ///< main product name
    std::string filetype;    ///< subproduct
    std::string formatType;  ///< filetype (mitiff or hdf5)
    std::string metadata;
    std::string channelInfo;
    std::string paletteinfo;
    int hdf5type;
    std::vector<std::string> vch; ///< name of channels selected
    std::string filename;    ///< explicit selection of file
    std::string actualfile;  ///< actual filename used
    bool autoFile;        ///< filename from plot time
    float cut;            ///< image cut/stretch factor
    int alphacut;          ///< alpha-blending cutoff value
    int alpha;             ///< alpha-blending value
    int maxDiff;          ///< max allowed timedifference in minutes
    bool classtable;      ///< use classtable
    int nx;               ///< horizontal size of image
    int ny;               ///< vertical size of image
    Area area;            ///< Satellite area/projection
    double gridResolutionX; /// Grid Resolution in the X direction
    double gridResolutionY; /// Grid Resolution in the Y direction
    miutil::miTime time;          ///< valid time
    std::string annotation;  ///< annotation string
    std::string plotname;    ///< unique plotname
    bool palette;         ///< palette sat-file
    std::string plotChannels;///< channelname for annotation
    bool mosaic;          ///< make mosaic plot
    miutil::miTime firstMosaicFileTime; ///< time start for mosaic image generation
    miutil::miTime lastMosaicFileTime;  ///< time stop for mosaic image generation
    std::string satellite_name; ///< name of satellite from file
    bool commonColourStretch;    /// other images can use stretch from this image

    float TrueLat; ///< grid true latitude
    float GridRot; ///< grid rotation
    float Ax;      ///< grid parameter
    float Ay;      ///< grid parameter
    float Bx;      ///< grid parameter
    float By;      ///< grid parameter

    std::string projection;
    std::string proj_string;

    std::string cal_vis;            /// calibration info visible channel
    std::string cal_ir;             /// calibration info ir channel
    std::vector<std::string> cal_table;  /// calibration info
/*
    struct table_cal {
        std::string channel;
        std::vector<std::string> val;
        float a;
        float b;
    };
    std::map<int,table_cal> calibrationTable; /// calibration of current channels
*/
    std::vector<std::string> cal_channels;  /// name++ of current channels
};

