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

import os
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QHeaderView
from qgis.core import QgsMessageLog
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from qgis.core import QgsRasterLayer
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
        self.curr_gem_name = None
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

    def accept(self):
        if len(self.ui.LST_GEMEINDEN.selectedItems()) < 1:
            QMessageBox.warning(self.iface.mainWindow(), DLG_CAPTION, u'Keine Gemeinde gewählt!')
            return
        for i in xrange(0, self.ui.TREE_THEMEN.topLevelItemCount()):
            node_root = self.ui.TREE_THEMEN.topLevelItem(i)
            if node_root.checkState(0) == Qt.Checked:
                self.__add_thema_layer(node_root)
            for j in xrange(0, node_root.childCount()):
                node_thema = node_root.child(j)
                if node_thema.checkState(0) == Qt.Checked:
                    self.__add_thema_layer(node_thema)
        QDialog.accept(self)

    def reject(self):
        QDialog.reject(self)

    def __add_thema_layer(self, node):
        thema = node.data(0, Qt.UserRole)
        if thema.quellen is None:
            return
        for quelle in thema.quellen:
            pfad = quelle.pfad.replace('{gem_name}', self.curr_gem_name)
            qml = None
            if not quelle.qml is None:
                qml = quelle.qml.replace('{gem_name}', self.curr_gem_name)
            if VRP_DEBUG is True:
                QgsMessageLog.logMessage('ADD LAYER: {0}'.format(pfad), DLG_CAPTION)
                QgsMessageLog.logMessage('LAYER QML: {0}'.format(qml), DLG_CAPTION)
            if os.path.isfile(pfad) is False:
                QMessageBox.warning(self.iface.mainWindow(), DLG_CAPTION, u'Thema [{0}] nicht vorhanden:\n{1}'.format(thema.name, pfad))
            else:
                if pfad.endswith('.shp') is True:
                    layer = QgsVectorLayer(pfad, thema.name, "ogr")
                else:
                    fileinfo = QFileInfo(pfad)
                    basename = fileinfo.baseName()
                    layer = QgsRasterLayer(pfad, basename)
                    if not layer.isValid():
                        QMessageBox.warning(self.iface.mainWindow(), DLG_CAPTION, u'Raster [{0}] konnte nicht geladen werden:\n{1}'.format(thema.name, pfad))
                        continue
                if not qml is None:
                    layer.loadNamedStyle(qml)
                QgsMapLayerRegistry.instance().addMapLayer(layer)

    def lst_gem_clicked(self, item):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.ui.LST_GSTKE.clear()
            self.curr_gem_name = item.data(Qt.UserRole)
            if VRP_DEBUG is True: QgsMessageLog.logMessage('GEM SELECTION: {0}'.format(self.curr_gem_name), DLG_CAPTION)
            self.gstke = self.gem_src.get_gst(self.curr_gem_name)
            self.__add_gstke(self.ui.LE_GST_FILTER.text())
        finally:
            QApplication.restoreOverrideCursor()

    def gst_text_changed(self, msg):
        self.__add_gstke(msg)

    def lst_themen_item_changed(self, item, idx):
        if VRP_DEBUG is True: QgsMessageLog.logMessage('treeitem changed: {0} {1}'.format(item, idx), DLG_CAPTION)
        checked = item.checkState(0)
        for i in xrange(0, item.childCount()):
            item.child(i).setCheckState(0, checked)


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
        themen = json_settings.themen()
        for thema_name, thema in themen.iteritems():
            tree_thema = QTreeWidgetItem(self.ui.TREE_THEMEN)
            tree_thema.setText(0, thema_name)
            tree_thema.setData(0, Qt.UserRole, thema)
            tree_thema.setFlags(tree_thema.flags() | Qt.ItemIsUserCheckable)
            #important! won't work otherwise
            tree_thema.setCheckState(0, Qt.Unchecked)
            if not thema.subthemen is None:
                for subthema in thema.subthemen:
                    if VRP_DEBUG is True: QgsMessageLog.logMessage(u'Subthema: {0}'.format(subthema.name), DLG_CAPTION)
                    tree_subthema = QTreeWidgetItem()
                    tree_subthema.setText(0, subthema.name)
                    tree_subthema.setData(0, Qt.UserRole, subthema)
                    tree_subthema.setFlags(tree_subthema.flags() | Qt.ItemIsUserCheckable)
                    tree_subthema.setCheckState(0, Qt.Unchecked)
                    tree_thema.addChild(tree_subthema)
