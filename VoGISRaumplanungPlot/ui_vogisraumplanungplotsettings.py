# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vogisraumplanungplotsettings.ui'
#
# Created: Mon Jan 27 10:45:46 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_VoGISRaumplanungPlotSettings(object):
    def setupUi(self, VoGISRaumplanungPlotSettings):
        VoGISRaumplanungPlotSettings.setObjectName(_fromUtf8("VoGISRaumplanungPlotSettings"))
        VoGISRaumplanungPlotSettings.resize(689, 152)
        VoGISRaumplanungPlotSettings.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(VoGISRaumplanungPlotSettings)
        self.buttonBox.setGeometry(QtCore.QRect(500, 120, 176, 27))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayoutWidget = QtGui.QWidget(VoGISRaumplanungPlotSettings)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 671, 101))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.LE_EINSTELLUNGEN = QtGui.QLineEdit(self.gridLayoutWidget)
        self.LE_EINSTELLUNGEN.setObjectName(_fromUtf8("LE_EINSTELLUNGEN"))
        self.gridLayout.addWidget(self.LE_EINSTELLUNGEN, 0, 1, 1, 1)
        self.LE_FILE_GEM = QtGui.QLineEdit(self.gridLayoutWidget)
        self.LE_FILE_GEM.setObjectName(_fromUtf8("LE_FILE_GEM"))
        self.gridLayout.addWidget(self.LE_FILE_GEM, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(VoGISRaumplanungPlotSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VoGISRaumplanungPlotSettings.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VoGISRaumplanungPlotSettings.accept)
        QtCore.QMetaObject.connectSlotsByName(VoGISRaumplanungPlotSettings)

    def retranslateUi(self, VoGISRaumplanungPlotSettings):
        VoGISRaumplanungPlotSettings.setWindowTitle(_translate("VoGISRaumplanungPlotSettings", "Dialog", None))
        self.label_4.setText(_translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p align=\"center\">Liste Gemeinden<br/>(voller Pfad mit<br/>Schreibberechtigung!)</p></body></html>", None))
        self.label.setText(_translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p>Einstellungsdatei<br/>(voller Pfad)</p></body></html>", None))

