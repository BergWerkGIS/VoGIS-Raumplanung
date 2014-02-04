# -*- coding: utf-8 -*-
"""Business object for Thema"""

from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *


class VRPQuelle:
    """Data source"""
    def __init__(self, js_quelle, parent_name):
        self.pfad = js_quelle['pfad']
        self.qml = None
        if 'qml' in js_quelle:
            if not js_quelle['qml'].isspace() and not js_quelle['qml'] == '':
                self.qml = js_quelle['qml']
        self.name = parent_name
        if 'name' in js_quelle:
            if not js_quelle['name'].isspace() and not js_quelle['name'] == '':
                self.name = js_quelle['name']


class VRPThema:
    """Thema"""

    def __init__(self, js_thema):
        self.name = js_thema['name']
        self.quellen = self.__get_quellen( js_thema['quellen']) if 'quellen' in js_thema else None
        self.subthemen = self.__get_sub_themen(js_thema['subthemen']) if 'subthemen' in js_thema else None

#    def __str__(self):
#        return '{0}, SubThemen:[{1}]'.format(self.name, ','.join(self.subthemen))

#    def __unicode__(self):
#        return u'{0}, SubThemen:[{1}]'.format(self.name, ','.join(self.subthemen))

    def __get_sub_themen(self, js_subthemen):
        subthemen = []
        for js_subthema in js_subthemen:
            if VRP_DEBUG is True: QgsMessageLog.logMessage('VRPThema Subthema: {0}'.format(js_subthema), DLG_CAPTION)
            subthemen.append(VRPThema(js_subthema))
        return subthemen

    def __get_quellen(self, js_quellen):
        quellen = []
        for js_quelle in js_quellen:
            if VRP_DEBUG is True: QgsMessageLog.logMessage('VRPQuelle: {0}'.format(js_quelle), DLG_CAPTION)
            quellen.append(VRPQuelle(js_quelle, self.name))
        return quellen
