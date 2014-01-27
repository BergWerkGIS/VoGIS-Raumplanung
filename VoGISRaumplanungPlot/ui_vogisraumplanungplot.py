# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vogisraumplanungplot.ui'
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

class Ui_VoGISRaumplanungPlot(object):
    def setupUi(self, VoGISRaumplanungPlot):
        VoGISRaumplanungPlot.setObjectName(_fromUtf8("VoGISRaumplanungPlot"))
        VoGISRaumplanungPlot.resize(757, 551)
        VoGISRaumplanungPlot.setModal(True)
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
        self.gridLayout.addWidget(self.LST_GSTKE, 4, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.LST_GEMEINDEN = QtGui.QListWidget(self.gridLayoutWidget)
        self.LST_GEMEINDEN.setObjectName(_fromUtf8("LST_GEMEINDEN"))
        self.gridLayout.addWidget(self.LST_GEMEINDEN, 4, 0, 1, 1)
        self.TREE_THEMEN = QtGui.QTreeWidget(self.gridLayoutWidget)
        self.TREE_THEMEN.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.TREE_THEMEN.setRootIsDecorated(True)
        self.TREE_THEMEN.setObjectName(_fromUtf8("TREE_THEMEN"))
        self.TREE_THEMEN.headerItem().setText(0, _fromUtf8("1"))
        self.TREE_THEMEN.header().setDefaultSectionSize(150)
        self.gridLayout.addWidget(self.TREE_THEMEN, 4, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.LE_GST_FILTER = QtGui.QLineEdit(self.gridLayoutWidget)
        self.LE_GST_FILTER.setObjectName(_fromUtf8("LE_GST_FILTER"))
        self.gridLayout.addWidget(self.LE_GST_FILTER, 1, 1, 1, 1)

        self.retranslateUi(VoGISRaumplanungPlot)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VoGISRaumplanungPlot.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VoGISRaumplanungPlot.reject)
        QtCore.QObject.connect(self.LST_GEMEINDEN, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), VoGISRaumplanungPlot.lst_gem_clicked)
        QtCore.QObject.connect(self.LE_GST_FILTER, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), VoGISRaumplanungPlot.gst_text_changed)
        QtCore.QObject.connect(self.TREE_THEMEN, QtCore.SIGNAL(_fromUtf8("itemChanged(QTreeWidgetItem*,int)")), VoGISRaumplanungPlot.lst_themen_item_changed)
        QtCore.QMetaObject.connectSlotsByName(VoGISRaumplanungPlot)

    def retranslateUi(self, VoGISRaumplanungPlot):
        VoGISRaumplanungPlot.setWindowTitle(_translate("VoGISRaumplanungPlot", "VoGISRaumplanungPlot", None))
        self.label_2.setText(_translate("VoGISRaumplanungPlot", "Grundstücke", None))
        self.label.setText(_translate("VoGISRaumplanungPlot", "Gemeinden", None))
        self.label_3.setText(_translate("VoGISRaumplanungPlot", "Themen", None))

