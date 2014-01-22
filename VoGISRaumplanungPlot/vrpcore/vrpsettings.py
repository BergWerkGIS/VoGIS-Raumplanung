# -*- coding: utf-8 -*-
from PyQt4.QtCore import QSettings
from qgis.core import QgsMessageLog
from constvals import *

class VRPSettings:
    """
    Settings for VoGIS Raumplanung Plot
    """

    def __init__(self):
        self.s = QSettings()
        #define settings keys
        self.key_datadir_base = 'vogisraumplanungplot/data'
        self.key_datadirname_geodaten = 'vogisraumplanungplot/geodaten'
        self.key_datadirname_projekte = 'vogisraumplanungplot/projekte'
        self.key_file_gemeinden = 'vogisraumplanungplot/listegemeinden'
        #initialize default values on first run
        if self.read(self.key_datadirname_geodaten) is None:
            self.store(self.key_datadirname_geodaten, 'Geodaten')
        if self.read(self.key_datadirname_projekte) is None:
            self.store(self.key_datadirname_projekte, 'Projekte')

    def store(self, key, val):
        self.s.setValue(key, val)

    def read(self, key):
        return self.s.value(key, None)

    def log(self):
        if VRP_DEBUG is True:
            QgsMessageLog.logMessage('basedir: {0}'.format(self.read(self.key_datadir_base)), DLG_CAPTION)
            QgsMessageLog.logMessage('geodir: {0}'.format(self.read(self.key_datadirname_geodaten)), DLG_CAPTION)
            QgsMessageLog.logMessage('prjdir: {0}'.format(self.read(self.key_datadirname_projekte)), DLG_CAPTION)
            QgsMessageLog.logMessage('gemlist: {0}'.format(self.read(self.key_file_gemeinden)), DLG_CAPTION)
