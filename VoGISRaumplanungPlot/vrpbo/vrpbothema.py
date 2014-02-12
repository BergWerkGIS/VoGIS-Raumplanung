# -*- coding: utf-8 -*-
"""Business object for Thema"""

from qgis.core import QgsMessageLog
from ..vrpcore.constvals import *


class VRPQuelle:
    """Data source"""
    def __init__(self, js_quelle, parent_name):
        #set name to parent, will be set again below, if quelle has own name
        self.name = parent_name
        self.pfad = js_quelle['pfad']
        self.qml = None
        self.statistik = False
        self.attribut = None
        self.filter = None
        self.text = None
        if 'name' in js_quelle:
            if not js_quelle['name'].isspace() and not js_quelle['name'] == '':
                self.name = js_quelle['name']
        if 'qml' in js_quelle:
            if not js_quelle['qml'].isspace() and not js_quelle['qml'] == '':
                self.qml = js_quelle['qml']
        if 'statistik' in js_quelle:
            self.statistik = js_quelle['statistik']
        if 'attribut' in js_quelle:
            if not js_quelle['attribut'].isspace() and not js_quelle['attribut'] == '':
                self.attribut = js_quelle['attribut']
        if 'filter' in js_quelle:
            if not js_quelle['filter'].isspace() and not js_quelle['filter'] == '':
                self.filter = js_quelle['filter']
        if 'text' in js_quelle:
            self.text = {}
            for txt in js_quelle['text']:
                self.text[txt] = js_quelle['text'][txt]


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
