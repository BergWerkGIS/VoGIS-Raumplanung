# -*- coding: utf-8 -*-
"""Class for reading JsonSettings"""

import json
from collections import OrderedDict
from ..vrpbo.vrpbothema import VRPThema

class JsonSettings:
    """Class for reading JsonSettings"""

    def __init__(self, filename):
        json_data = open(filename)
        self.json = json.load(json_data)

    def dkm_gesamt(self):
        """Path to DKM shapefile for whole Vorarlberg"""
        return self.json['dkmgesamt']['pfad'], self.json['dkmgesamt']['stand']

    def dkm_gemeinde(self, gem_name):
        """Path to DKM shapefile for specific Gemeinde"""
        pfad = self.json['dkmgemeinde']['pfad']
        return pfad.replace('{gem_name}', gem_name)

    def layouts(self):
        """Composer layouts (Name and QPT file path)"""


    def themen(self):
        """Return Topics"""
        vrp_themen = OrderedDict()
        for js_thema in self.json['themen']:
            thema = VRPThema(js_thema)
            vrp_themen[thema.name] = thema
        return vrp_themen
