# -*- coding: utf-8 -*-
"""Class for reading JsonSettings"""

import json
from collections import OrderedDict
from ..vrpbo.vrpbothema import VRPQuelle
from ..vrpbo.vrpbothema import VRPThema
from ..vrpbo.vrpbolayout import VRPLayout

class JsonSettings:
    """Class for reading JsonSettings"""

    def __init__(self, filename):
        json_data = open(filename)
        self.json = json.load(json_data)

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
        shpgstk = self.json['dkmgemeinde']['shpgstk']
        shpgstk = shpgstk.replace('{gem_name}', gem_name)
        qmlgstk = self.json['dkmgemeinde']['qmlgstk']
        qmlgstk = qmlgstk.replace('{gem_name}', gem_name)
        shpgnr = self.json['dkmgemeinde']['shpgnr']
        shpgnr = shpgnr.replace('{gem_name}', gem_name)
        qmlgnr = self.json['dkmgemeinde']['qmlgnr']
        qmlgnr = qmlgnr.replace('{gem_name}', gem_name)
        return {'shpgstk':shpgstk, 'qmlgstk':qmlgstk, 'shpgnr':shpgnr, 'qmlgnr':qmlgnr}

    def luftbild(self):
        """Path to ortho image"""
        return self.json['luftbild']

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
