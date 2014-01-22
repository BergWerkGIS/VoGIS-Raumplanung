# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vogisraumplanungplotsettings.ui'
#
# Created: Wed Jan 22 13:34:49 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VoGISRaumplanungPlotSettings(object):
    def setupUi(self, VoGISRaumplanungPlotSettings):
        VoGISRaumplanungPlotSettings.setObjectName(_fromUtf8("VoGISRaumplanungPlotSettings"))
        VoGISRaumplanungPlotSettings.resize(699, 208)
        self.buttonBox = QtGui.QDialogButtonBox(VoGISRaumplanungPlotSettings)
        self.buttonBox.setGeometry(QtCore.QRect(230, 170, 176, 27))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayoutWidget = QtGui.QWidget(VoGISRaumplanungPlotSettings)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 671, 156))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.LE_DATA_GEO = QtGui.QLineEdit(self.gridLayoutWidget)
        self.LE_DATA_GEO.setObjectName(_fromUtf8("LE_DATA_GEO"))
        self.gridLayout.addWidget(self.LE_DATA_GEO, 1, 1, 1, 1)
        self.LE_DATA_PRJ = QtGui.QLineEdit(self.gridLayoutWidget)
        self.LE_DATA_PRJ.setObjectName(_fromUtf8("LE_DATA_PRJ"))
        self.gridLayout.addWidget(self.LE_DATA_PRJ, 2, 1, 1, 1)
        self.LE_DATA_BASE = QtGui.QLineEdit(self.gridLayoutWidget)
        self.LE_DATA_BASE.setObjectName(_fromUtf8("LE_DATA_BASE"))
        self.gridLayout.addWidget(self.LE_DATA_BASE, 0, 1, 1, 1)
        self.LE_FILE_GEM = QtGui.QLineEdit(self.gridLayoutWidget)
        self.LE_FILE_GEM.setObjectName(_fromUtf8("LE_FILE_GEM"))
        self.gridLayout.addWidget(self.LE_FILE_GEM, 3, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.retranslateUi(VoGISRaumplanungPlotSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VoGISRaumplanungPlotSettings.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VoGISRaumplanungPlotSettings.accept)
        QtCore.QMetaObject.connectSlotsByName(VoGISRaumplanungPlotSettings)

    def retranslateUi(self, VoGISRaumplanungPlotSettings):
        VoGISRaumplanungPlotSettings.setWindowTitle(QtGui.QApplication.translate("VoGISRaumplanungPlotSettings", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p>Basisverzeichnis<br/>(voller Pfad)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p>Geodatenverzeichnis<br/>(nur Name)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p align=\"center\">Projekteverzeichnis<br/>(nur Name)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p align=\"center\">Liste Gemeinden<br/>(nur Name)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

