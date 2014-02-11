# -*- coding: utf-8 -*-

from os import path
from tempfile import TemporaryFile
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QFileDialog
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
        if VRP_DEBUG is True: QgsMessageLog.logMessage('Einstellungen: ABBRUCH', DLG_CAPTION)
        QDialog.reject(self)

    def accept(self):
        if VRP_DEBUG is True: QgsMessageLog.logMessage('Einstellungen: SPEICHERN', DLG_CAPTION)
        file_settings = self.ui.LE_EINSTELLUNGEN.text()
        file_gemcache = self.ui.LE_FILE_GEM.text()
        if path.isfile(file_settings) is False:
            QMessageBox.warning(self.iface.mainWindow(), DLG_CAPTION, 'Einstellungsdatei: Nicht vorhanden!')
            return
        if self.__canWrite(file_gemcache) is False:
            msg = 'Gemeindeliste: Keine Schreibberechtigung im Verzeichnis!\n\nEinstellungen trotzdem speichern?'
            answer = QMessageBox.question(
                                          self.iface.mainWindow(),
                                          DLG_CAPTION,
                                          msg,
                                          QMessageBox.Yes | QMessageBox.No
                                          )
            if QMessageBox.No == answer:
                return
        self.s.store(self.s.key_file_settings, file_settings)
        self.s.store(self.s.key_file_gemeinden, file_gemcache)

        QDialog.accept(self)

    def __canWrite(self, cache_file):
        pfad = path.dirname(cache_file)
        tmp_file = TemporaryFile(dir=pfad)
        try:
            print 'WRiTING TEST', tmp_file
            return True
        except:
            return False
        finally:
            tmp_file.close()

    def selectFileSettings(self):
        file_dlg = QFileDialog(self.iface.mainWindow())
        jsn_set = file_dlg.getOpenFileName(
                                           self.iface.mainWindow(),
                                           "Einstellungsdatei ...",
                                           self.s.read(self.s.key_file_settings),
                                           'JSON Datei (*.json)'
                                           )
        if jsn_set is None or jsn_set == '':
            return
        self.ui.LE_EINSTELLUNGEN.setText(jsn_set)
        self.s.store(self.s.key_file_settings, jsn_set)

    def selectFileGemCache(self):
        file_dlg = QFileDialog(self.iface.mainWindow())
        txt_out = file_dlg.getSaveFileName(
                                           self.iface.mainWindow(),
                                           "Cache Datei für Gemeindenamen ...",
                                           self.s.read(self.s.key_file_gemeinden),
                                           'Textdatei (*.txt)'
                                           )
        if txt_out is None or txt_out == '':
            return
        self.ui.LE_FILE_GEM.setText(txt_out)
        self.s.store(self.s.key_file_gemeinden, txt_out)

