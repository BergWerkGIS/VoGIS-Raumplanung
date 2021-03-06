# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VoGISRaumplanungPlot
                                 A QGIS plugin
 Create Plots
                              -------------------
        begin                : 2013-10-01
        copyright            : (C) 2014 by BergWerk GIS
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import resources_rc
from vogisraumplanungplotdialog import VoGISRaumplanungPlotDialog
from vogisraumplanungplotsettingsdialog import VoGISRaumplanungPlotSettingsDialog
import os.path
from vrpcore.vrpsettings import VRPSettings
from vrpcore.constvals import *


class VoGISRaumplanungPlot:

    def __init__(self, iface):
        QgsMessageLog.logMessage(u'{0}: initialisiere'.format(DLG_CAPTION), DLG_CAPTION)
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'vogisraumplanungplot_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        #http://www.iconarchive.com/show/build-icons-by-umar123/0045-Map-icon.html
        self.action = QAction( QIcon(":/plugins/vogisraumplanungplot/icon.png"), u"VoGIS Plot", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&VoGIS Raumplanung", self.action)

        self.action_settings = QAction( QIcon(":/plugins/vogisraumplanungplot/icon.png"), u"VoGIS Plot Einstelllungen", self.iface.mainWindow())
        self.action_settings.triggered.connect(self.settings)
        self.iface.addPluginToMenu(u"&VoGIS Raumplanung", self.action_settings)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&VoGIS Raumplanung", self.action)
        self.iface.removePluginMenu(u"&VoGIS Raumplanung", self.action_settings)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        s = VRPSettings()
        s.log()
        file_settings = s.read(s.key_file_settings)
        file_gem_cache = s.read(s.key_file_gemeinden)
        if (
            file_settings is None or
            file_settings.isspace() or
            file_settings == '' or
            file_gem_cache is None or
            file_gem_cache.isspace() or
            file_gem_cache == ''
            ):
            dlg = VoGISRaumplanungPlotSettingsDialog(self.iface, s)
            dlg.show()
            #0=cancel 1=OK
            result = dlg.exec_()
            if result != 1:
                return

        # Create the dialog (after translation) and keep reference
        self.dlg = VoGISRaumplanungPlotDialog(self.iface, s)
        self.dlg.show()
        result = self.dlg.exec_()
        if result == 1:
            pass

    def settings(self):
        s = VRPSettings()
        s.log()
        dlg = VoGISRaumplanungPlotSettingsDialog(self.iface, s)
        dlg.show()
        dlg.exec_()
