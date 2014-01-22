# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vogisraumplanungplot.ui'
#
# Created: Wed Jan 22 09:46:32 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VoGISRaumplanungPlot(object):
    def setupUi(self, VoGISRaumplanungPlot):
        VoGISRaumplanungPlot.setObjectName(_fromUtf8("VoGISRaumplanungPlot"))
        VoGISRaumplanungPlot.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(VoGISRaumplanungPlot)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(VoGISRaumplanungPlot)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VoGISRaumplanungPlot.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VoGISRaumplanungPlot.reject)
        QtCore.QMetaObject.connectSlotsByName(VoGISRaumplanungPlot)

    def retranslateUi(self, VoGISRaumplanungPlot):
        VoGISRaumplanungPlot.setWindowTitle(QtGui.QApplication.translate("VoGISRaumplanungPlot", "VoGISRaumplanungPlot", None, QtGui.QApplication.UnicodeUTF8))

