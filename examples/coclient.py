#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from metno.metlibs import ClientButton, miMessage, qmstrings
from metno.diana import *

class Window(QMainWindow):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)
        
        contents = QWidget()
        layout = QFormLayout(contents)

        self.nameEdit = QLineEdit()
        self.nameEdit.setText("Example")
        layout.addRow(self.tr("Name:"), self.nameEdit)
        self.latitudeEdit = QDoubleSpinBox()
        self.latitudeEdit.setRange(-90, 90)
        layout.addRow(self.tr("Latitude:"), self.latitudeEdit)
        self.longitudeEdit = QDoubleSpinBox()
        self.longitudeEdit.setRange(-180, 180)
        layout.addRow(self.tr("Longitude:"), self.longitudeEdit)
        
        self.sendButton = QPushButton(self.tr("Send coordinates"))
        self.sendButton.setEnabled(False)
        self.sendButton.clicked.connect(self.sendMessage)
        layout.addRow(self.sendButton)
        
        self.clientButton = ClientButton("coclient.py", "/usr/bin/coserver4", self.statusBar())
        self.statusBar().addPermanentWidget(self.clientButton, 0)
        self.clientButton.useLabel(True)
        self.clientButton.receivedMessage.connect(self.handleMessage)
        self.clientButton.addressListChanged.connect(self.handleConnection)

        self.setCentralWidget(contents)
    
    def handleMessage(self, message):
    
        if message.command == qmstrings.positions:

            # Receive positions from Diana.
            lat, lon = map(float, message.data[0].split(":"))
            self.latitudeEdit.setValue(lat)
            self.longitudeEdit.setValue(lon)
        else:
            print "command:    ", message.command
            print "commondesc: ", message.commondesc
            print "description:", message.description
            print "data:       ", message.data

    def handleConnection(self):

        self.sendButton.setEnabled(self.clientButton.clientTypeExist("Diana"))

        msg = miMessage()
        msg.command = qmstrings.enableshowtext
        msg.commondesc = "dataset:on"
        self.clientButton.sendMessage(msg)

    def sendMessage(self):

        msg = miMessage()
        msg.command = qmstrings.positions
        msg.commondesc = "dataset"
        msg.description = "name:lat:lon:annotation"
        data = "%s:%f:%f:%s" % (self.nameEdit.text(), self.latitudeEdit.value(), self.longitudeEdit.value(), self.nameEdit.text())
        msg.data = [data.encode("latin1")]
        self.clientButton.sendMessage(msg)

        msg = miMessage()
        msg.command = qmstrings.showpositions
        msg.commondesc = "dataset"
        self.clientButton.sendMessage(msg)

        msg = miMessage()
        msg.command = qmstrings.showpositionname
        msg.commondesc = "dataset:normal"
        msg.data = ["true:true"]
        self.clientButton.sendMessage(msg)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    paintgl = PaintGL()
    
    LocalSetupParser.parse("/etc/diana/3.35/diana.setup-COMMON")

    c = Controller()
    if not c.parseSetup():
        sys.exit(1)
    
    window = Window()
    window.show()

    sys.exit(app.exec_())
