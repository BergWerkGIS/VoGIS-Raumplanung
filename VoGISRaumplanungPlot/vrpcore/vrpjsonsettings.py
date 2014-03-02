# -*- coding: utf-8 -*-
"""Class for reading JsonSettings"""

import time
from collections import OrderedDict
from qgis.core import QgsMessageLog
#from ..vrpbo.vrpbothema import VRPQuelle
from ..vrpbo.vrpbothema import VRPThema
from ..vrpbo.vrpbolayout import VRPLayout
from ..vrpcore.constvals import *
try:
    import simplejson as json
except ImportError:
    import json

class JsonSettings:
    """Class for reading JsonSettings"""

    def __init__(self, iface, filename):
        self.iface = iface
        json_txt = ''
        time_start = time.time()
        json_file = open(filename, 'r')
        time_before_read_file = time.time()
        for line in json_file:
            if line.strip().startswith('//') is False:
                json_txt += line
        time_after_read_file = time.time()
        #self.json = json.load(json_file)
        time_before_decode_json = time.time()
        self.json = json.loads(json_txt)
        time_after_decode_json = time.time()
        if VRP_DEBUG is True:
            span_read_file = time_after_read_file - time_before_read_file
            span_decode_json = time_after_decode_json - time_before_decode_json
            span_initialization = time_after_decode_json - time_start
            QgsMessageLog.logMessage('JsonSettings (read file): {0:.3f}'.format(span_read_file), DLG_CAPTION)
            QgsMessageLog.logMessage('JsonSettings (decode json): {0:.3f}'.format(span_decode_json), DLG_CAPTION)
            QgsMessageLog.logMessage('JsonSettings (initialization): {0:.3f}'.format(span_initialization), DLG_CAPTION)


    def fld_pgem_name(self):
        """Attribute field with commune name"""
        return self.json['pgemnamefeld']
    def fld_kg(self):
        """Attribute field with KG number"""
        return self.json['kgfeld']

    def fld_gnr(self):
        """Attribute field with GSTK number"""
        return self.json['gnrfeld']

    def dkm_stand(self):
        """Date of DKM"""
        return self.json['dkmstand']

    def dkm_gesamt(self):
        """Path to DKM shapefile for whole Vorarlberg"""
        return self.json['dkmgesamt']['pfad']

    def dkm_gemeinde(self, gem_name):
        """Path to DKM shapefile for specific Gemeinde"""
        lyrnamegstk = self.json['dkmgemeinde']['lyrnamegstk']
        shpgstk = self.json['dkmgemeinde']['shpgstk']
        shpgstk = shpgstk.replace('{gem_name}', gem_name)
        qmlgstk = self.json['dkmgemeinde']['qmlgstk']
        qmlgstk = qmlgstk.replace('{gem_name}', gem_name)
        lyrnamegnr = self.json['dkmgemeinde']['lyrnamegnr']
        shpgnr = self.json['dkmgemeinde']['shpgnr']
        shpgnr = shpgnr.replace('{gem_name}', gem_name)
        qmlgnr = self.json['dkmgemeinde']['qmlgnr']
        qmlgnr = qmlgnr.replace('{gem_name}', gem_name)
        return {
                'lyrnamegstk':lyrnamegstk,
                'shpgstk':shpgstk,
                'qmlgstk':qmlgstk,
                'lyrnamegnr':lyrnamegnr,
                'shpgnr':shpgnr,
                'qmlgnr':qmlgnr
                }

    def luftbild(self):
        """Path to ortho image"""
        return self.json['luftbild']['pfad']

    def luftbild_lyrname(self):
        """Path to ortho image"""
        return self.json['luftbild']['lyrname']

    def textinfo_layout(self):
        """Composer layout for statistical textinfo"""
        return self.json['textinfolayout']

    def layouts(self):
        """Composer layouts (Name and QPT file path)"""
        vrp_layouts = OrderedDict()
        for js_layout in self.json['composerlayouts']:
            layout = VRPLayout(js_layout)
            vrp_layouts[layout.name] = layout
        return vrp_layouts


    def themen(self):
        """Return Topics"""
        vrp_themen = OrderedDict()
        for js_thema in self.json['themen']:
            thema = VRPThema(js_thema)
            vrp_themen[thema.name] = thema
        return vrp_themen
