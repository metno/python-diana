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

class QPainter
{
    %TypeHeaderCode
    #include <QtGui/QPainter>
    %End

public:
    QPainter();
    QPainter(QPaintDevice *);
    ~QPainter();

    bool begin(QPaintDevice *);
    bool end();
    bool isActive() const;

private:
    QPainter(const QPainter &);
};

class QPaintDevice
{
    %TypeHeaderCode
    #include <QtGui/QPaintDevice>
    %End

public:
    virtual ~QPaintDevice();

private:
    QPaintDevice();
};

class QImage : public QPaintDevice
{
    %TypeHeaderCode
    #include <QtGui/QImage>
    %End

public:
     enum Format {
        Format_Invalid,
        Format_Mono,
        Format_MonoLSB,
        Format_Indexed8,
        Format_RGB32,
        Format_ARGB32,
        Format_ARGB32_Premultiplied,
        Format_RGB16,
        Format_ARGB8565_Premultiplied,
        Format_RGB666,
        Format_ARGB6666_Premultiplied,
        Format_RGB555,
        Format_ARGB8555_Premultiplied,
        Format_RGB888,
        Format_RGB444,
        Format_ARGB4444_Premultiplied,
    };
    QImage();
    QImage(int width, int height, QImage::Format format);
    ~QImage();
    bool save(const QString &fileName, const char* format=0, int quality=-1) const;

private:
    QImage(const QImage &);
};

