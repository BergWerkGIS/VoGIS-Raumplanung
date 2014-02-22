# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vogisraumplanungplot.ui'
#
# Created: Sat Feb 22 11:52:46 2014
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
        VoGISRaumplanungPlot.resize(594, 556)
        VoGISRaumplanungPlot.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(VoGISRaumplanungPlot)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(VoGISRaumplanungPlot)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.LST_GSTKE = QtGui.QListWidget(VoGISRaumplanungPlot)
        self.LST_GSTKE.setObjectName(_fromUtf8("LST_GSTKE"))
        self.gridLayout.addWidget(self.LST_GSTKE, 4, 1, 1, 1)
        self.label = QtGui.QLabel(VoGISRaumplanungPlot)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.LST_GEMEINDEN = QtGui.QListWidget(VoGISRaumplanungPlot)
        self.LST_GEMEINDEN.setObjectName(_fromUtf8("LST_GEMEINDEN"))
        self.gridLayout.addWidget(self.LST_GEMEINDEN, 4, 0, 1, 1)
        self.TREE_THEMEN = QtGui.QTreeWidget(VoGISRaumplanungPlot)
        self.TREE_THEMEN.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.TREE_THEMEN.setRootIsDecorated(True)
        self.TREE_THEMEN.setObjectName(_fromUtf8("TREE_THEMEN"))
        self.TREE_THEMEN.headerItem().setText(0, _fromUtf8("1"))
        self.TREE_THEMEN.header().setDefaultSectionSize(150)
        self.gridLayout.addWidget(self.TREE_THEMEN, 4, 2, 1, 1)
        self.label_3 = QtGui.QLabel(VoGISRaumplanungPlot)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.LE_GST_FILTER = QtGui.QLineEdit(VoGISRaumplanungPlot)
        self.LE_GST_FILTER.setObjectName(_fromUtf8("LE_GST_FILTER"))
        self.gridLayout.addWidget(self.LE_GST_FILTER, 1, 1, 1, 1)
        self.CHK_Ortho = QtGui.QCheckBox(VoGISRaumplanungPlot)
        self.CHK_Ortho.setObjectName(_fromUtf8("CHK_Ortho"))
        self.gridLayout.addWidget(self.CHK_Ortho, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.CB_Layout = QtGui.QComboBox(VoGISRaumplanungPlot)
        self.CB_Layout.setObjectName(_fromUtf8("CB_Layout"))
        self.verticalLayout.addWidget(self.CB_Layout)
        self.buttonBox = QtGui.QDialogButtonBox(VoGISRaumplanungPlot)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(VoGISRaumplanungPlot)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VoGISRaumplanungPlot.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VoGISRaumplanungPlot.reject)
        QtCore.QObject.connect(self.LST_GEMEINDEN, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), VoGISRaumplanungPlot.lst_gem_clicked)
        QtCore.QObject.connect(self.LE_GST_FILTER, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), VoGISRaumplanungPlot.gst_text_changed)
        QtCore.QObject.connect(self.TREE_THEMEN, QtCore.SIGNAL(_fromUtf8("itemChanged(QTreeWidgetItem*,int)")), VoGISRaumplanungPlot.lst_themen_item_changed)
        QtCore.QObject.connect(self.LST_GEMEINDEN, QtCore.SIGNAL(_fromUtf8("currentItemChanged(QListWidgetItem*,QListWidgetItem*)")), VoGISRaumplanungPlot.lst_gem_currentItem_changed)
        QtCore.QMetaObject.connectSlotsByName(VoGISRaumplanungPlot)

    def retranslateUi(self, VoGISRaumplanungPlot):
        VoGISRaumplanungPlot.setWindowTitle(_translate("VoGISRaumplanungPlot", "VoGISRaumplanungPlot", None))
        self.label_2.setText(_translate("VoGISRaumplanungPlot", "Grundstücke", None))
        self.label.setText(_translate("VoGISRaumplanungPlot", "Gemeinden", None))
        self.label_3.setText(_translate("VoGISRaumplanungPlot", "Themen", None))
        self.CHK_Ortho.setText(_translate("VoGISRaumplanungPlot", "Orthofoto", None))

