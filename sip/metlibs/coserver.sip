/*
 python-diana - Python API for Diana - A Free Meteorological Visualisation Tool

 Copyright (C) 2014 met.no

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

%Import QtGui/QtGuimod.sip
%Import QtNetwork/QtNetworkmod.sip

class ClientButton : public QPushButton
{
%TypeHeaderCode
#include <coserver/ClientButton.h>
%End

public:
    ClientButton(const QString & text, const QString & server, QWidget * parent);
    %Docstring
    This button starts a new client and connects to the running coserver.
    It will start a new coserver if one is not already running.
    @param text Text to display with button
    @param server Which server to use
    @param parent Parent widget
    %End
    ~ClientButton();

    void sendMessage(miMessage &msg);
    %Docstring
    Sends a message.
    @param msg The message to be sent
    %End

    const std::string& getClientName(int id);

    bool clientTypeExist(const std::string &type);
    %Docstring
    Sends a request to the server to search for a
    specific type of client among the active connected
    clients.
    @param type The type of client(s) to search for
    %End

    void useLabel(bool label);
    %Docstring
    Sets the text-label on the button to label.
    @param label To use/not use label
    %End

    public Q_SLOTS:
    void connectToServer();
    %Docstring
    Connects to the running coserver if not connected,
    disconnects if already connected.
    %End

    void setLabel(const std::string& name);
    %Docstring
    Sets the name of the other connected client on the connect button.
    @param name Name of connecting client
    %End

    void connected();
    void disconnected();

    void unableToConnect();


Q_SIGNALS:
    void receivedMessage(const miMessage&);
    void addressListChanged();
    void connectionClosed();
    void connectedToServer();
};

class CoClient : public QObject
{
%TypeHeaderCode
#include <coserver/CoClient.h>
%End

public:
    CoClient(const char* clientType, const char* host, const char* serverCommand, quint16 port = 0);
    ~CoClient();

    void setBroadcastClient();
    %Docstring
    Send message to all CoServer client
    %End

    void disconnectFromServer();
    %Docstring
    Disconnects from the server.
    %End

    bool sendMessage(miMessage &msg);
    %Docstring
    Sends a message to the server.
    @param msg The message
    @return Returns true upon successful sending, false otherwise
    %End

    bool notConnected();
    const std::string& getClientName(int);
    bool clientTypeExist(const std::string &type);

public Q_SLOTS:
    void connectToServer();
    %Docstring
    Connects to the server.
    %End

Q_SIGNALS:
    void receivedMessage(const miMessage&);
    void addressListChanged();
    void connected();
    void newClient(const std::string&);
    void unableToConnect();
    void disconnected();
};

class miMessage
{
%TypeHeaderCode
#include <coserver/miMessage.h>
%End

public:
  miMessage();
  miMessage(int to, int from, const char *command,
            const char *description);

  int to;
  int from /PyName=from_/;
  std::string command;
  std::string description;
  std::string commondesc;
  std::string common;
  std::string clientType;
  std::string co;
  std::vector <std::string> data;

  std::string content() const;
};

namespace qmstrings{
%TypeHeaderCode
#include <coserver/QLetterCommands.h>
%End
const char *vprof
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::vprof);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *vcross
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::vcross);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *addimage
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::addimage);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *positions
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::positions);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *showpositions
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::showpositions);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *hidepositions
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::hidepositions);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *changeimage
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::changeimage);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *showpositionname
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::showpositionname);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *showpositiontext
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::showpositiontext);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *enableposclick
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::enableposclick);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *enableposmove
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::enableposmove);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *showtext
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::showtext);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *enableshowtext
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::enableshowtext);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *textrequest
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::textrequest);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *selectposition
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::selectposition);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *settime
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::settime);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *remove
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::remove);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *removeclient
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::removeclient);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *newclient
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::newclient);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *allclients
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::allclients);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *timechanged
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::timechanged);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *init_HQC_params
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::init_HQC_params);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *update_HQC_params
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::update_HQC_params);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *select_HQC_param
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::select_HQC_param);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *apply_quickmenu
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::apply_quickmenu);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *station
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::station);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *changeimageandtext
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::changeimageandtext);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *changeimageandimage
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::changeimageandimage);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *seteditpositions
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::seteditpositions);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *editposition
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::editposition);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *copyvalue
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::copyvalue);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *areas
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::areas);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *selectarea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::selectarea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *areacommand
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::areacommand);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *showarea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::showarea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *changearea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::changearea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *deletearea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::deletearea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *annotation
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::annotation);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *changetype
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::changetype);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *autoredraw
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::autoredraw);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *redraw
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::redraw);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *sendkey
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::sendkey);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *editmode
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::editmode);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *printclicked
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::printclicked);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *getcurrentplotcommand
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::getcurrentplotcommand);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *currentplotcommand
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::currentplotcommand);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *getproj4maparea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::getproj4maparea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *proj4maparea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::proj4maparea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *getmaparea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::getmaparea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *maparea
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::maparea);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *directory_changed
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::directory_changed);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};
const char *file_changed
{
    %GetCode
    sipPy = PyString_FromString(qmstrings::file_changed);
    %End
    %SetCode
    PyErr_SetString(PyExc_ValueError, "cannot assign to constants");
    sipErr = 1;
    %End
};

const int default_id;
const int all;
const int port;
};
