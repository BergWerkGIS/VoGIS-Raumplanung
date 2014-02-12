# -*- coding: utf-8 -*-
"""Business object for Grunstück Statistik"""

from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *

class VRPStatistik:
    """Statistics for one parcel"""
    def __init__(self, gstk_nr, gstk_flaeche, gemeindename):
        self.gnr = gstk_nr
        self.flaeche = gstk_flaeche
        self.gem_name = gemeindename
        self.subthemen = []

    def add_subthema(self, subthema):
        """add subthema"""
        self.subthemen.append(subthema)

    def __str__(self):
        asstr = '{1}{0}{2}{0}{3:.2f}'.format('\t', self.gem_name, self.gnr, self.flaeche)
        for subthema in self.subthemen:
            asstr += '\n' + subthema.__str__()
        return asstr

    def __unicode__(self):
        asunicode = u'{1}{0}{2}{0}{3:.2f}'.format(u'\t', self.gem_name, self.gnr, self.flaeche)
        for subthema in self.subthemen:
            asunicode += u'\n' + subthema.__unicode__()
        return asunicode
