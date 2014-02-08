# -*- coding: utf-8 -*-
"""QGIS Settings for VoGIS Raumplanung Plot"""

from PyQt4.QtCore import QSettings
from qgis.core import QgsMessageLog
from constvals import *

class VRPSettings:
    """
    QGIS Settings for VoGIS Raumplanung Plot
    """

    def __init__(self):
        self.s = QSettings()
        self.key_file_settings = 'vogisraumplanungplot/filesettings'
        self.key_file_gemeinden = 'vogisraumplanungplot/filegemcache'
        self.key_file_pdf = 'vogisraumplanungplot/filepdf'

    def store(self, key, val):
        self.s.setValue(key, val)

    def read(self, key):
        return self.s.value(key, None)

    def log(self):
        if VRP_DEBUG is True:
            QgsMessageLog.logMessage('settings: {0}'.format(self.read(self.key_file_settings)), DLG_CAPTION)
            QgsMessageLog.logMessage('gemlist: {0}'.format(self.read(self.key_file_gemeinden)), DLG_CAPTION)
