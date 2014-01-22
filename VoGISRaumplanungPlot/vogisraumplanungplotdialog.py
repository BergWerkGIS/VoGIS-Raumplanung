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
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QHeaderView
from qgis.core import QgsMessageLog
from ui_vogisraumplanungplot import Ui_VoGISRaumplanungPlot
from vrpcore.vrpsettings import VRPSettings
from vrpcore.constvals import *
from vrpsources.vrpgemeinden import VRPGemeinden

class VoGISRaumplanungPlotDialog(QDialog):

    def __init__(self, iface, settings):
        self.iface = iface
        self.s = settings

        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_VoGISRaumplanungPlot()
        self.ui.setupUi(self)

        self.__add_themen()

        self.gem_src = VRPGemeinden(self.s)
        gem_names = self.gem_src.get_names()
        #if VRP_DEBUG is True: QgsMessageLog.logMessage('\n'.join(gem_names), DLG_CAPTION)
        for gem in gem_names:
            item = QListWidgetItem(gem)
            item.setData(Qt.UserRole, gem)
            self.ui.LST_GEMEINDEN.addItem(item)

    def lst_gem_clicked(self, item):
        self.ui.LST_GSTKE.clear()
        gem_name = item.data(Qt.UserRole)
        if VRP_DEBUG is True: QgsMessageLog.logMessage('GEM SELECTION: {0}'.format(gem_name), DLG_CAPTION)
        gstke = self.gem_src.get_gst(gem_name)
        #show them sorted
        for gst in sorted(gstke.iterkeys()):
            item = QListWidgetItem(gst)
            item.setData(Qt.UserRole, gst)
            if gstke[gst] != 'FEHLER':
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                #important! won't work otherwise
                item.setCheckState(Qt.Unchecked)
            self.ui.LST_GSTKE.addItem(item)

    def __add_themen(self):
        self.ui.TREE_THEMEN.headerItem().setText(0, '')
        #TODO: resize column to contents
        #all of these don't work??
        self.ui.TREE_THEMEN.header().resizeSection(0, 250)
        self.ui.TREE_THEMEN.header().setResizeMode(QHeaderView.ResizeToContents);
        self.ui.TREE_THEMEN.header().setStretchLastSection(True);
        roots = OrderedDict([
                 ('DKM', [u'Grundstücke', 'Beschriftung']),
                 ('Orthophoto',[]),
                 ('Raumplanung',[u'Flächenwidmungen', 'Beschriftung', u'Grünzone', u'Eignungszonen für Einkaufszentren', 'Einkaufszentren', 'Seveso-II Schutzabstand', u'Archäologische Fundzonen', 'Rohstoffplan']),
                 ('Gefahrenzonen (WLV)',['Rote Gefahrenzone', 'Gelbe Gefahrenzone', 'Braune Intensivzone und Hinweisbereich', 'Blauer Vorbehaltsbereich']),
                 ('Abfallwirtschaft',['Altstandorte', 'Deponien']),
                 ('Energie',['Gasleitungen', 'Hochspannungsleitungen', 'HS-Beschränkungsbereich']),
                 ('Geologie',['Geotopinventar']),
                 ('Naturschutz',['Natura 2000', 'Naturschutzgebiet', 'Pflanzenschutzgebiet', u'Geschützter Landschaftsteil', u'Biosphärenpark', 'Ruhezone', u'örtliches Schutzgebiet', u'Großraumbiotop', 'Streuwiesenevaluierung']),
                 ('Wasser',['Quellen', 'Brunnen', 'Schutzgebiet', 'GW-Schongebiet', 'HQ30', 'HQ100', 'HQ300'])
                 ])
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
