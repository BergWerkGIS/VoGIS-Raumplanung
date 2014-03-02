# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vogisraumplanungplotsettings.ui'
#
# Created: Sun Mar  2 13:18:40 2014
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
        VoGISRaumplanungPlotSettings.resize(727, 144)
        VoGISRaumplanungPlotSettings.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(VoGISRaumplanungPlotSettings)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(VoGISRaumplanungPlotSettings)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(VoGISRaumplanungPlotSettings)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.LE_EINSTELLUNGEN = QtGui.QLineEdit(VoGISRaumplanungPlotSettings)
        self.LE_EINSTELLUNGEN.setObjectName(_fromUtf8("LE_EINSTELLUNGEN"))
        self.gridLayout.addWidget(self.LE_EINSTELLUNGEN, 0, 2, 1, 1)
        self.LE_FILE_GEM = QtGui.QLineEdit(VoGISRaumplanungPlotSettings)
        self.LE_FILE_GEM.setObjectName(_fromUtf8("LE_FILE_GEM"))
        self.gridLayout.addWidget(self.LE_FILE_GEM, 1, 2, 1, 1)
        self.BTN_FileSettings = QtGui.QPushButton(VoGISRaumplanungPlotSettings)
        self.BTN_FileSettings.setMaximumSize(QtCore.QSize(50, 16777215))
        self.BTN_FileSettings.setObjectName(_fromUtf8("BTN_FileSettings"))
        self.gridLayout.addWidget(self.BTN_FileSettings, 0, 1, 1, 1)
        self.BTN_FileGemCache = QtGui.QPushButton(VoGISRaumplanungPlotSettings)
        self.BTN_FileGemCache.setMaximumSize(QtCore.QSize(50, 16777215))
        self.BTN_FileGemCache.setObjectName(_fromUtf8("BTN_FileGemCache"))
        self.gridLayout.addWidget(self.BTN_FileGemCache, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(VoGISRaumplanungPlotSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(VoGISRaumplanungPlotSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VoGISRaumplanungPlotSettings.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VoGISRaumplanungPlotSettings.accept)
        QtCore.QObject.connect(self.BTN_FileSettings, QtCore.SIGNAL(_fromUtf8("clicked()")), VoGISRaumplanungPlotSettings.selectFileSettings)
        QtCore.QObject.connect(self.BTN_FileGemCache, QtCore.SIGNAL(_fromUtf8("clicked()")), VoGISRaumplanungPlotSettings.selectFileGemCache)
        QtCore.QMetaObject.connectSlotsByName(VoGISRaumplanungPlotSettings)

    def retranslateUi(self, VoGISRaumplanungPlotSettings):
        VoGISRaumplanungPlotSettings.setWindowTitle(_translate("VoGISRaumplanungPlotSettings", "Dialog", None))
        self.label.setText(_translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p>Einstellungsdatei<br/>(voller Pfad)</p></body></html>", None))
        self.label_4.setText(_translate("VoGISRaumplanungPlotSettings", "<html><head/><body><p align=\"center\">Liste Gemeinden<br/>(voller Pfad mit<br/>Schreibberechtigung!)</p></body></html>", None))
        self.BTN_FileSettings.setText(_translate("VoGISRaumplanungPlotSettings", "...", None))
        self.BTN_FileGemCache.setText(_translate("VoGISRaumplanungPlotSettings", "...", None))

