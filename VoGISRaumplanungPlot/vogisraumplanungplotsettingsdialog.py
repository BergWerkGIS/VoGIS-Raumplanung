# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox
from qgis.core import QgsMessageLog
from vrpcore.constvals import *
from ui_vogisraumplanungplotsettings import Ui_VoGISRaumplanungPlotSettings


class VoGISRaumplanungPlotSettingsDialog(QDialog):

    def __init__(self, iface, settings):

        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        self.s = settings

        self.ui = Ui_VoGISRaumplanungPlotSettings()
        self.ui.setupUi(self)

        self.ui.LE_EINSTELLUNGEN.setText(self.s.read(self.s.key_file_settings))
        self.ui.LE_FILE_GEM.setText(self.s.read(self.s.key_file_gemeinden))

    def reject(self):
        if VRP_DEBUG is True: QgsMessageLog.logMessage('ABBRUCH', DLG_CAPTION)
        QDialog.reject(self)

    def accept(self):
        if VRP_DEBUG is True: QgsMessageLog.logMessage('SPEICHERN', DLG_CAPTION)
        if VRP_DEBUG is True: QMessageBox.warning(self.iface.mainWindow(), DLG_CAPTION, 'TODO: Eingaben validieren!!!\n\n????\nDirekt in Settings\n??')

        self.s.store(self.s.key_file_settings, self.ui.LE_EINSTELLUNGEN.text())
        self.s.store(self.s.key_file_gemeinden, self.ui.LE_FILE_GEM.text())

        QDialog.accept(self)

