# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vogisraumplanungplot.ui'
#
# Created: Wed Jan 22 19:47:13 2014
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
        VoGISRaumplanungPlot.resize(757, 551)
        self.buttonBox = QtGui.QDialogButtonBox(VoGISRaumplanungPlot)
        self.buttonBox.setGeometry(QtCore.QRect(10, 510, 591, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayoutWidget = QtGui.QWidget(VoGISRaumplanungPlot)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 741, 491))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.LST_GSTKE = QtGui.QListWidget(self.gridLayoutWidget)
        self.LST_GSTKE.setObjectName(_fromUtf8("LST_GSTKE"))
        self.gridLayout.addWidget(self.LST_GSTKE, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.LST_GEMEINDEN = QtGui.QListWidget(self.gridLayoutWidget)
        self.LST_GEMEINDEN.setObjectName(_fromUtf8("LST_GEMEINDEN"))
        self.gridLayout.addWidget(self.LST_GEMEINDEN, 1, 0, 1, 1)
        self.TREE_THEMEN = QtGui.QTreeWidget(self.gridLayoutWidget)
        self.TREE_THEMEN.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.TREE_THEMEN.setRootIsDecorated(True)
        self.TREE_THEMEN.setObjectName(_fromUtf8("TREE_THEMEN"))
        self.TREE_THEMEN.headerItem().setText(0, _fromUtf8("1"))
        self.TREE_THEMEN.header().setDefaultSectionSize(150)
        self.gridLayout.addWidget(self.TREE_THEMEN, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.retranslateUi(VoGISRaumplanungPlot)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VoGISRaumplanungPlot.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VoGISRaumplanungPlot.reject)
        QtCore.QObject.connect(self.LST_GEMEINDEN, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), VoGISRaumplanungPlot.lst_gem_clicked)
        QtCore.QMetaObject.connectSlotsByName(VoGISRaumplanungPlot)

    def retranslateUi(self, VoGISRaumplanungPlot):
        VoGISRaumplanungPlot.setWindowTitle(QtGui.QApplication.translate("VoGISRaumplanungPlot", "VoGISRaumplanungPlot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VoGISRaumplanungPlot", "Grundstücke", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VoGISRaumplanungPlot", "Gemeinden", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VoGISRaumplanungPlot", "Themen", None, QtGui.QApplication.UnicodeUTF8))

