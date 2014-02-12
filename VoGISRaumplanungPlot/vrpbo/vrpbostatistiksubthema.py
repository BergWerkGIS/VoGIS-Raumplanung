# -*- coding: utf-8 -*-
"""Business object for Grundstück Statistik"""

from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *

class VRPStatistikSubThema:
    """Statistics for one parcel"""
    def __init__(self, subthema_name, text_flaeche):
        self.name = subthema_name
        self.txt_area = text_flaeche

    def __str__(self):
        #{3:.2f}
        txt = ''
        for key, val in self.txt_area.iteritems():
            txt += '{0}:{1:.2f}; '.format(key, val)
        return '{1}{0}{2}'.format('\t', self.name, txt)

    def __unicode__(self):
        txt = u''
        for key, val in self.txt_area.iteritems():
            txt += u'{0}:{1:.2f}; '.format(key, val)
        return u'{1}{0}{2}'.format(u'\t', self.name, txt)
