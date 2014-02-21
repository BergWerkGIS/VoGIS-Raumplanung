# -*- coding: utf-8 -*-
"""Business object for Grunstück Statistik"""

from collections import OrderedDict
from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *

class VRPStatistik:
    """Statistics for one parcel"""
    def __init__(self, gstk_nr, thema_name, gstk_flaeche, gemeindename):
        self.gnr = gstk_nr
        self.thema = thema_name
        self.flaeche = gstk_flaeche
        self.gem_name = gemeindename
        self.subthemen = OrderedDict()

    def add_subthema(self, thema_name, subthema):
        """add subthema"""
        self.subthemen[thema_name] = subthema

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
