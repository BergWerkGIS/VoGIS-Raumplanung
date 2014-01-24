# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VoGISRaumplanungPlotDialog
                                 A QGIS plugin
 Create Plots
                             -------------------
        begin                : 2013-12-15
        copyright            : (C) 2013 by BergWerk GIS
        email                : wb@BergWerk-GIS.at
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QHeaderView
from qgis.core import QgsMessageLog
from ui_vogisraumplanungplot import Ui_VoGISRaumplanungPlot
from vrpcore.vrpsettings import VRPSettings
from vrpcore.vrpjsonsettings import JsonSettings
from vrpcore.constvals import *
from vrpsources.vrpgemeinden import VRPGemeinden

class VoGISRaumplanungPlotDialog(QDialog):

    def __init__(self, iface, settings):
        self.iface = iface
        self.s = settings

        QDialog.__init__(self, iface.mainWindow())
        # Set up the user interface from Designer.
        self.ui = Ui_VoGISRaumplanungPlot()
        self.ui.setupUi(self)

        self.gstke = {}
        self.__add_themen()

        self.gem_src = VRPGemeinden(self.s)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            gem_names = self.gem_src.get_names()
            #if VRP_DEBUG is True: QgsMessageLog.logMessage('\n'.join(gem_names), DLG_CAPTION)
            for gem in gem_names:
                item = QListWidgetItem(gem)
                item.setData(Qt.UserRole, gem)
                self.ui.LST_GEMEINDEN.addItem(item)
        finally:
            QApplication.restoreOverrideCursor()

        #speed up items insertion
        self.ui.LST_GSTKE.setLayoutMode( QListWidget.Batched );
        self.ui.LST_GSTKE.setBatchSize( 100 );
        self.ui.LST_GSTKE.setUniformItemSizes(True);

    def lst_gem_clicked(self, item):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.ui.LST_GSTKE.clear()
            gem_name = item.data(Qt.UserRole)
            if VRP_DEBUG is True: QgsMessageLog.logMessage('GEM SELECTION: {0}'.format(gem_name), DLG_CAPTION)
            self.gstke = self.gem_src.get_gst(gem_name)
            self.__add_gstke(self.ui.LE_GST_FILTER.text())
        finally:
            QApplication.restoreOverrideCursor()

    def gst_text_changed(self, msg):
        self.__add_gstke(msg)

    def __add_gstke(self, filter):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.ui.LST_GSTKE.clear()
            #show them sorted
            for gst, props in sorted(self.gstke.iteritems()):
                item = None
                if gst == 'EXCEPTION':
                    item = QListWidgetItem(props)
                else:
                    if filter in gst:
                        item = QListWidgetItem(gst)
                        item.setData(Qt.UserRole, props)
                        if props != 'FEHLER':
                            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                            #important! won't work otherwise
                            item.setCheckState(Qt.Unchecked)
                if not item is None:
                    self.ui.LST_GSTKE.addItem(item)
        finally:
            QApplication.restoreOverrideCursor()

    def __add_themen(self):
        self.ui.TREE_THEMEN.headerItem().setText(0, '')
        #TODO: resize column to contents
        #all of these don't work??
        self.ui.TREE_THEMEN.header().resizeSection(0, 250)
        self.ui.TREE_THEMEN.header().setResizeMode(QHeaderView.ResizeToContents);
        self.ui.TREE_THEMEN.header().setStretchLastSection(True);
        # roots = OrderedDict([
        #          ('DKM', [u'Grundstücke', 'Beschriftung']),
        #          ('Orthophoto',[]),
        #          ('Raumplanung',[u'Flächenwidmungen', 'Beschriftung', u'Grünzone', u'Eignungszonen für Einkaufszentren', 'Einkaufszentren', 'Seveso-II Schutzabstand', u'Archäologische Fundzonen', 'Rohstoffplan']),
        #          ('Gefahrenzonen (WLV)',['Rote Gefahrenzone', 'Gelbe Gefahrenzone', 'Braune Intensivzone und Hinweisbereich', 'Blauer Vorbehaltsbereich']),
        #          ('Abfallwirtschaft',['Altstandorte', 'Deponien']),
        #          ('Energie',['Gasleitungen', 'Hochspannungsleitungen', 'HS-Beschränkungsbereich']),
        #          ('Geologie',['Geotopinventar']),
        #          ('Naturschutz',['Natura 2000', 'Naturschutzgebiet', 'Pflanzenschutzgebiet', u'Geschützter Landschaftsteil', u'Biosphärenpark', 'Ruhezone', u'örtliches Schutzgebiet', u'Großraumbiotop', 'Streuwiesenevaluierung']),
        #          ('Wasser',['Quellen', 'Brunnen', 'Schutzgebiet', 'GW-Schongebiet', 'HQ30', 'HQ100', 'HQ300'])
        #          ])
        json_settings = JsonSettings(self.s.read(self.s.key_file_settings))
        roots = json_settings.themen()
        for root, nodes in roots.iteritems():
            child = QTreeWidgetItem(self.ui.TREE_THEMEN)
            child.setText(0, root)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            #important! won't work otherwise
            child.setCheckState(0, Qt.Unchecked)
            for node in nodes:
                child2 = QTreeWidgetItem()
                child2.setText(0, node)
                child2.setFlags(child2.flags() | Qt.ItemIsUserCheckable)
                #important! won't work otherwise
                child2.setCheckState(0, Qt.Unchecked)
                child.addChild(child2)
