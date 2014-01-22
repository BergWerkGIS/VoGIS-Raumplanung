# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox
from qgis.core import QgsMessageLog
from vrpcore.constvals import *
from ui_vogisraumplanungplotsettings import Ui_VoGISRaumplanungPlotSettings


class VoGISRaumplanungPlotSettingsDialog(QDialog):

    def __init__(self, iface, settings):

        self.iface = iface
        self.s = settings

        QDialog.__init__(self)
        self.ui = Ui_VoGISRaumplanungPlotSettings()
        self.ui.setupUi(self)

        self.ui.LE_DATA_BASE.setText(self.s.read(self.s.key_datadir_base))
        self.ui.LE_DATA_GEO.setText(self.s.read(self.s.key_datadirname_geodaten))
        self.ui.LE_DATA_PRJ.setText(self.s.read(self.s.key_datadirname_projekte))
        self.ui.LE_FILE_GEM.setText(self.s.read(self.s.key_file_gemeinden))

    def reject(self):
        if VRP_DEBUG is True: QgsMessageLog.logMessage('ABBRUCH', DLG_CAPTION)
        QDialog.reject(self)

    def accept(self):
        if VRP_DEBUG is True: QgsMessageLog.logMessage('SPEICHERN', DLG_CAPTION)
        if VRP_DEBUG is True: QMessageBox.warning(self.iface.mainWindow(), DLG_CAPTION, 'TODO: Eingaben validieren!!!\n\n????\nDirekt in Settings\n??')

        self.s.store(self.s.key_datadir_base, self.ui.LE_DATA_BASE.text())
        self.s.store(self.s.key_datadirname_geodaten, self.ui.LE_DATA_GEO.text())
        self.s.store(self.s.key_datadirname_projekte, self.ui.LE_DATA_PRJ.text())
        self.s.store(self.s.key_file_gemeinden, self.ui.LE_FILE_GEM.text())

        QDialog.accept(self)

