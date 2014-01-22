# -*- coding: utf-8 -*-
import sys
from os import path
#import time
#from qgis.core import QgsMessageLog
from qgis.core import QgsVectorLayer
#from ..vrpcore.constvals import *


class VRPGemeinden:
    """
    Read names of communes.
    Either from cache file or from shape file.
    """

    def __init__(self, settings):
        self.s = settings
        self.datadir = self.s.read(self.s.key_datadir_base)
        self.geodir = self.s.read(self.s.key_datadirname_geodaten)
        self.cached_filename = self.s.read(self.s.key_file_gemeinden)
        self.shape_full_filename = path.join(
                                             self.datadir,
                                             self.geodir,
                                             'Grenzen',
                                             'DKM',
                                             'Vorarlberg',
                                             'Grundstuecke',
                                             'GST.shp')
        self.gstke = {}

    def get_names(self):
        """Return names of communes"""
        gem_names = []

        try:
            with open(self.cached_filename, 'r') as cfile:
                #TODO: INVESTIGATE! with QgsMessageLog opnening of the dialog
                #takes AGES and does NOT show up in logwindow
                #QgsMessageLog('{0}'.format(VRP_DEBUG), DLG_CAPTION)
                #if VRP_DEBUG is True: QgsMessageLog('filed opened', DLG_CAPTION)
                for row in(row.strip() for row in cfile):
                    if row:
                        gem_names.append(row)
        except:
            #if VRP_DEBUG is True: print QgsMessageLog.logMessage('exception: cannot read cached GEMEINDENAMEN', DLG_CAPTION)
            lyr = QgsVectorLayer(self.shape_full_filename, 'XYZ', 'ogr')
            #start = time.clock()
            for feat in lyr.getFeatures():
                gem_name = feat['PGEM_NAME']
                if not gem_name in gem_names:
                    gem_names.append(gem_name)
            #step = time.clock()
            #print 'reading features:', (step - start)
            gem_names = sorted(gem_names)
            #print 'sorting names:', (time.clock() - step)
            try:
                with open(self.cached_filename, 'w') as cfile:
                    cfile.write('\n'.join(gem_names))
            except:
                gem_names = [self.cached_filename, 'FEHLER BEIM SPEICHERN DER GEMEINDENAMEN!']

        return gem_names

    def get_gst(self, gem_name):
        """
        Return parcels information for commune
        """
        try:
            if gem_name in self.gstke:
                return self.gstke[gem_name]
            shp_full_filename = path.join(
                                          self.datadir,
                                          self.geodir,
                                          'Grenzen',
                                          'DKM',
                                          gem_name,
                                          'Grundstuecke',
                                          'GST.shp')
            if path.exists(shp_full_filename) is False:
                return {'Shapefile nicht vorhanden!':'FEHLER'}
            lyr = QgsVectorLayer(shp_full_filename, 'XYZ', 'ogr')
            gst = {}
            for feat in lyr.getFeatures():
                gst[feat['GNR']] = feat
            self.gstke[gem_name] = gst
        except:
            return {'EXCEPTION':'{0}'.format(sys.exc_info()[0])}
        return self.gstke[gem_name]
