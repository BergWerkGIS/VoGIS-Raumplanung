# -*- coding: utf-8 -*-
"""Class for reading JsonSettings"""

import json
from collections import OrderedDict

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

    def themen(self):
        """Return Topics"""
        vrp_themen = OrderedDict()
        for thema in self.json['themen']:
            subthemen = []
            if 'subthemen' in thema:
                for subthema in thema['subthemen']:
                    subthemen.append(subthema['name'])
            vrp_themen[thema['name']] = subthemen
        return vrp_themen
