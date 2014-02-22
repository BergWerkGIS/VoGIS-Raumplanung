# -*- coding: utf-8 -*-

import sys
from os import path
from qgis.core import QgsMessageLog
from qgis.core import QgsVectorLayer
from qgis.gui import QgsMessageBar
from ..vrpcore.constvals import *
from ..vrpcore.vrpjsonsettings import JsonSettings

class VRPGemeinden:
    """
    Read names of communes.
    Either from cache file or from shape file.
    """

    def __init__(self, iface, settings, jsonsettings):
        self.iface = iface
        #if self.qgis_settingsVRP_DEBUG is True: print QgsMessageLog.logMessage(u'import: {0}'.format(dir(vrpcore)), self.qgis_settingsDLG_CAPTION)
        if VRP_DEBUG is True: print QgsMessageLog.logMessage(u'import: {0}'.format(dir(JsonSettings)), DLG_CAPTION)
        self.qgis_settings = settings
        self.file_settings = self.qgis_settings.read(self.qgis_settings.key_file_settings)
        self.file_gemeinden = self.qgis_settings.read(self.qgis_settings.key_file_gemeinden)
        #self.json_settings = JsonSettings(self.file_settings)
        self.json_settings = jsonsettings
        self.dkm_gesamt_filename = self.json_settings.dkm_gesamt()
        stand = self.json_settings.dkm_stand()
        if VRP_DEBUG is True: print QgsMessageLog.logMessage(u'DKM Stand: {0}'.format(stand), DLG_CAPTION)
        self.gstke = {}

    def get_names(self):
        """Return names of communes"""
        gem_names = []

        try:
            with open(self.file_gemeinden, 'r') as cfile:
                if VRP_DEBUG is True: QgsMessageLog.logMessage('cached GEMEINDENAMEN opened', DLG_CAPTION)
                for row in(row.strip() for row in cfile):
                    if row:
                        gem_names.append(row)
        except:
            self.iface.messageBar().pushMessage(u'Liste mit Gemeindenamen wird neu erstellt.', QgsMessageBar.INFO)
            if VRP_DEBUG is True:
                QgsMessageLog.logMessage('exception: cannot read cached GEMEINDENAMEN', DLG_CAPTION)
                QgsMessageLog.logMessage(self.file_gemeinden, DLG_CAPTION)
            lyr = QgsVectorLayer(self.dkm_gesamt_filename, 'XYZ', 'ogr')
            #start = time.clock()
            for feat in lyr.getFeatures():
                gem_name = feat[self.json_settings.fld_pgem_name()]
                if not gem_name in gem_names:
                    gem_names.append(gem_name)
            #step = time.clock()
            #print 'reading features:', (step - start)
            gem_names = sorted(gem_names)
            #print 'sorting names:', (time.clock() - step)
            try:
                with open(self.file_gemeinden, 'w') as cfile:
                    cfile.write('\n'.join(gem_names))
            except:
                self.iface.messageBar().pushMessage(u'Liste mit Gemeindenamen konnte nicht gespeichert werden.', QgsMessageBar.CRITICAL)
                gem_names = [self.file_gemeinden, 'FEHLER BEIM SPEICHERN DER GEMEINDENAMEN!']

        return gem_names

    def get_gst(self, gem_name):
        """
        Return parcels information for commune
        """
        try:
            if gem_name in self.gstke:
                return self.gstke[gem_name]
            shp_full_filename = self.json_settings.dkm_gemeinde(gem_name)['shpgstk']
            if path.exists(shp_full_filename) is False:
                return {'Shapefile nicht vorhanden!':'FEHLER'}
            lyr = QgsVectorLayer(shp_full_filename, 'XYZ', 'ogr')
            gst = {}
            for feat in lyr.getFeatures():
                kgem = feat[self.json_settings.fld_kg()]
                gnr = feat[self.json_settings.fld_gnr()]
                gst['{0}:{1}'.format(kgem, gnr)] = {'id':feat.id(), 'kg':kgem, 'gnr':gnr, 'bbox':None }
            self.gstke[gem_name] = gst
        except AttributeError as exae:
            ex_txt = u'{0}'.format(exae.message)
            QgsMessageLog.logMessage('get_gst: {0}'.format(ex_txt), DLG_CAPTION)
            return {'EXCEPTION':ex_txt}
        except:
            ex_txt = 'xx{0}'.format(sys.exc_info()[0])
            QgsMessageLog.logMessage('get_gst: {0}'.format(ex_txt), DLG_CAPTION)
            return {'EXCEPTION':ex_txt}
        return self.gstke[gem_name]
